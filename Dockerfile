FROM python:3.11
LABEL org.opencontainers.image.source https://github.com/bsiebens/todoguardian

WORKDIR /app

COPY pyproject.toml .
RUN python -m pip install poetry
RUN poetry install

COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]