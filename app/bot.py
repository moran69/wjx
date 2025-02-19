import requests
import logging

class TelegramBot:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"

    def send_message(self, message: str) -> bool:
        try:
            url = f"{self.base_url}/sendMessage"
            data = {"chat_id": self.chat_id, "text": message, "parse_mode": "HTML"}
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                logging.info("Telegram message sent successfully")
                return True
            logging.error(f"Failed to send message: {response.status_code}")
            return False
        except Exception as e:
            logging.error(f"Error sending Telegram message: {e}")
            return False
