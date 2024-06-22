import aiohttp
import asyncio
from typing import Union, List

SMS_API_URL = "https://sms.ru/sms/send"
API_TOKEN = "8AF6EC7A-53C3-80C0-E90B-CA7787E31DC8"
MAX_TRY = 3
API_TIMEOUT = 1

async def send_sms(phone: Union[str, List[str]], mess: Union[str, List[str]]):
    print('отправка смс')
    result = {'status': None, 'data': {}, 'message': None}
    try:
        params = {
            'api_id': API_TOKEN,
            'json': 1
        }
        if isinstance(phone, list) and not isinstance(mess, list):
            params['to'] = ','.join(phone)
            params['msg'] = mess
        elif not isinstance(phone, list) and not isinstance(mess, list):
            params['to'] = phone
            params['msg'] = mess
        elif isinstance(phone, list) and isinstance(mess, list):
            for el, msg in zip(phone, mess):
                params[f'to[{el}]'] = msg

        tr = MAX_TRY
        while tr > 0:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(SMS_API_URL, data=params) as response:
                        response.raise_for_status()
                        content_type = response.headers.get('Content-Type')
                        if content_type and 'application/json' in content_type:
                            result['status'] = 'OK'
                            result['data'] = await response.json()
                        else:
                            result['status'] = 'ERROR'
                            result['message'] = f'Invalid response format: {content_type}'
                            result['response_text'] = await response.text()
                        break
            except aiohttp.ClientError as e:
                result['status'] = 'ERROR'
                result['message'] = str(e)
                tr -= 1
                await asyncio.sleep(API_TIMEOUT)

        if tr == 0:
            result['status'] = 'ERROR'
    except Exception as e:
        print(e)
        result['status'] = 'ERROR'
        result['message'] = str(e)
    return result

