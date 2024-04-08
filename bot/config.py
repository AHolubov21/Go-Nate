# bot/config.py

import json
import logging
from typing import List, Dict

class Config:
    def __init__(self):
        logging.debug("Initializing Config class")
        self.load_config()

    def load_config(self):
        logging.info("Loading configuration from config.json")
        try:
            with open('config.json', 'r') as file:
                config_data = json.load(file)

            self.app_token = config_data.get('slack', {}).get('app_token', '')  
            self.bot_token = config_data.get('slack', {}).get('bot_token', '')  
            self.bot_user_id = config_data.get('slack', {}).get('bot_user_id', '')  
            self.alert_keywords = config_data.get('alert_keywords', [])
            self.alert_resolution_time = config_data.get('escalation_times', {'P2': 15, 'P3': 30})
            self.database_url = config_data.get('database_url', '')
            self.ollama_endpoint = config_data.get('llama', {}).get('api_url', '')
            self.ollama_model_name = config_data.get('llama', {}).get('model_name', '')
            self.ollama_api_token = config_data.get('llama', {}).get('api_token', '')
            self.runbook_path = config_data.get('runbook_path', '')

            self.validate_config()
            logging.info("Configuration loaded successfully.")
        except FileNotFoundError:
            logging.error("Configuration file 'config.json' not found.", exc_info=True)
        except json.JSONDecodeError:
            logging.error("Error parsing 'config.json'. Please ensure it is valid JSON.", exc_info=True)
        except Exception as e:
            logging.error(f"Unexpected error loading configuration: {e}", exc_info=True)

    def validate_config(self):
        if not self.app_token or not self.bot_token:
            logging.warning("Slack tokens are missing or empty in the configuration.")
        if not self.alert_keywords:
            logging.warning("Alert keywords are missing or empty in the configuration.")
        if not self.ollama_endpoint or not self.ollama_model_name or not self.ollama_api_token:
            logging.warning("Llama API endpoint, model name, or API token is missing or empty in the configuration.")
        if not self.runbook_path:
            logging.warning("Runbook path is missing or empty in the configuration.")

    def get_app_token(self) -> str:
        return self.app_token

    def get_bot_token(self) -> str:
        return self.bot_token

    def get_bot_user_id(self) -> str:
        return self.bot_user_id

    def get_alert_keywords(self) -> List[str]:
        return self.alert_keywords

    def get_alert_resolution_time(self) -> Dict[str, int]:
        return self.alert_resolution_time

    def get_database_url(self) -> str:
        return self.database_url

    def get_ollama_endpoint(self) -> str:
        return self.ollama_endpoint

    def get_ollama_model_name(self) -> str:
        return self.ollama_model_name

    def get_ollama_api_token(self) -> str:
        return self.ollama_api_token

    def get_runbook_path(self) -> str:
        return self.runbook_path

    def load_runbook_contents(self) -> str:
        """Load and return the contents of the runbook."""
        try:
            with open(self.runbook_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            logging.error(f"Runbook file '{self.runbook_path}' not found.", exc_info=True)
            return ""
