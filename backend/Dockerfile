FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt
COPY .env .
COPY alembic.ini .
COPY app app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
