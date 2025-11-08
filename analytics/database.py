"""
Advanced Analytics Database Management
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class Database:
    def __init__(self, db_path: str = "logs/tiktok_analytics.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.setup_database()
        
    def setup_database(self):
        """Initialize database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Accounts table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        last_used DATETIME,
                        total_actions INTEGER DEFAULT 0,
                        success_rate REAL DEFAULT 0,
                        status TEXT DEFAULT 'active',
                        suspicion_score INTEGER DEFAULT 0
                    )
                ''')
                
                # Interactions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS interactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        account_id INTEGER,
                        action_type TEXT NOT NULL,
                        target_user TEXT,
                        success BOOLEAN NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        response_time REAL,
                        details TEXT,
                        FOREIGN KEY (account_id) REFERENCES accounts (id)
                    )
                ''')
                
                # Performance metrics table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS performance_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        account_id INTEGER,
                        date DATE NOT NULL,
                        actions_count INTEGER DEFAULT 0,
                        success_count INTEGER DEFAULT 0,
                        avg_response_time REAL,
                        suspicion_events INTEGER DEFAULT 0,
                        FOREIGN KEY (account_id) REFERENCES accounts (id)
                    )
                ''')
                
                # Safety events table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS safety_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        account_id INTEGER,
                        event_type TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        description TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        resolved BOOLEAN DEFAULT FALSE,
                        FOREIGN KEY (account_id) REFERENCES accounts (id)
                    )
                ''')
                
                conn.commit()
                self.logger.info("Database initialized successfully")
                
        except Exception as e:
            self.logger.error(f"Database setup failed: {e}")
            
    def log_interaction(self, username: str, action_type: str, target_user: str, 
                       success: bool, response_time: float, details: Dict = None):
        """Log an interaction to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get or create account
                account_id = self._get_or_create_account(cursor, username)
                
                # Insert interaction
                cursor.execute('''
                    INSERT INTO interactions 
                    (account_id, action_type, target_user, success, response_time, details)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (account_id, action_type, target_user, success, response_time, 
                      json.dumps(details) if details else None))
                
                # Update account stats
                self._update_account_stats(cursor, account_id, success)
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Interaction logging failed: {e}")
            
    def _get_or_create_account(self, cursor, username: str) -> int:
        """Get account ID or create new account"""
        cursor.execute('SELECT id FROM accounts WHERE username = ?', (username,))
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            cursor.execute(
                'INSERT INTO accounts (username) VALUES (?)', 
                (username,)
            )
            return cursor.lastrowid
            
    def _update_account_stats(self, cursor, account_id: int, success: bool):
        """Update account statistics"""
        # Update last used timestamp
        cursor.execute(
            'UPDATE accounts SET last_used = CURRENT_TIMESTAMP WHERE id = ?',
            (account_id,)
        )
        
        # Update total actions
        cursor.execute(
            'UPDATE accounts SET total_actions = total_actions + 1 WHERE id = ?',
            (account_id,)
        )
        
        # Calculate success rate
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful
            FROM interactions 
            WHERE account_id = ?
        ''', (account_id,))
        
        result = cursor.fetchone()
        if result and result[0] > 0:
            success_rate = (result[1] / result[0]) * 100
            cursor.execute(
                'UPDATE accounts SET success_rate = ? WHERE id = ?',
                (success_rate, account_id)
            )
            
    def log_safety_event(self, username: str, event_type: str, severity: str, 
                        description: str = None):
        """Log safety-related event"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                account_id = self._get_or_create_account(cursor, username)
                
                cursor.execute('''
                    INSERT INTO safety_events 
                    (account_id, event_type, severity, description)
                    VALUES (?, ?, ?, ?)
                ''', (account_id, event_type, severity, description))
                
                # Update suspicion score
                score_increase = {
                    'low': 5,
                    'medium': 15,
                    'high': 30,
                    'critical': 50
                }.get(severity, 10)
                
                cursor.execute('''
                    UPDATE accounts 
                    SET suspicion_score = suspicion_score + ? 
                    WHERE id = ?
                ''', (score_increase, account_id))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Safety event logging failed: {e}")
            
    def get_account_stats(self, username: str) -> Dict:
        """Get comprehensive account statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT 
                        total_actions,
                        success_rate,
                        status,
                        suspicion_score,
                        last_used
                    FROM accounts 
                    WHERE username = ?
                ''', (username,))
                
                result = cursor.fetchone()
                if not result:
                    return {}
                    
                stats = {
                    'total_actions': result[0],
                    'success_rate': result[1],
                    'status': result[2],
                    'suspicion_score': result[3],
                    'last_used': result[4]
                }
                
                # Get recent activity
                cursor.execute('''
                    SELECT 
                        action_type,
                        COUNT(*) as count,
                        AVG(response_time) as avg_time,
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count
                    FROM interactions 
                    WHERE account_id = (SELECT id FROM accounts WHERE username = ?)
                    AND timestamp > datetime('now', '-7 days')
                    GROUP BY action_type
                ''', (username,))
                
                recent_activity = {}
                for row in cursor.fetchall():
                    recent_activity[row[0]] = {
                        'count': row[1],
                        'avg_response_time': row[2],
                        'success_count': row[3]
                    }
                    
                stats['recent_activity'] = recent_activity
                
                return stats
                
        except Exception as e:
            self.logger.error(f"Account stats retrieval failed: {e}")
            return {}
            
    def get_performance_report(self, days: int = 7) -> Dict:
        """Generate performance report for specified period"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Overall statistics
                cursor.execute('''
                    SELECT 
                        COUNT(DISTINCT account_id) as active_accounts,
                        COUNT(*) as total_actions,
                        AVG(CASE WHEN success = 1 THEN 1 ELSE 0 END) * 100 as success_rate,
                        AVG(response_time) as avg_response_time
                    FROM interactions 
                    WHERE timestamp > datetime('now', ?)
                ''', (f'-{days} days',))
                
                overall = cursor.fetchone()
                
                # Account performance ranking
                cursor.execute('''
                    SELECT 
                        a.username,
                        COUNT(i.id) as action_count,
                        SUM(CASE WHEN i.success = 1 THEN 1 ELSE 0 END) as success_count,
                        AVG(i.response_time) as avg_response_time
                    FROM accounts a
                    LEFT JOIN interactions i ON a.id = i.account_id
                    WHERE i.timestamp > datetime('now', ?)
                    GROUP BY a.username
                    ORDER BY success_count DESC
                ''', (f'-{days} days',))
                
                account_performance = []
                for row in cursor.fetchall():
                    account_performance.append({
                        'username': row[0],
                        'action_count': row[1],
                        'success_count': row[2],
                        'success_rate': (row[2] / row[1] * 100) if row[1] > 0 else 0,
                        'avg_response_time': row[3]
                    })
                    
                # Safety events summary
                cursor.execute('''
                    SELECT 
                        severity,
                        COUNT(*) as count
                    FROM safety_events 
                    WHERE timestamp > datetime('now', ?)
                    GROUP BY severity
                ''', (f'-{days} days',))
                
                safety_summary = {}
                for row in cursor.fetchall():
                    safety_summary[row[0]] = row[1]
                    
                return {
                    'overall': {
                        'active_accounts': overall[0],
                        'total_actions': overall[1],
                        'success_rate': overall[2],
                        'avg_response_time': overall[3]
                    },
                    'account_performance': account_performance,
                    'safety_summary': safety_summary,
                    'report_period_days': days
                }
                
        except Exception as e:
            self.logger.error(f"Performance report generation failed: {e}")
            return {}
            
    def close(self):
        """Close database connection"""
        pass  # SQLite handles connection automatically