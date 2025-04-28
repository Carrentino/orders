FROM python:3.12

WORKDIR /app

RUN pip install --upgrade pip

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

COPY ./src ./src
COPY ./alembic.ini .

ENV PYTHONPATH=/app

CMD ["poetry", "run", "python", "src/main.py"]
