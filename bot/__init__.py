# bot/__init__.py
from .config import Config
from .database import Database
from .alert_handler import AlertHandler
from .nathan_bot import NathanBot

# Initialize configuration
config = Config()

# Create a database instance
database = Database(config.get_database_url())

# Initialize the alert handler with the bot_user_id
alert_handler = AlertHandler(config, database, config.get_bot_user_id())

# Initialize the bot
bot = NathanBot(config, alert_handler)
