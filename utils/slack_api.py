#utils/slack_api.py

from slack_sdk.errors import SlackApiError

def is_alert(message: str, alert_keywords=None) -> bool:
    """Проверяет, является ли сообщение алертом."""
    if alert_keywords is None:
        alert_keywords = ["[FIRING]", "CloudWatch Alarm", "Problem", "Alert"]
    return any(keyword in message for keyword in alert_keywords)

def extract_priority(message: str) -> str:
    """Извлекает приоритет алерта из сообщения."""
    if "[P1]" in message:
        return "P1"
    elif "[P2]" in message:
        return "P2"
    elif "[P3]" in message:
        return "P3"
    elif "[P4]" in message:
        return "P4"
    else:
        return "PU"

def send_message_to_thread(client, channel: str, thread_ts: str, message: str):
    """Отправляет сообщение в тред Slack, используя WebClient."""
    try:
        response = client.chat_postMessage(
            channel=channel,
            thread_ts=thread_ts,
            text=message
        )
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")

def add_reaction_to_message(client, channel: str, timestamp: str, reaction: str):
    """Добавляет реакцию к сообщению в Slack, используя WebClient."""
    try:
        response = client.reactions_add(
            channel=channel,
            timestamp=timestamp,
            name=reaction
        )
    except SlackApiError as e:
        print(f"Error adding reaction to Slack message: {e.response['error']}")
