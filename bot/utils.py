# bot/utils.py

import logging
import aiohttp
from aiohttp import ClientSession, ClientTimeout
import asyncio 

logging.info(f"aiohttp version: {aiohttp.__version__}") 

async def generate_response(prompt: str, model_name: str, api_url: str, timeout=15) -> str:
    """
    Generates a response using the LLM with error handling and timeouts.
    """
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }
    logging.debug(f"Sending request to LLM API with prompt: '{prompt}'")
    try:
        async with aiohttp.ClientSession(timeout=ClientTimeout(total=timeout)) as session:  # Correct timeout setup!
            async with session.post(f"{api_url}/api/generate", json=data) as response:
                response_text = await response.text()
                if response.status == 200:
                    json_response = await response.json()
                    logging.debug(f"Received response from LLM API: {json_response}")
                    return json_response.get("response", "").strip()
                else:
                    logging.error(f"LLM API call failed with status {response.status}, response: {response_text}")
                    return "Error generating response from LLM"  # Informative fallback

    except aiohttp.ClientTimeoutError:
        logging.error(f"LLM API request timed out after {timeout} seconds.")
        return "Error generating response from LLM (timeout)"  # Timeout-specific fallback

    except aiohttp.ClientError as e:
        logging.error(f"Exception occurred when calling LLM API: {e}", exc_info=True)
        return "Error generating response from LLM"  # General fallback
    
async def determine_priority_and_escalation(prompt_priority: str, prompt_escalation: str, model_name: str, api_url: str) -> tuple:
    """
    Determines the priority and escalation message for an alert using LLM.
    """
    priority = await generate_response(prompt_priority, model_name, api_url)
    if priority in ["P1", "P2", "P3", "P4"]:
        escalation_message = await generate_response(prompt_escalation, model_name, api_url)
        return priority, escalation_message
    return priority, ""

