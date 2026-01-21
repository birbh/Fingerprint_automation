-- ============================================
-- Crime Lab Database Schema
-- Fingerprint Automation System
-- ============================================

-- Create database
CREATE DATABASE IF NOT EXISTS crime_lab;
USE crime_lab;

-- ============================================
-- Suspects Table
-- ============================================
CREATE TABLE IF NOT EXISTS suspects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    mugshot_path VARCHAR(500),
    charges TEXT,
    date_of_crime DATE,
    aliases TEXT,
    arrest_history TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================
-- Match History Table
-- Stores each fingerprint match event
-- ============================================
CREATE TABLE IF NOT EXISTS match_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    suspect_id INT NOT NULL,
    confidence_score INT NOT NULL,
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (suspect_id) REFERENCES suspects(id) ON DELETE CASCADE
);

-- ============================================
-- Sample Data - Test Suspects
-- ============================================

-- Suspect 1: John "The Shadow" Doe
INSERT INTO suspects (id, name, mugshot_path, charges, date_of_crime, aliases, arrest_history) VALUES
(1, 'John "The Shadow" Doe', 'suspects_images/suspect1.jpg', 
'Armed Robbery, Grand Theft Auto, Assault with a Deadly Weapon', 
'2024-03-15',
'Johnny Shadow, J.D., The Ghost, Shadow Man',
'2020-05-12: Petty Theft (6 months probation)
2021-11-03: Breaking and Entering (1 year jail)
2023-07-22: Assault (2 years probation)
2024-03-15: Armed Robbery (WANTED)');

-- Suspect 2: Theo Ash
INSERT INTO suspects (id, name, mugshot_path, charges, date_of_crime, aliases, arrest_history) VALUES
(2, 'Theo Ash', 'suspects_images/suspect2.jpg',
'Identity Theft, Wire Fraud, Computer Hacking, Money Laundering',
'2023-11-08',
'The Spider, J. Smith, Red Jane, Digital Ghost',
'2019-02-14: Credit Card Fraud (3 years probation)
2021-06-19: Identity Theft (5 years prison - paroled)
2023-11-08: Wire Fraud and Hacking (WANTED)');

-- Suspect 3: Marcus "Blaze" Rodriguez
INSERT INTO suspects (id, name, mugshot_path, charges, date_of_crime, aliases, arrest_history) VALUES
(3, 'Marcus "Blaze" Rodriguez', 'suspects_images/suspect3.jpg',
'Arson, Drug Trafficking, Possession of Illegal Firearms',
'2024-01-20',
'Blaze, M-Rod, Fire Starter, El Fuego',
'2018-09-10: Drug Possession (1 year jail)
2020-12-05: Arson (3 years prison)
2022-08-15: Weapons Violation (2 years probation)
2024-01-20: Drug Trafficking (WANTED)');

-- Suspect 4: Sarah "Ice Queen" Chen
INSERT INTO suspects (id, name, mugshot_path, charges, date_of_crime, aliases, arrest_history) VALUES
(4, 'Sarah "Ice Queen" Chen', 'suspects_images/suspect4.jpg',
'Embezzlement, Corporate Espionage, Bribery',
'2023-09-30',
'Ice Queen, S. Chen, The Accountant, Diamond Sarah',
'2017-04-20: Tax Evasion (5 years probation)
2019-11-12: Corporate Fraud (3 years prison - paroled)
2023-09-30: Embezzlement (WANTED)');

-- Suspect 5: Tommy "Wheels" Harper
INSERT INTO suspects (id, name, mugshot_path, charges, date_of_crime, aliases, arrest_history) VALUES
(5, 'Tommy "Wheels" Harper', 'suspects_images/suspect5.jpg',
'Car Theft Ring Leader, Illegal Street Racing, Reckless Endangerment',
'2024-02-14',
'Wheels, T-Bone, Fast Tommy, The Driver',
'2016-07-08: Street Racing (1 year probation)
2018-03-22: Grand Theft Auto (2 years jail)
2021-10-15: Chop Shop Operation (4 years prison - paroled)
2024-02-14: Car Theft Ring (WANTED)');

-- ============================================
-- Sample Match History
-- ============================================
INSERT INTO match_history (suspect_id, confidence_score, matched_at) VALUES
(1, 225, '2026-01-15 14:23:10'),
(2, 198, '2026-01-16 09:45:33'),
(1, 235, '2026-01-17 16:12:05');

-- ============================================
-- Useful Queries
-- ============================================

-- View all suspects
-- SELECT * FROM suspects;

-- View match history with suspect names
-- SELECT mh.id, s.name, mh.confidence_score, mh.matched_at 
-- FROM match_history mh 
-- JOIN suspects s ON mh.suspect_id = s.id 
-- ORDER BY mh.matched_at DESC;

-- Get suspect with latest match
-- SELECT s.*, mh.confidence_score, mh.matched_at 
-- FROM suspects s 
-- LEFT JOIN match_history mh ON s.id = mh.suspect_id 
-- WHERE s.id = 1 
-- ORDER BY mh.matched_at DESC 
-- LIMIT 1;

-- ============================================
-- GSR Sessions - Polygraph History
-- Stores per-session GSR baseline and readings for a suspect
-- ============================================
CREATE TABLE IF NOT EXISTS gsr_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    suspect_id INT NOT NULL,
    baseline INT,
    peak INT,
    readings_json LONGTEXT, -- JSON array of readings for the session
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP NULL,
    FOREIGN KEY (suspect_id) REFERENCES suspects(id) ON DELETE CASCADE
);

-- Optional: add instantaneous GSR value to match_history at match time
-- Uncomment to enable if desired
-- ALTER TABLE match_history ADD COLUMN gsr_reading INT;
