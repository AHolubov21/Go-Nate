import sqlite3

def initialize_database():
    conn = sqlite3.connect('nathan.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            timestamp DATETIME,
            priority TEXT,
            escalation_message TEXT
        );
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
