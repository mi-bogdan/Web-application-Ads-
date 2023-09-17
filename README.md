<h2 align="center">API объявлений</h2>


**Ссылки**:
- [VK](https://vk.com/id404101172)


### Описание проекта:
API объявлений - это проект, разработанный с использованием Django REST Framework (DRF) для создания и управления объявлениями. Этот API обеспечивает функционал для создания, чтения, обновления и удаления объявлений, а также возможность просмотра списка всех объявлений и поиска по различным параметрам.

### Инструменты разработки

**Стек:**
- Python >= 3.10
- Django >= 4
- PostgreSQL

## Разработка

##### 1) Клонировать репозиторий

    git clone https://github.com/mi-bogdan/Web-application-Ads-.git

##### 2) Создать виртуальное окружение

    python -m venv venv
    
##### 3) Активировать виртуальное окружение

    venv/Scripts/activate       

##### 4) Устанавливить зависимости:

    pip install -r requirements.txt

##### 6) Выполнить команду для выполнения миграций

    python manage.py migrate
    
##### 8) Создать суперпользователя

    python manage.py createsuperuser
    
##### 9) Запустить сервер

    python manage.py runserver

После этого API объявлений будет доступен по адресу http://localhost:8000/.

## Эндпоинты

Следующие эндпоинты доступны в API объявлений:

- GET /api/v1/ads - Вывод объявлений 
- GET /api/v1/ads/<pk>/ - Вывод подробного объявления
- POST /api/v1/create-ads/ - Создание объявления
- POST /api/v1/comments/ - Добавления комментария к объявлению 
- PUT /api/v1/like/<pk>/ - Создания лайка 
- POST /api/v1/report/ - Отправка жалобы на объявления
- POST /api/v1/add-favorite-ads/ - Добавления в избранное объявление
- POST /api/v1/favorite-ads/ - Вывод избранных объявлений пользователя 
- DELETE /api/v1/delete-favorite/<pk>/ - Удаление изранных объявления
- GET /api/v1/categories/ - Вывод категорий 
- GET /api/v1/ads-categories/<pk>/ - Фильтрация объявлений по категориям


Copyright (c) 2023-present, - Shnyra Bogdan
