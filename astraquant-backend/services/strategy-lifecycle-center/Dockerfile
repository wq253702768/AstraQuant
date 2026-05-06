FROM python:3.12-slim

WORKDIR /app

COPY shared/python /shared/python
COPY services/strategy-lifecycle-center/pyproject.toml .
COPY services/strategy-lifecycle-center/app ./app

RUN pip install --no-cache-dir -e /shared/python && pip install --no-cache-dir -e .

EXPOSE 8023

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8023"]
