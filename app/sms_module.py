import requests
import time
from typing import Union, List

SMS_API_URL = "https://sms.ru/api/send"
API_TOKEN = "8AF6EC7A-53C3-80C0-E90B-CA7787E31DC8"
MAX_TRY = 3
API_TIMEOUT = 1  # seconds

def send_sms(phone: Union[str, List[str]], mess: Union[str, List[str]]):
    print("Sending SMS")
    result = {"status": None, "data": {}, "message": None}
    try:
        url = f"{SMS_API_URL}?api_id={API_TOKEN}"
        if isinstance(phone, list) and not isinstance(mess, list):
            url += f"&to={','.join(phone)}&msg={mess}"
        elif isinstance(phone, str) and not isinstance(mess, list):
            url += f"&to={phone}&msg={mess}"
        elif isinstance(phone, list) and isinstance(mess, list):
            for el, ndx in zip(phone, mess):
                url += f"&to[{el}]={ndx}"
        
        tr = MAX_TRY
        while tr > 0:
            try:
                response = requests.get(f"{url}&json=1")
                response.raise_for_status()
                result["status"] = "OK"
                result["data"] = response.json()
                break
            except requests.RequestException as e:
                result["status"] = "ERROR"
                result["message"] = str(e)
                tr -= 1
                if tr == 0:
                    break
                time.sleep(API_TIMEOUT)
    except Exception as e:
        print(e)
        result["status"] = "ERROR"
        result["message"] = str(e)
    return result
