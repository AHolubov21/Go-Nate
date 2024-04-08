#bot/nathan_bot.py

import logging
import asyncio
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.errors import SlackApiError

class NathanBot:
    def __init__(self, config, alert_handler):
        self.config = config
        self.alert_handler = alert_handler
        self.app_token = self.config.get_app_token()
        self.web_client = AsyncWebClient(token=self.config.get_bot_token())
        self.bot_user_id = self.config.get_bot_user_id()  # Bot's user ID
        self.processed_alerts = set()  # To prevent double posting
        logging.info("NathanBot initialized with config and alert_handler.")

    async def process(self, client: SocketModeClient, req: SocketModeRequest):
        logging.info("Processing new request.")
        try:
            if req.type == "events_api":
                data = req.payload.get('event', {})
                channel = data.get('channel')
                text = data.get('text', '')
                user = data.get('user', '')
                ts = data.get('ts')

                if user == self.bot_user_id:
                    logging.debug("Message from bot itself, ignoring to prevent loops.")
                    return

                logging.info(f"Received message: {text} in channel {channel} from user {user}")
                if self.alert_handler.is_alert(text, user) and ts not in self.processed_alerts:
                    logging.info(f"Alert detected: {text}")
                    logging.info("Processing alert...")
                    priority, escalation_message = await self.alert_handler.process_alert(channel, text, user, ts)
                    logging.info("Finished processing alert.")
                    if priority:
                        reaction = self.get_reaction_for_priority(priority)
                        await self.add_reaction_if_not_present(channel, ts, reaction)
                        if escalation_message:
                            await self.send_message(channel, ts, escalation_message)
                            logging.info(f"Sent escalation message to channel '{channel}' in a thread")
                        self.processed_alerts.add(ts)  # Mark the alert as processed
                else:
                    logging.debug("Message is not an alert or has already been processed.")
        except Exception as e:
            logging.exception("Exception occurred during processing Slack event:", exc_info=True)

    async def add_reaction_if_not_present(self, channel, ts, reaction):
        try:
            message_reactions = await self.web_client.reactions_get(channel=channel, timestamp=ts)
            reactions = [r['name'] for r in message_reactions.get('message', {}).get('reactions', [])]
            if reaction not in reactions and ts not in self.processed_alerts:
                await self.web_client.reactions_add(channel=channel, timestamp=ts, name=reaction)
                logging.info(f"Added reaction '{reaction}' to message in channel '{channel}'")
                self.processed_alerts.add(ts)  # Mark the alert as processed
        except SlackApiError as e:
            if e.response["error"] != "already_reacted":
                raise

    async def send_message(self, channel, ts, message):
        if ts not in self.processed_alerts:
            await self.web_client.chat_postMessage(
                channel=channel,
                thread_ts=ts,
                text=message
            )
            self.processed_alerts.add(ts)  # Mark the alert as processed

    async def start(self):
        logging.info("Starting NATHAN bot...")
        try:
            await self.web_client.start()  
            logging.info("NATHAN bot connected to Slack and listening for events.")

            # Replace the event handling loop
            async for event in self.web_client.iter_events():
                if event.get('type') == 'message':
                    await self.process_message(event)  

        except Exception as e:
            logging.error(f"An error occurred during bot startup: {e}", exc_info=True)
        finally:
            logging.info("NATHAN bot disconnected.")

    def get_reaction_for_priority(self, priority: str) -> str:
        priority_reactions = {
            'PU': 'question',
            'P4': 'white_check_mark',
            'P3': 'eyes',
            'P2': 'exclamation',
            'P1': 'fire'
        }
        return priority_reactions.get(priority, 'grey_question')