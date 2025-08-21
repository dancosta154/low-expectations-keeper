
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "wsgi:app", "--preload", "--workers=2", "--threads=4", "--bind=0.0.0.0:8080"]
