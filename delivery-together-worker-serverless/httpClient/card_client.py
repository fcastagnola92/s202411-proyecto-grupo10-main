import requests
import http
from config import Config

env = Config()


def update_card(card):
    try:
        headers = {
            "Content-Type": f"application/json"
        }
        data = {
            "ruv": card.ruv,
            "status": card.status
        }
        response = requests.put(f'{env.CARD_BASE_URL}/credit-cards/resolve', headers=headers, json=data)
        
        if response.status_code == http.HTTPStatus.OK:
            print("Data sended")
        else:
            print("Error:", response.status_code)
    except requests.exceptions.RequestException as e:
        # Handle any connection errors
        print("Error:", e)
        raise ValueError('Something was wrong')