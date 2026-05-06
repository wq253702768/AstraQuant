FROM python:3.12-slim
WORKDIR /app
COPY shared/python /shared/python
COPY services/backtest-service /app
RUN pip install --no-cache-dir -e /shared/python -e /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]
