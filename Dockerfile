FROM python:3.12-alpine:3.20

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "./wheesh/manage.py", "runserver", "0.0.0.0:8000"]