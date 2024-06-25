import requests
import json
import websocket
import _thread
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder

BASE_URL = "http://127.0.0.1:8000"

phone = '+7996789610'
phone_r = '7996789611'

def test_register_user():
    url = f"{BASE_URL}/users/register/"
    payload = {
        "phone": f"{phone}",
        "name": "Иван",
        "role": "user"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Registration successful:", response.json())
        return response.json()['code']
    else:
        print("Registration failed:", response.status_code, response.text)

def test_register_realtor():
    url = f"{BASE_URL}/users/register/"
    payload = {
        "phone": f"{phone_r}",
        "name": "Иван",
        "role": "realtor"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Registration successful:", response.json())
        return response.json()['code']
    else:
        print("Registration failed:", response.status_code, response.text)        

def test_activate_user(code):
    url = f"{BASE_URL}/users/activate/"
    payload = {
        "phone": f"{phone}",
        "activation_code": f"{code}"  # замените на правильный код активации
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Activation successful:", response.json())
    else:
        print("Activation failed:", response.status_code, response.text)

def test_login_user(code, phone):
    url = f"{BASE_URL}/users/token"
    payload = {
        "phone": phone,
        "activation_code": code
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Login successful:", response.json())
        return response.json()["access_token"]
    else:
        print("Login failed:", response.status_code, response.text)
        return None

def test_update_user1(access_token):
    url = f"{BASE_URL}/users/update/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    # data = {
    #     "phone": phone,
    #     "first_name": "Иван",
    #     "last_name": "Петров"
    # }
    # files = {
    #     "avatar": ("test_avatar.jpg", open("test_avatar.jpg", "rb")),
    #     "licenses": ("test_license.jpg", open("test_license.jpg", "rb"))
    # }
    # response = requests.put(url, headers=headers, data=data, files=files)
    # if response.status_code == 200:
    #     print("Update successful:", response.json())
    # else:
    #     print("Update failed:", response.status_code, response.text)

    data = {
        "phone": phone,
        "first_name": "Иван",
        "last_name": "Петров",
        "middle_name": "Иванович",
        "sex": "M",
        "city": "Москва",
        "email": "ivan.petrov@example.com",
        "user_type": "user",
        "whatsapp": "+79197777777",
        "telegram": "@ivanpetrov",
        "viber": "+79197777777",
        "zoom": "ivan.petrov.zoom",
        "prop_city": "Москва",
        "prop_offer": "Продажа",
        "prop_type": "Квартира",
        "prop_state": "Новая",
        "about": "Описание",
        "notifications_all_messages": True,
        "notifications_new_matches": True,
        "notifications_responses": True,
        "notifications_contacts": True,
        "notifications_news": False
    }
    files = {
        "avatar": ("avatar.jpg", open("test_avatar.jpg", "rb"), "image/jpeg"),
        "licenses": ("licenses.jpg", open("test_license.jpg", "rb"), "image/jpeg")
    }
    response = requests.put(url, headers=headers, data=data, files=files)
    
    print(response.status_code, response.json())
    if response.status_code == 200:
        print("Update successful:", response.json())
    else:
        print("Update failed:", response.status_code, response.text)


def test_update_user2(access_token):
    url = f"{BASE_URL}/users/update/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    # data = {
    #     "phone": phone,
    #     "first_name": "Иван",
    #     "last_name": "Петров"
    # }
    # files = {
    #     "avatar": ("test_avatar.jpg", open("test_avatar.jpg", "rb")),
    #     "licenses": ("test_license.jpg", open("test_license.jpg", "rb"))
    # }
    # response = requests.put(url, headers=headers, data=data, files=files)
    # if response.status_code == 200:
    #     print("Update successful:", response.json())
    # else:
    #     print("Update failed:", response.status_code, response.text)

    data = {
        "phone": phone,
        "notifications_news": True
    }

    response = requests.put(url, headers=headers, data=data)
    
    print(response.status_code, response.json())
    if response.status_code == 200:
        print("Update successful:", response.json())
    else:
        print("Update failed:", response.status_code, response.text)

def test_reset_password():
    url = f"{BASE_URL}/reset/"
    payload = {
        "phone": f"{phone}"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Password reset successful:", response.json())
    else:
        print("Password reset failed:", response.status_code, response.text)

def test_delete_user(access_token):
    url = f"{BASE_URL}/delete/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "phone": f"{phone}"
    }
    response = requests.delete(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("User deletion successful:", response.json())
    else:
        print("User deletion failed:", response.status_code, response.text)

def test_get_users(access_token):
    url = f"{BASE_URL}/users/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "skip": 0,
        "limit": 10
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print("Get users successful:", response.json())
    else:
        print("Get users failed:", response.status_code, response.text)

def test_get_user_info(access_token):
    url = f"{BASE_URL}/users/me/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
        print("Get user info successful:", response.json())
    else:
        print("Get user info failed:", response.status_code, response.text)


def test_create_property(access_token):
    url = f"{BASE_URL}/properties/create"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    multipart_data = MultipartEncoder(
        fields={
            "deal_format": "sale",
            "type": "apartment",
            "subtype": "studio",
            "condition": "new",
            "entry_year": "2024",
            "entry_quarter": "2",
            "purpose": "residence",
            "location": "123 Main St, Anytown",
            "price": "150000",
            "currency": "USD",
            "title": "Beautiful Studio Apartment",
            "description": "A beautiful new studio apartment located in the heart of the city.",
            "floor": "3",
            "total_area": "45.5",
            "living_area": "40",
            "ceiling_height": "3",
            "rooms": "1",
            "bedrooms": "1",
            "bathrooms": "1",
            "features": "kitchen,balcony",
            "equipment": "furniture,appliances",
            "building_floors": "10",
            "building_living_area": "4000",
            "apartments": "50",
            "lifts_per_entrance": "2",
            "building_features": "parking,pool",
            "building_name": "Luxury Residences",
            "developer": "Top Developer",
            "materials": "brick",
            "territory_area": "2000",
            "territory_features": "garden,gym",
            "nearby_places": "beach,park",
            "views": "sea view,city view",
            "video_title": "Apartment Tour",
            "video_url": "http://example.com/tour",
            "services": "remote deal,crypto payment",
            "commission_amount": "5",
            "commission_type": "% of deal",
            "documents": "title deed,purchase contract",
            "images": ("layout1.jpg", open("test_building_layout.jpg", "rb"), "image/jpeg"),
            "images": ("layout2.jpg", open("test_layout.jpg", "rb"), "image/jpeg"),
            "document_file1": ("doc1.pdf", open("doc1.pdf", "rb"), "application/pdf"),
            "document_file2": ("doc2.pdf", open("doc2.pdf", "rb"), "application/pdf"),

        }
    )
    
    headers['Content-Type'] = multipart_data.content_type

    response = requests.post(url, headers=headers, data=multipart_data)
    if response.status_code == 200:
        print("Property creation successful:", response.json())
    else:
        print("Property creation failed:", response.status_code, response.text)


def test_create_request(access_token):
    url = f"{BASE_URL}/users/create_request"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "city": "Москва",
        "district": "Центральный",
        "deal_format": "хочу купить",
        "type": "квартира",
        "subtype": "апартаменты",
        "condition": "новая",
        "construction_year": 2023,
        "construction_quarter": 4,
        "total_rooms": "2",
        "total_area_min": 50,
        "total_area_max": 70,
        "budget_min": 10000000,
        "budget_max": 15000000,
        "currency": "RUB",
        "purchase_purpose": "для проживания",
        "urgency": "срочно",
        "purchase_method": "в ипотеку",
        "mortgage_approved": True,
        "wishes": "хорошая инфраструктура"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Request creation successful:", response.json())
    else:
        print("Request creation failed:", response.status_code, response.text)

def test_get_my_requests(access_token):
    url = f"{BASE_URL}/users/my_requests"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Get my requests successful:", response.json())
    else:
        print("Get my requests failed:", response.status_code, response.text)


def test_get_prop(token):
    url = f"{BASE_URL}/properties/my_properties/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Get user info successful:", response.json())
    else:
        print("Get user info failed:", response.status_code, response.text)    


def test_create_chat(token, buyer_id, seller_id):
    url = f"{BASE_URL}/chat/create_chat"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "buyer_id": buyer_id,
        "seller_id": seller_id,
        "property_id": 1
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
    if response.status_code == 200:
        return response.json()
    else:
        print("Get user info failed:", response.status_code, response.text)   

def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send(f"Hello {i}")
        time.sleep(1)
        ws.close()
    _thread.start_new_thread(run, ())

def test_websocket_chat(chat_id, token):
    ws = websocket.WebSocketApp(f"ws://localhost:8000/chat/ws/{chat_id}?token={token}",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

if __name__ == "__main__":
    code = test_register_user()
    test_activate_user(code)
    token = test_login_user(code, phone)
    user_id = test_get_user_info(token)['id']

    code = test_register_realtor()
    test_activate_user(code)
    token1 = test_login_user(code, phone_r)
    realtor_id = test_get_user_info(token1)['id']
    if token and token1:
        test_create_property(token1)
        chat = test_create_chat(token, user_id, realtor_id)
        print("chat:", chat)
        test_websocket_chat(chat['id'], token)
        # test_create_request(token)
        # test_get_my_requests(token)
        # test_update_user1(token)
        # print("---------------------------------------------")
        # test_update_user2(token)
        # test_get_user_info(token)
        # test_reset_password()
        # test_get_users(token)
        # test_delete_user(token)
