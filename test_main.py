import requests

BASE_URL = "http://localhost:8000"

phone = '+77988623099'

def test_register_user():
    url = f"{BASE_URL}/register/"
    payload = {
        "phone": f"{phone}",
        "name": "Иван",
        "role": "Риелтор"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Registration successful:", response.json())
        return response.json()['code']
    else:
        print("Registration failed:", response.status_code, response.text)

def test_activate_user(code):
    url = f"{BASE_URL}/activate/"
    payload = {
        "phone": f"{phone}",
        "activation_code": f"{code}"  # замените на правильный код активации
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Activation successful:", response.json())
    else:
        print("Activation failed:", response.status_code, response.text)

def test_login_user(code):
    url = f"{BASE_URL}/token"
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

def test_update_user(access_token):
    url = f"{BASE_URL}/update/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "phone": phone,
        "first_name": "Иван",
        "last_name": "Петров"
    }
    files = {
        "avatar": ("test_avatar.jpg", open("test_avatar.jpg", "rb")),
        "licenses": ("test_license.jpg", open("test_license.jpg", "rb"))
    }
    response = requests.put(url, headers=headers, data=data, files=files)
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
        print("Get user info successful:", response.json())
    else:
        print("Get user info failed:", response.status_code, response.text)

if __name__ == "__main__":
    code = test_register_user()
    test_activate_user(code)
    token = test_login_user(code)
    if token:
        test_update_user(token)
        test_get_user_info(token)
        test_reset_password()
        test_get_users(token)
        test_delete_user(token)
