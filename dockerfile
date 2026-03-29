FROM python:3.14-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install

COPY . .

RUN poetry install

EXPOSE 9000

CMD ["poetry", "run", "python3", "main.py"]
