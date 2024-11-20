FROM python:3.11

RUN apt-get update && apt-get install -y curl wget

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app


COPY poetry.lock pyproject.toml /app/

RUN poetry install

COPY . /app

