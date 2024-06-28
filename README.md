### Автогенерация миграций с помощью Alembic, SQLAlchemy

Создание БД:

```
docker run -d \
  --name testpostgres \
  -p 5432:5432 \
  -v $HOME/postgresql/data2:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=postgres  \
  postgres:13
```

Как начать пользоваться alembic.

1. Установка пакета

```poetry add alembic```

2. Инициализация Alembic

```
alembic init alembic
or
alembic init -t async alembic (асинхронная поддержка)
```

Будут созданы след файлы:

- alembic/env.py
- alembic/script.py.mako
- alembic/versions
- alembic.ini

3. В alembic/env.py необходимо внести правки (пример для Sync Alembic):

- Добавить импорт моделей
  ```import src.db.models```
- Импорт Base
  ```from src.db.postgres import Base```
- Импортируем settings, понадобится строка подключения к БД
```from src.core.config import settings```
- Заменяем 
```
target_metadata = None
на
target_metadata = Base.metadata
```
- Фрмируем строку подключения к БД

```sync_url = f"postgresql://{settings.db_dsn}"```

- Убираем поиск строки из конфигурационного файла
```# url = config.get_main_option("sqlalchemy.url")```

- Заменяем в run_migrations_offline() url на наше подключение sync_url

- Правим run_migrations_online() на:

```
def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = sync_url
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
```
4. Создаем новую миграцию 

```alembic revision --autogenerate -m "Имя миграции"```

5. Применяем миграцию

```alembic upgrade head```

6. Решить конфликт

```alembic merge heads```

7. Отменить последнюю миграцию

```alembic downgrade -1```