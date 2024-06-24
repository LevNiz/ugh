Базовый URL
http://37.220.84.232:8000

1. Регистрация пользователя
URL: users/register/

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
URL: users/activate/

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
URL: users/token

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
URL: users/me/

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
URL: users/update/

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
URL: users/reset/

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
URL: users/delete/

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
URL: users/list/

Метод: GET

Описание: Получает список пользователей с пагинацией.

Параметры:

skip (int): Количество пользователей, которые нужно пропустить (для пагинации).
limit (int): Максимальное количество пользователей, которые нужно вернуть.
Пример запроса:
GET /list/?skip=0&limit=10

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


9. Создание объекта недвижимости
URL: /properties/create

Метод: POST

Описание: Создает новый объект недвижимости. Доступно только для пользователей с ролями realtor, agency, developer.

Параметры:

deal_format (string): Формат сделки (например, "sale", "rent").
type (string): Тип недвижимости (например, "apartment", "house").
subtype (string): Подтип недвижимости (например, "studio", "penthouse").
condition (string): Состояние недвижимости (например, "new", "resale").
entry_year (int): Год ввода в эксплуатацию.
entry_quarter (int): Квартал ввода в эксплуатацию.
purpose (string): Назначение недвижимости (например, "residence", "investment").
location (string): Адрес недвижимости.
price (float): Цена недвижимости.
currency (string): Валюта цены (например, "USD", "EUR").
title (string): Заголовок объявления.
description (string): Описание недвижимости.
images (list of files): Список изображений недвижимости.
floor (int, optional): Этаж.
total_area (float, optional): Общая площадь.
living_area (float, optional): Жилая площадь.
ceiling_height (float, optional): Высота потолков.
rooms (int, optional): Количество комнат.
bedrooms (int, optional): Количество спален.
bathrooms (int, optional): Количество ванных комнат.
features (string, optional): Особенности (например, "kitchen,balcony").
equipment (string, optional): Оснащение (например, "furniture,appliances").
layout (file, optional): Планировка квартиры.
building_floors (int, optional): Количество этажей в здании.
building_living_area (float, optional): Жилая площадь здания.
apartments (int, optional): Количество квартир в здании.
lifts_per_entrance (int, optional): Количество лифтов на подъезд.
building_features (string, optional): Особенности здания (например, "parking,pool").
building_name (string, optional): Название здания/жилого комплекса.
developer (string, optional): Девелопер.
materials (string, optional): Материалы строительства.
building_layout (file, optional): Планировка здания.
territory_area (float, optional): Площадь территории.
territory_features (string, optional): Особенности территории (например, "garden,gym").
territory_layout (file, optional): Планировка территории.
nearby_places (string, optional): Близлежащие места (например, "beach,park").
views (string, optional): Виды (например, "sea view,city view").
video_title (string, optional): Название видео.
video_url (string, optional): URL видео.
services (string, optional): Услуги (например, "remote deal,crypto payment").
commission_amount (float, optional): Размер комиссии.
commission_type (string, optional): Тип комиссии (например, "% of deal", "fixed").
documents (string, optional): Список документов (например, "title deed,purchase contract").
document_file1 (file, optional): Документ 1.
document_file2 (file, optional): Документ 2.
document_file3 (file, optional): Документ 3.


curl -X POST "{BASE_URL}/properties/create \
-H "Authorization: Bearer your_access_token_here" \
-H "Content-Type: multipart/form-data" \
-F "deal_format=sale" \
-F "type=apartment" \
-F "subtype=studio" \
-F "condition=new" \
-F "entry_year=2024" \
-F "entry_quarter=2" \
-F "purpose=residence" \
-F "location=123 Main St, Anytown" \
-F "price=150000" \
-F "currency=USD" \
-F "title=Beautiful Studio Apartment" \
-F "description=A beautiful new studio apartment located in the heart of the city." \
-F "images=@layout1.jpg" \
-F "images=@layout2.jpg" \
-F "document_file1=@doc1.pdf" \
-F "document_file2=@doc2.pdf" \
-F "document_file3=@doc3.pdf" \
-F "floor=3" \
-F "total_area=45.5" \
-F "living_area=40" \
-F "ceiling_height=3" \
-F "rooms=1" \
-F "bedrooms=1" \
-F "bathrooms=1" \
-F "features=kitchen,balcony" \
-F "equipment=furniture,appliances" \
-F "layout=@layout.jpg" \
-F "building_floors=10" \
-F "building_living_area=4000" \
-F "apartments=50" \
-F "lifts_per_entrance=2" \
-F "building_features=parking,pool" \
-F "building_name=Luxury Residences" \
-F "developer=Top Developer" \
-F "materials=brick" \
-F "building_layout=@building_layout.jpg" \
-F "territory_area=2000" \
-F "territory_features=garden,gym" \
-F "territory_layout=@territory_layout.jpg" \
-F "nearby_places=beach,park" \
-F "views=sea view,city view" \
-F "video_title=Apartment Tour" \
-F "video_url=http://example.com/tour" \
-F "services=remote deal,crypto payment" \
-F "commission_amount=5" \
-F "commission_type=% of deal" \
-F "documents=title deed,purchase contract"


10. Получение списка объектов недвижимости, созданных текущим пользователем
URL: /properties/my_properties/

Метод: GET

Описание: Возвращает список объектов недвижимости, созданных текущим авторизованным пользователем. Доступно только для пользователей с ролью realtor, agency, developer.

Параметры:
Не требуется

Пример запроса:

curl -X GET "{BASE_URL}/properties/my_properties/" \
-H "Authorization: Bearer your_access_token_here"