# bot/main.py

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
import asyncio
from bot.config import Config
from bot.database import Database
from bot.alert_handler import AlertHandler
from bot.nathan_bot import NathanBot

# Set up logging only once, remove duplicate basicConfig calls
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

async def main():
    # Load configuration
    config = Config()
    logging.info("Configuration and database initialization starts...")

    # Initialize database
    database = Database(config.get_database_url())
    logging.info("Database initialized successfully.")

    # Initialize alert handler with bot_user_id
    alert_handler = AlertHandler(config, database, config.get_bot_user_id())
    logging.info("Alert handler initialized successfully.")

    # Initialize and start the bot
    bot = NathanBot(config, alert_handler)
    logging.info("NATHAN bot starting...")
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
