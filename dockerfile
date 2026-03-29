FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root

COPY . .

RUN poetry install

EXPOSE 9000

CMD ["poetry", "run", "python3", "main.py"]
