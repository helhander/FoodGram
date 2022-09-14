[![foodgram workflow](https://github.com/helhander/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/helhander/foodgram-project-react/actions/workflows/foodgram_workflow.yml)
## Проект YaMDb.
### Описание
Онлайн-сервис и API Foodgram, «Продуктовый помощник». 
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Ссылка на развернутый проект
http://tsg.sytes.net/

### Шаблон env-файла:

```
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
POSTGRES_USER='user'
POSTGRES_PASSWORD='password'
DB_HOST='db'
DB_PORT=5432
ENV_ALLOWED_HOSTS='127.0.0.1,localhost,backend'
```

### Как запустить контейнеры:

Клонировать репозиторий:

```
git clone git@github.com:helhander/foodgram-project-react.git
```

Перейти в папку infra/

```
cd infra/
```

Выполнить команду создания и старта контейнеров:

```
docker-compose up -d
```

Выполнить миграции БД:

```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
```

Добавить superuser, если это необходимо (для проверки - root@yandex.ru:Qwerty123+):

```
docker-compose exec backend python manage.py createsuperuser
```

Загрузить данные в БД из дампа:

```
docker-compose exec backend python manage.py loaddata fixture.json
```

Выгрузить данные из БД:

```
docker-compose exec backend python manage.py dumpdata > fixtures.json
```

Остановить и удалить контейнеры:

```
docker-compose down -v
```
### Автор
Трофимов Никита
