#utils/llama_api.py
#import requests
#import logging
#import asyncio
#from bot.config import Config

#config = Config()
#LLAMA_API_URL = config.get_ollama_endpoint()
#LLAMA_MODEL_NAME = config.get_ollama_model_name()

#async def generate_response(prompt: str, model_name: str = LLAMA_MODEL_NAME) -> str:
#    """Generates a response using the Llama API."""
#    headers = {
#        "Authorization": "Bearer your_llama_api_token"  # Replace 'your_llama_api_token' with your actual token if required
#    }
#    data = {
#        "model": model_name,
#        "prompt": prompt,
#        "stream": False  # Get the response in a single message
#    }
#    logging.debug(f"Sending request to Llama API with prompt: '{prompt}'")
#    try:
#        loop = asyncio.get_event_loop()
#        response = await loop.run_in_executor(
#            None, 
#            lambda: requests.post(f"{LLAMA_API_URL}/api/generate", json=data, headers=headers)
#        )
#        response.raise_for_status()
#        logging.debug(f"Received response from Llama API: {response.json()}")
#        return response.json()["response"]
#    except requests.RequestException as e:
#        logging.error(f"Error calling Llama API: {e}", exc_info=True)
#        return ""

#def get_priority_and_message(alert_text: str) -> tuple[str, str]:
#    """Determines the priority and escalation message for an alert."""
#    priority_prompt = f"{alert_text}\nWhat is the priority code (P1, P2, P3, P4, or PU) of this alert?"
#    priority = asyncio.run(generate_response(priority_prompt))

#    if priority not in ["P1", "P2", "P3", "P4"]:
#        return priority, ""

#    message_prompt = f"{alert_text}\nWhat is the escalation message for this alert?"
#    message = asyncio.run(generate_response(message_prompt))

#    return priority, message
#