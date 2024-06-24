Базовый URL
http://37.220.84.232:8000

1. Регистрация пользователя
URL: /register/

Метод: POST

Описание: Регистрирует нового пользователя и отправляет SMS с кодом активации.

Роли: user, realtor, developer, agency

Параметры:

phone (string): Номер телефона пользователя.
first_name (string): Имя пользователя.
last_name (string): Фамилия пользователя.
role (string): Роль пользователя.
Пример запроса:
{
"phone": "+79197777779",
"first_name": "Иван",
"last_name": "Иванов",
"role": "realtor"
}

Пример ответа:
{
"message": "User created successfully",
"code": "123456"
}

2. Активация пользователя
URL: /activate/

Метод: POST

Описание: Активирует пользователя по коду активации.

Параметры:

phone (string): Номер телефона пользователя.
activation_code (string): Код активации, отправленный на телефон.
Пример запроса:
{
"phone": "+79197777779",
"activation_code": "123456"
}

Пример ответа:
{
"message": "User activated successfully"
}

3. Получение токена доступа
URL: /token

Метод: POST

Описание: Получает токен доступа для авторизации.

Параметры:

phone (string): Номер телефона пользователя.
activation_code (string): Код активации.
Пример запроса:
{
"phone": "+79197777779",
"activation_code": "123456"
}

Пример ответа:
{
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
"token_type": "bearer"
}

4. Получение информации о текущем пользователе
URL: /users/me/

Метод: GET

Описание: Получает информацию о текущем авторизованном пользователе.

Заголовок:

Authorization (string): Токен доступа в формате Bearer <token>.
Пример запроса:
GET /users/me/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Пример ответа:
{
"id": 1,
"first_name": "Иван",
"last_name": "Иванов",
"phone": "+79197777779",
"role": "Риелтор",
...
}

5. Обновление данных пользователя
URL: /update/

Метод: PUT

Описание: Обновляет данные пользователя.

Параметры:

phone (string): Номер телефона пользователя (обязательный).
Другие параметры (опциональные): first_name, last_name, middle_name, sex, city, email, user_type, whatsapp, telegram, viber, zoom, prop_city, prop_offer, prop_type, prop_state, about.
Файлы: avatar (файл изображения), licenses (файл изображения).
Пример запроса:
PUT /update/
Content-Type: multipart/form-data
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

phone=+79197777779
first_name=Иван
last_name=Петров
avatar=@/path/to/avatar.jpg
licenses=@/path/to/license.jpg

Пример ответа:
{
"message": "User updated successfully",
"user": {
"id": 1,
"first_name": "Иван",
"last_name": "Петров",
"phone": "+79197777779",
...
}
}

6. Сброс кода активации
URL: /reset/

Метод: POST

Описание: Сбрасывает код активации и отправляет новый код на телефон.

Параметры:

phone (string): Номер телефона пользователя.
Пример запроса:
{
"phone": "+79197777779"
}

Пример ответа:
{
"message": "New activation code set"
}

7. Удаление пользователя
URL: /delete/

Метод: DELETE

Описание: Удаляет пользователя по номеру телефона.

Параметры:

phone (string): Номер телефона пользователя.
Пример запроса:
{
"phone": "+79197777779"
}

Пример ответа:
{
"message": "User deleted successfully"
}

8. Получение списка пользователей
URL: /users/

Метод: GET

Описание: Получает список пользователей с пагинацией.

Параметры:

skip (int): Количество пользователей, которые нужно пропустить (для пагинации).
limit (int): Максимальное количество пользователей, которые нужно вернуть.
Пример запроса:
GET /users/?skip=0&limit=10

Пример ответа:
[
{
"id": 1,
"first_name": "Иван",
"last_name": "Иванов",
"phone": "+79197777779",
"role": "Риелтор",
...
},
...
]