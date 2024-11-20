### Как запустить 
```
cоздать .env и ввести данные для полей как в .env-example
docker compose up -- build
poetry install
alembic upgrade head
uvicorn src.main:app --reload
http://127.0.0.1:8000/docs/
```