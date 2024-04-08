#models/alert_model.py

import logging
from datetime import datetime

class AlertModel:
    def __init__(self, channel, message, priority, status='unresolved', received_at=None, resolved_at=None):
        self.channel = channel
        self.message = message
        self.priority = priority
        self.status = status
        self.received_at = received_at if received_at else datetime.now()
        self.resolved_at = resolved_at
        logging.debug(f"AlertModel initialized: {self}")

    def __repr__(self):
        return f"<Alert(channel={self.channel}, priority={self.priority}, status={self.status}, received_at={self.received_at}, resolved_at={self.resolved_at})>"

    def log_to_database(self, database):
        try:
            database.log_alert(self.message, self.received_at.isoformat(), self.priority, self.status)
            logging.info(f"Alert logged to database: {self}")
        except Exception as e:
            logging.error(f"Error logging alert to database: {e}", exc_info=True)
