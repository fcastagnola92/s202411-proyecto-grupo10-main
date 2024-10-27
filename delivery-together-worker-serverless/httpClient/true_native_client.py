import requests
import http
from config import Config

env = Config()


def get_card_by_ruv(ruv):
    try:
        print(ruv)
        headers = {
            "Authorization": f"Bearer {env.TRUENATIVE_SECRET_TOKEN}"
        }

        response = requests.get(f'{env.TRUENATIVE_BASE_URL}/native/cards/{ruv}', headers=headers)
        
        if response.status_code == http.HTTPStatus.OK:
            return response.json()
        elif response.status_code == http.HTTPStatus.ACCEPTED:
            print("Request accepted the process is still pending")
        else:
            print("Error:", response.status_code)
        return None
    except requests.exceptions.RequestException as e:
        # Handle any connection errors
        print("Error:", e)
        return None