# 🎯 XAMPP Setup Guide for Crime Lab System

Quick guide for setting up the Crime Lab system using XAMPP.

## Step 1: Install XAMPP

1. Download XAMPP from [apachefriends.org](https://www.apachefriends.org/)
2. Install XAMPP (no special options needed)
3. Open XAMPP Control Panel

## Step 2: Start MySQL

1. In XAMPP Control Panel, click **Start** next to MySQL
2. Status should turn green
3. Port should show: **3306**

**Note:** You don't need to start Apache unless you want to.

## Step 3: Create Database

### Method 1: phpMyAdmin (GUI - Easier)

1. Open browser and go to: `http://localhost/phpmyadmin`
2. Click the **"SQL"** tab at the top
3. Open `database/schema.sql` file from the project in a text editor
4. Copy ALL the SQL code (includes suspects, match_history, AND gsr_sessions tables)
5. Paste it into the SQL query box in phpMyAdmin
6. Click **"Go"** button at the bottom
7. ✅ You should see "crime_lab" database appear in the left sidebar with three tables:
   - `suspects`
   - `match_history`
   - `gsr_sessions` (NEW - for polygraph data)

### Method 2: Command Line

```bash
# Navigate to project folder
cd /Users/bir_65/Fingerprint_automation

# Run MySQL command (XAMPP path)
/Applications/XAMPP/xamppfiles/bin/mysql -u root

# Inside MySQL prompt:
source database/schema.sql
exit;
```

## Step 4: Verify Database

In phpMyAdmin:
1. Click **"crime_lab"** database in left sidebar
2. You should see three tables:
   - `suspects` (5 sample suspects)
   - `match_history` (fingerprint match logs)
   - `gsr_sessions` (NEW - polygraph session data)

## Step 5: Configure Flask App

The `web_app/app.py` should have these settings for XAMPP:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Empty for default XAMPP
    'database': 'crime_lab'
}
```

**Your current password:** If you've set password to `'finger'`, keep it that way!

## Step 6: Test Connection

```bash
cd web_app
python3 app.py
```

If you see this, it's working:
```
Crime Lab Web Server Starting...
Access at: http://localhost:5000
```

If you see database errors:
- Check XAMPP MySQL is running (green in control panel)
- Verify password in `app.py` matches XAMPP settings
- Make sure database was created (check phpMyAdmin)

## Managing XAMPP

### Start/Stop MySQL
- Open XAMPP Control Panel
- Click Start/Stop next to MySQL

### View Database
- Always available at: `http://localhost/phpmyadmin`

### Check if MySQL is Running
- Look for green highlight in XAMPP Control Panel
- Port 3306 should be listed

### Common XAMPP Ports
- MySQL: 3306
- Apache: 80 (not needed for this project)
- phpMyAdmin: http://localhost/phpmyadmin

## Troubleshooting

### Port 3306 Already in Use
- Another MySQL instance is running
- Stop other MySQL services first
- Or change XAMPP MySQL port in config

### Can't Access phpMyAdmin
- Make sure Apache is started in XAMPP
- Try: `http://127.0.0.1/phpmyadmin`

### Database Connection Error in Flask
```python
# Check these in app.py:
'host': 'localhost',      # ✓ Correct
'user': 'root',           # ✓ Correct
'password': '',           # ✓ Empty or 'finger' if you set it
'database': 'crime_lab'   # ✓ Must match database name
```

### Database Not Found
- Go to phpMyAdmin
- Check if "crime_lab" exists in left sidebar
- If not, run `database/schema.sql` again

## Advantages of XAMPP

✅ Easy GUI control panel
✅ phpMyAdmin for visual database management  
✅ No password setup needed (default is empty)
✅ Easy to start/stop services
✅ Perfect for development and demos
✅ Cross-platform (Mac, Windows, Linux)
✅ Ready for fingerprint + polygraph integration

## New GSR (Polygraph) Feature

The Crime Lab system now includes:
- **Live stress detection** via GSR sensor on Arduino A0
- **Real-time graph** displayed on dossier page
- **Auto-calibrated baseline** from first 10 readings
- **Stress color coding** (green=stable, red=stress)
- **Database persistence** in `gsr_sessions` table
- **500ms update rate** for smooth real-time visualization

No additional XAMPP configuration needed—just ensure the `gsr_sessions` table is created by running the full schema.sql file.

---

**Next:** Follow [QUICKSTART.md](QUICKSTART.md) starting from Step 2!
