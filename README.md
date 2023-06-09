# Django Friends Service
## Описание

Данный проект представляет собой REST API сервис для сохранения информации об 
отношениях между пользователями. 

Сервис позволяет:
- зарегистрировать нового пользователя
- отправить одному пользователю заявку в друзья другому
- принять/отклонить пользователю заявку в друзья от другого пользователя
- посмотреть пользователю список своих исходящих и входящих заявок в друзья
- посмотреть пользователю список своих друзей
- получить пользователю статус дружбы с каким-то другим пользователем (нет ничего / есть
исходящая заявка / есть входящая заявка / уже друзья)
- удалить пользователю другого пользователя из своих друзей

Проект реализован на [Django Rest Framework](https://www.django-rest-framework.org/).

OpenAPI спецификация проекта [Specification](https://github.com/Andrew-Goncharov/django-friends-service/blob/main/backend/openapi-schema.yml).

## Инструкция

Для запуска проекта необходимо выполнить несколько шагов:

1. Клонировать репозиторий:

    `git clone https://github.com/Andrew-Goncharov/django-friends-service.git`

2. Создать виртуальное окружение:

    `python -m venv venv`

3. Активировать виртуальное окружение:

    Для Linux - `source /venv/bin/activate`

    Для Windows - `.\venv\Scripts\activate`

4. Установить зависимости:
    
    `pip install -r requirements.txt`

5. Применить миграции:
    
    `cd backend`
    
    `python manage.py migrate`
    
6. Создать суперпользователя для доступа к админ панели:

    `python manage.py createsuperuser`

7. Теперь можно запустить проект:

    `python manage.py runserver`


## Примеры отправки запросов
### Создание нового пользователя

    curl --location 'http://127.0.0.1:8000/create_user/' \
    --header 'Content-Type: application/json' \
    --data '{
        "id": "c70415b1-22f2-485f-af12-e8acb4fe0739",
        "username": "Sergey2"
    }'

### Создание запроса на добавление в друзья

    curl --location 'http://127.0.0.1:8000/create_friendship_request/' \
    --header 'Content-Type: application/json' \
    --data '{
        "sender": "c70415b1-22f2-485f-af12-e8acb4fe0739",
        "receiver": "c70415b1-22f2-485f-af12-e8acb4fe0737"
    }'
    
### Обработка запроса на добавление в друзья

    curl --location 'http://127.0.0.1:8000/process_friendship_request/' \
    --header 'Content-Type: application/json' \
    --data '{
        "sender": "c70415b1-22f2-485f-af12-e8acb4fe0739",
        "receiver": "c70415b1-22f2-485f-af12-e8acb4fe0737",
        "action": "accept"
    }'


### Получения информации о запросах

    curl --location 'http://127.0.0.1:8000/get_friendship_requests/?user_id=15082c23-8fcc-4b35-b323-733256abd350qw'

### Определение статуса

    curl --location 'http://127.0.0.1:8000/get_friendship_status/?user_id_1=0eaa7a28-6aa6-4924-b1a9-6ab82c12e299&user_id_2=c70415b1-22f2-485f-af12-e8acb4fe0737'

### Получение списка друзей
    
    curl --location 'http://127.0.0.1:8000/get_user_friends/?user_id=0eaa7a28-6aa6-4924-b1a9-6ab82c12e299'
    
### Удаление из друзей

    curl --location --request DELETE 'http://127.0.0.1:8000/remove_from_friends/?user_id=0eaa7a28-6aa6-4924-b1a9-6ab82c12e299&friend_id=c70415b1-22f2-485f-af12-e8acb4fe0737'