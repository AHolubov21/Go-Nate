import unittest
from unittest.mock import patch
from bot.database import Database
from models.alert_model import Alert

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database()

    @patch('bot.database.sqlite3')
    def test_connect(self, mock_sqlite):
        self.database.connect()
        mock_sqlite.connect.assert_called_once_with('alerts.db')

    @patch('bot.database.sqlite3')
    def test_create_table(self, mock_sqlite):
        self.database.create_table()
        mock_sqlite.connect().cursor().execute.assert_called_once_with(
            'CREATE TABLE IF NOT EXISTS alerts (id INTEGER PRIMARY KEY, text TEXT, channel TEXT, timestamp TEXT, priority TEXT)'
        )

    @patch('bot.database.sqlite3')
    def test_insert_alert(self, mock_sqlite):
        alert = Alert(
            text="[FIRING] High CPU usage on server 'server-01'",
            channel="C123456",
            timestamp="1234567890.123456",
            priority="P1"
        )
        self.database.insert_alert(alert)
        mock_sqlite.connect().cursor().execute.assert_called_once_with(
            'INSERT INTO alerts (text, channel, timestamp, priority) VALUES (?, ?, ?, ?)',
            (alert.text, alert.channel, alert.timestamp, alert.priority)
        )



if __name__ == '__main__':
    unittest.main()
