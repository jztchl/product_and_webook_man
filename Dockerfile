FROM python:3.12-slim-bookworm

RUN pip install --no-cache-dir uv

WORKDIR /app

ENV TZ=Asia/Kolkata
ENV UV_HTTP_TIMEOUT=120
COPY . .

RUN uv pip install --system --no-cache -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]