FROM python:3.12-slim
WORKDIR /app
COPY shared/python /shared/python
COPY services/audit-center-service /app
RUN pip install --no-cache-dir -e /shared/python -e /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8022"]
