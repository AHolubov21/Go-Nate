#tesst_logging.py

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.debug("Debug message.")
logging.info("Info message.")
logging.warning("Warning message.")
logging.error("Error message.")
logging.critical("Critical message.")


import logging
import os
import asyncio
import aiohttp
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.web.async_client import AsyncWebClient
from bot.alert_handler import AlertHandler
from bot.config import Config
from bot.database import Database

# Configure logging to output to the console at the DEBUG level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.debug("Debug message: Logging is configured correctly.")

print("Environment Variables:")
print(os.environ)

logging.debug("Starting bot/main.py script execution...")
class NathanBot:
    def __init__(self, config: Config, alert_handler: AlertHandler):
        self.config = config
        self.alert_handler = alert_handler
        self.app_token = self.config.get_app_token()
        logging.debug("NathanBot initialized with config and alert handler.")

    async def process(self, client: SocketModeClient, req: SocketModeRequest):
        logging.debug("Processing new request.")
        try:
            if req.type == "events_api":
                data = req.payload.get('event', {})
                logging.debug(f"Event data received: {data}")
                channel = data.get('channel')
                text = data.get('text', '')
                user = data.get('user', '')
                logging.info(f"Received message: {text} in channel {channel} from user {user}")
                if self.alert_handler.is_alert(text):
                    logging.info(f"Alert detected: {text}")
                    await self.alert_handler.process_alert(channel, text, user)
                else:
                    logging.debug(f"Message is not an alert: {text}")
        except Exception as e:
            logging.exception("Exception occurred during processing Slack event:", exc_info=True)

    async def start(self):
        logging.info("Starting the bot...")
        session = aiohttp.ClientSession()
        try:
            client = SocketModeClient(
                app_token=self.app_token,
                web_client=AsyncWebClient(token=self.config.get_bot_token(), session=session)
            )
            client.socket_mode_request_listeners.append(self.process)
            logging.info("Attempting to connect to Slack...")
            await client.connect()
            logging.info("Connected to Slack. Listening for events...")
            while True:
                await asyncio.sleep(1)
        except Exception as e:
            logging.exception("Exception occurred during bot connection to Slack:", exc_info=True)
        finally:
            logging.info("Closing session...")
            await session.close()
            logging.info("Session closed.")

async def main():
    logging.debug("Inside main function (before bot start)...")
    config = Config()
    database = Database(config.get_database_url())
    alert_handler = AlertHandler(config, database)
    bot = NathanBot(config, alert_handler)
    await bot.start()

if __name__ == "__main__":
    logging.debug("Running main function (before asyncio.run)...")
    asyncio.run(main())
    logging.debug("Script execution completed.")
