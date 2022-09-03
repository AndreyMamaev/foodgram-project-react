# Проект FoodGram

Проект запущен по адресу http://158.160.9.204

Логин администратора: mamaev.andrey@mail.ru
Пароль администратора: admin

![workflow](https://github.com/AndreyMamaev/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Описание

Данный проект представляет собой онлайн-сервис "Продуктовый помошник", в котором реализованы следующие **возможности**:

- Публиковать рецепты.
- Добавлять понравившиеся рецепты в избранное.
- Присваивать рецептам тэги, а также сортировать по ним.
- Подписываться на пользователей.
- Добавлять рецепты в корзину.
- Перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд  из корзины.

## Технлологии

- Django
- Django DRF
- PostgreSQL
- Docker
- Nginx

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```git clone git@github.com:AndreyMamaev/foodgram-project-react.git```

Создать файл .env, в котором необходимо создать переменные:

- DB_ENGINE
- DB_NAME
- POSTGRES_USER
- POSTGRES_PASSWORD
- DB_HOST
- DB_PORT
- SECRET_KEY
- HOST

```cd infra```

Cоздать образ и контейнеры:

```docker-compose up```

```docker-compose exec web python manage.py migrate```

```docker-compose exec web python manage.py collectstatic --no-input```

Наполнить базу данными из файла с фикстурами:

```docker-compose exec web python manage.py loaddata fixtures.json```

## Примеры запросов к API

Запросы к API начинаются с ```/api/```

1. Получить список всех рецептов:

Запрос:
GET ```/api/recipes/```

Ответ:
```
[
    {
        "count": 0, # Количество объектов
        "next": "string", # Следующая страница
        "previous": "string", # Предыдущая страница
        "results": [] # Рецепты
    }
]
```

2. Получение информации о конкретном рецепте:

Запрос:
GET ```/api/recipes/{recipe_id}/```

Ответ:
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

3. Добавление нового произведения:

Запрос:
POST ```/api/recipes/```
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

Ответ:
Аналогично запросу GET ```/api/recipes/{recipe_id}/```

## Документация представлена [здесь](http://158.160.9.204/api/docs/)

## Авторы:

Андрей Мамаев
