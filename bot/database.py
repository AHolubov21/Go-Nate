# bot/database.py

import sqlite3
import logging

class Database:
    def __init__(self, db_path: str):
        logging.debug("Initializing Database class")
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        logging.info(f"Creating database table at: {self.db_path}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS alerts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        message TEXT NOT NULL UNIQUE,
                        timestamp TEXT NOT NULL,
                        priority TEXT NOT NULL,
                        escalation_message TEXT
                    );
                """)
                conn.commit()
                logging.info("Database table created successfully.")
        except sqlite3.DatabaseError as e:
            logging.error(f"Database error during table creation: {e}", exc_info=True)

    def log_alert(self, message: str, timestamp: str, priority: str, escalation_message: str):
        logging.info(f"Logging alert to database with message: '{message}'")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO alerts (message, timestamp, priority, escalation_message)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(message) DO UPDATE SET
                        timestamp = excluded.timestamp,
                        priority = excluded.priority,
                        escalation_message = excluded.escalation_message;
                """, (message, timestamp, priority, escalation_message))
                conn.commit()
                logging.info("Alert logged to database successfully.")
        except sqlite3.IntegrityError:
            logging.error(f"Duplicate alert detected with message: '{message}'")
        except sqlite3.DatabaseError as e:
            logging.error(f"Database error during logging alert: {e}", exc_info=True)

    def update_escalation_message(self, message: str, escalation_message: str):
        logging.info(f"Updating escalation message in database for message: '{message}'")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE alerts
                    SET escalation_message = ?
                    WHERE message = ?;
                """, (escalation_message, message))
                conn.commit()
                logging.info("Escalation message updated successfully in the database.")
        except sqlite3.DatabaseError as e:
            logging.error(f"Database error during escalation message update: {e}", exc_info=True)

