
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=user_service.settings 

EXPOSE 50051

CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput &sudod & python -m user_service.server"]
