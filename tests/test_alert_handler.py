import unittest
from unittest.mock import patch
from bot.alert_handler import AlertHandler
from models.alert_model import Alert


class TestAlertHandler(unittest.TestCase):
    def setUp(self):
        self.alert_handler = AlertHandler()

    @patch('bot.alert_handler.AlertHandler.process_alert')
    def test_handle_message(self, mock_process_alert):
        # Пример сообщения, которое может быть алертом
        message = {
            "type": "message",
            "channel": "C123456",
            "user": "U123456",
            "text": "[FIRING] High CPU usage on server 'server-01'",
            "ts": "1234567890.123456"
        }
        self.alert_handler.handle_message(message)
        mock_process_alert.assert_called_once()

    @patch('bot.alert_handler.AlertHandler.send_escalation_message')
    @patch('bot.alert_handler.llama_api')
    def test_process_alert(self, mock_llama_api, mock_send_escalation_message):
        alert = Alert(
            text="[FIRING] High CPU usage on server 'server-01'",
            channel="C123456",
            timestamp="1234567890.123456"
        )

        # Предполагаем, что Llama API возвращает приоритет P1 для алерта
        mock_llama_api.get_alert_priority.return_value = "P1"

        self.alert_handler.process_alert(alert)
        mock_send_escalation_message.assert_called_once_with(alert, "P1")

    # Добавьте дополнительные тестовые случаи здесь


if __name__ == '__main__':
    unittest.main()
