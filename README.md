Базовый URL
http://localhost:8000

1. Регистрация пользователя

URL: /register/

Метод: POST

Описание: Регистрирует нового пользователя и отправляет SMS с кодом активации и паролем.

Параметры:
- phone (string): Номер телефона пользователя.
- name (string): Имя пользователя.
- role (string): Роль пользователя.

Пример запроса:
{
    "phone": "+79197777777",
    "name": "Иван",
    "role": "Риелтор"
}

Пример ответа:
{
    "message": "User created successfully"
}


2. Активация пользователя

URL: /activate/

Метод: POST

Описание: Активация пользователя с помощью кода, отправленного по SMS.

Параметры:
- phone (string): Номер телефона пользователя.
- activation_code (string): Код активации, отправленный по SMS.

Пример запроса:
{
    "phone": "+79197777777",
    "activation_code": "123456"
}

Пример ответа:
{
    "message": "User activated successfully"
}


3. Вход пользователя

URL: /token

Метод: POST

Описание: Аутентификация пользователя и получение токена доступа.

Параметры:
- username (string): Номер телефона пользователя.
- password (string): Пароль пользователя.

Пример запроса:
username=+79197777777&password=generated_password

Пример ответа:
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}


4. Получение информации о текущем пользователе

URL: /users/me/

Метод: GET

Описание: Получение информации о текущем авторизованном пользователе.

Заголовки:
- Authorization: Токен доступа в формате Bearer <token>.

Пример ответа:
{
    "id": 1,
    "phone": "+79197777777",
    "first_name": "Иван",
    "last_name": "Иванов",
    "role": "Риелтор"
}


5. Обновление информации о пользователе

URL: /update/

Метод: PUT

Описание: Обновление информации о пользователе.

Параметры:
- phone (string): Номер телефона пользователя.
- Остальные поля (опционально): Обновляемые данные пользователя (см. схему UserUpdate).

Пример запроса:
{
    "phone": "+79197777777",
    "first_name": "Иван",
    "last_name": "Петров"
}

Пример ответа:
{
    "message": "User updated successfully"
}


6. Сброс пароля

URL: /reset/

Метод: POST

Описание: Сброс пароля пользователя и отправка нового пароля по SMS.

Параметры:
- phone (string): Номер телефона пользователя.

Пример запроса:
{
    "phone": "+79197777777"
}

Пример ответа:
{
    "message": "Temporary password set"
}


7. Удаление пользователя

URL: /delete/

Метод: DELETE

Описание: Удаление пользователя.

Параметры:
- phone (string): Номер телефона пользователя.

Пример запроса:
{
    "phone": "+79197777777"
}

Пример ответа:
{
    "message": "User deleted successfully"
}


8. Получение списка пользователей

URL: /users/

Метод: GET

Описание: Получение списка пользователей (только для администраторов).

Параметры:
- skip (int, опционально): Пропустить указанное количество пользователей.
- limit (int, опционально): Ограничить количество возвращаемых пользователей.

Пример запроса:
/users/?skip=0&limit=10

Пример ответа:
[
    {
        "id": 1,
        "phone": "+79197777777",
        "first_name": "Иван",
        "last_name": "Иванов",
        "role": "Риелтор"
    },
    {
        "id": 2,
        "phone": "+79263334455",
        "first_name": "Петр",
        "last_name": "Петров",
        "role": "Клиент"
    }
]