# Проект FoodGram

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
- SQLite

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```git clone git@github.com:AndreyMamaev/foodgram-project-react.git```

Cоздать и активировать виртуальное окружение:

```python -m venv env```

```venv/scripts/activate```

```python -m pip install --upgrade pip```

Установить зависимости из файла requirements.txt:

```pip install -r requirements.txt```

Выполнить миграции:

```cd backend/```

```python manage.py migrate```

Запустить проект:

```python manage.py runserver```

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

## Авторы:

Андрей Мамаев
