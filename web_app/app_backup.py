"""
Crime Lab Flask WebSocket Server
Real-time fingerprint match dossier display system
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import mysql.connector
from datetime import datetime
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'crime_lab_secret_2026'
socketio = SocketIO(app, cors_allowed_origins="*")

# ============================================
# Database Configuration
# ============================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Empty '' for default XAMPP, or your custom password
    'database': 'crime_lab'
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

# ============================================
# Routes
# ============================================

@app.route('/')
def index():
    """Home page - waiting for match"""
    return render_template('waiting.html')

@app.route('/suspect/<int:suspect_id>')
def suspect_dossier(suspect_id):
    """Display suspect dossier page"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Get suspect data
    cursor.execute("""
        SELECT * FROM suspects WHERE id = %s
    """, (suspect_id,))
    suspect = cursor.fetchone()
    
    # Get latest match for this suspect
    cursor.execute("""
        SELECT confidence_score, matched_at 
        FROM match_history 
        WHERE suspect_id = %s 
        ORDER BY matched_at DESC 
        LIMIT 1
    """, (suspect_id,))
    latest_match = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not suspect:
        return jsonify({'error': 'Suspect not found'}), 404
    
    # Add match data to suspect dict
    if latest_match:
        suspect['latest_confidence'] = latest_match['confidence_score']
        suspect['latest_match_time'] = latest_match['matched_at']
    else:
        suspect['latest_confidence'] = None
        suspect['latest_match_time'] = None
    
    return render_template('dossier.html', suspect=suspect)

@app.route('/api/suspect/<int:suspect_id>')
def get_suspect_data(suspect_id):
    """API endpoint to get suspect data as JSON"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT s.*, 
               (SELECT confidence_score FROM match_history 
                WHERE suspect_id = s.id 
                ORDER BY matched_at DESC LIMIT 1) as latest_confidence,
               (SELECT matched_at FROM match_history 
                WHERE suspect_id = s.id 
                ORDER BY matched_at DESC LIMIT 1) as latest_match_time
        FROM suspects s 
        WHERE s.id = %s
    """, (suspect_id,))
    
    suspect = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not suspect:
        return jsonify({'error': 'Suspect not found'}), 404
    
    # Convert datetime to string for JSON serialization
    if suspect.get('latest_match_time'):
        suspect['latest_match_time'] = suspect['latest_match_time'].strftime('%Y-%m-%d %H:%M:%S')
    if suspect.get('date_of_crime'):
        suspect['date_of_crime'] = suspect['date_of_crime'].strftime('%Y-%m-%d')
    if suspect.get('created_at'):
        suspect['created_at'] = suspect['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    
    return jsonify(suspect)

@app.route('/api/log-match', methods=['POST'])
def log_match():
    """
    Log a fingerprint match event
    Expected JSON: {"suspect_id": 1, "confidence": 225}
    """
    data = request.get_json()
    
    if not data or 'suspect_id' not in data or 'confidence' not in data:
        return jsonify({'error': 'Missing suspect_id or confidence'}), 400
    
    suspect_id = data['suspect_id']
    confidence = data['confidence']
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    
    try:
        # Insert match record
        cursor.execute("""
            INSERT INTO match_history (suspect_id, confidence_score) 
            VALUES (%s, %s)
        """, (suspect_id, confidence))
        
        conn.commit()
        
        # Broadcast to all connected WebSocket clients
        socketio.emit('new_match', {
            'suspect_id': suspect_id,
            'confidence': confidence,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'suspect_id': suspect_id,
            'confidence': confidence
        })
    
    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500

@app.route('/api/gsr', methods=['POST'])
def gsr_update():
    """
    Receive GSR sensor updates and broadcast to clients.
    Expected JSON: {"value": <int>}
    """
    data = request.get_json() or {}
    val = data.get('value')
    try:
        val = int(val)
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid GSR value'}), 400

    socketio.emit('gsr_update', {
        'value': val,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    return jsonify({'success': True})

@app.route('/api/gsr-session/start', methods=['POST'])
def gsr_session_start():
    """
    Start a new GSR session for a suspect.
    Expected JSON: {"suspect_id": <int>}
    Returns: {"session_id": <int>}
    """
    data = request.get_json() or {}
    suspect_id = data.get('suspect_id')
    try:
        suspect_id = int(suspect_id)
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid suspect_id'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO gsr_sessions (suspect_id) VALUES (%s)
            """,
            (suspect_id,)
        )
        conn.commit()
        session_id = cursor.lastrowid
        cursor.close(); conn.close()
        return jsonify({'success': True, 'session_id': session_id})
    except mysql.connector.Error as err:
        conn.rollback(); cursor.close(); conn.close()
        return jsonify({'error': str(err)}), 500

@app.route('/api/gsr-session/end', methods=['POST'])
def gsr_session_end():
    """
    End a GSR session and persist baseline/peak/readings.
    Expected JSON: {"session_id": <int>, "baseline": <int|null>, "readings": [ints]}
    """
    data = request.get_json() or {}
    session_id = data.get('session_id')
    baseline = data.get('baseline')
    readings = data.get('readings') or []

    try:
        session_id = int(session_id)
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid session_id'}), 400

    # Normalize baseline
    try:
        baseline = int(baseline) if baseline is not None else None
    except (TypeError, ValueError):
        baseline = None

    # Calculate peak if readings provided
    peak = max(readings) if isinstance(readings, list) and readings else None
    readings_json = json.dumps(readings) if isinstance(readings, list) else json.dumps([])

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE gsr_sessions
               SET baseline = %s,
                   peak = %s,
                   readings_json = %s,
                   ended_at = CURRENT_TIMESTAMP
             WHERE id = %s
            """,
            (baseline, peak, readings_json, session_id)
        )
        conn.commit()
        cursor.close(); conn.close()
        return jsonify({'success': True})
    except mysql.connector.Error as err:
        conn.rollback(); cursor.close(); conn.close()
        return jsonify({'error': str(err)}), 500

@app.route('/api/gsr-history/<int:suspect_id>')
def gsr_history(suspect_id):
    """Return GSR sessions history for the given suspect."""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT id, baseline, peak, started_at, ended_at,
                   readings_json,
                   JSON_LENGTH(readings_json) AS points
              FROM gsr_sessions
             WHERE suspect_id = %s
             ORDER BY started_at DESC
            """,
            (suspect_id,)
        )
        sessions = cursor.fetchall() or []
        # Fallback if JSON_LENGTH unsupported: estimate by commas
        for s in sessions:
            if s.get('points') is None and s.get('readings_json'):
                s['points'] = s['readings_json'].count(',') + 1
        cursor.close(); conn.close()
        return jsonify({'success': True, 'sessions': sessions})
    except mysql.connector.Error as err:
        cursor.close(); conn.close()
        return jsonify({'error': str(err)}), 500

@app.route('/api/suspects')
def list_suspects():
    """List all suspects in database"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, charges FROM suspects ORDER BY id")
    suspects = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(suspects)

# ============================================
# WebSocket Events
# ============================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f'Client connected: {request.sid}')
    emit('connection_response', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f'Client disconnected: {request.sid}')

@socketio.on('request_update')
def handle_update_request(data):
    """Handle manual update request from client"""
    suspect_id = data.get('suspect_id')
    if suspect_id:
        emit('refresh_dossier', {'suspect_id': suspect_id})

# ============================================
# Main
# ============================================

if __name__ == '__main__':
    print("=" * 50)
    print("Crime Lab Web Server Starting...")
    print("=" * 50)
    print("Access at: http://localhost:5001")
    print("WebSocket enabled for real-time updates")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    # Run with SocketIO
    socketio.run(app, debug=True, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)
