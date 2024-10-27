import json
import base64
from httpClient import get_card_by_ruv, card_client
def sync_verification_state(event, context):
    try:
        print(event["data"])
        decoded_data = base64.b64decode(event["data"])
        print(decoded_data)
        data = json.loads(decoded_data.decode("utf-8"))
        ruv = data['ruv']
        card_result = get_card_by_ruv(ruv)
        if (card_result):
            card_client(card_result)
        else:
            print('There is not any result')
        
        return card_result
    except:
        print('Some error ocurred')
        pass