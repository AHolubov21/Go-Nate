# bot/alert_handler.py

import logging
from bot.config import Config
from bot.database import Database
from bot.utils import generate_response
from slack_sdk.errors import SlackApiError
from typing import Tuple
from datetime import datetime
import asyncio
import re

class AlertHandler:
    def __init__(self, config: Config, database: Database, bot_user_id: str):
        self.config = config
        self.database = database
        self.bot_user_id = bot_user_id
        self.processed_alerts = set()
        self.alerts_waiting_for_resolution = {}
        logging.debug("AlertHandler instance created.")

    def is_alert(self, message: str, user_id: str) -> bool:
        if user_id == self.bot_user_id:
            return False
        return any(keyword.lower() in message.lower() for keyword in self.config.get_alert_keywords())

    async def get_priority(self, alert_message: str) -> str:
        # Load runbook content
        with open(self.config.get_runbook_path(), 'r') as file:
            runbook_content = file.read()

        priority_prompt = f"Alert: '{alert_message}'.\nWhat is the priority according to the runbook? The answer must contain only the error code P1, P2, P3, P4, or PU.\n\nRunbook:\n{runbook_content}"
        try:
            response = await generate_response(
                prompt=priority_prompt,
                model_name=self.config.get_ollama_model_name(),
                api_url=self.config.get_ollama_endpoint(),
                timeout=15  # Timeout of 15 seconds
            )
            match = re.search(r'\b(P1|P2|P3|P4|PU)\b', response)
            priority = match.group(0) if match else 'PU'
            logging.info(f"Extracted priority from LLM API response: {priority}")
            return priority

        except asyncio.TimeoutError:
            logging.error(f"LLM request for priority timed out after 15 seconds.")
            return "PU"  # Fallback priority

        except Exception as e:  # Catch broader potential errors
            logging.error(f"Error getting priority from LLM: {e}", exc_info=True)
            return "PU"  # Fallback   

    async def get_escalation_message(self, alert_message: str, priority: str) -> str:
        # Load runbook content
        with open(self.config.get_runbook_path(), 'r') as file:
            runbook_content = file.read()

        escalation_prompt = f"Alert: '{alert_message}' with priority '{priority}'.\nWhat is the escalation message according to the runbook?\n\nRunbook:\n{runbook_content}"
        try:
            escalation_message = await generate_response(
                prompt=escalation_prompt,
                model_name=self.config.get_ollama_model_name(),
                api_url=self.config.get_ollama_endpoint(),
                timeout=15 
            )
            logging.info(f"LLM API response for escalation message: {escalation_message}")
            return escalation_message.strip()

        except asyncio.TimeoutError:
            logging.error(f"LLM request for escalation message timed out after 15 seconds.")
            return "Failed to generate escalation message"  # Fallback

        except Exception as e:
            logging.error(f"Error getting escalation message from LLM: {e}", exc_info=True)
            return "Failed to generate escalation message"  # Fallback   

    async def wait_for_resolution(self, alert_id: str, alert_message: str, priority: str):
        resolution_time = self.config.get_alert_resolution_time().get(priority, 0) * 60
        await asyncio.sleep(resolution_time)

        if alert_id not in self.alerts_waiting_for_resolution:
            return

        escalation_message = await self.get_escalation_message(alert_message, priority)
        await self.send_escalation_to_slack(alert_id, escalation_message)
        del self.alerts_waiting_for_resolution[alert_id]

    async def process_alert(self, channel: str, text: str, user: str, ts: str) -> Tuple[str, str]:
        logging.info(f"Attempting to process alert: '{text}' from user '{user}' in channel '{channel}'")
        if ts not in self.processed_alerts:
            if self.is_alert(text, user):
                timestamp = datetime.now().isoformat()
                priority = await self.get_priority(text)

                self.database.log_alert(text, timestamp, priority, "")
                self.processed_alerts.add(ts)

                if priority in ['P2', 'P3']:
                    self.alerts_waiting_for_resolution[ts] = timestamp
                    asyncio.create_task(self.wait_for_resolution(ts, text, priority))
                    return priority, "Waiting for resolution"

                escalation_message = await self.get_escalation_message(text, priority)
                self.database.update_escalation_message(text, escalation_message)
                return priority, escalation_message

        logging.info(f"Alert '{text}' is not new or not recognized as an alert.")
        return None, None

    async def send_escalation_to_slack(self, alert_id: str, escalation_message: str):
        try:
            response = await self.config.web_client.chat_postMessage(
                channel=self.config.get_alert_channel(),
                text=escalation_message
            )
            logging.info(f"Sent escalation message to Slack channel: {response['channel']}")
        except SlackApiError as e:
            logging.error(f"Failed to send escalation message to Slack: {e}", exc_info=True)


    def resolve_alert(self, alert_id: str):
        if alert_id in self.alerts_waiting_for_resolution:
            del self.alerts_waiting_for_resolution[alert_id]

