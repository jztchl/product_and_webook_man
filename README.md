
# Product Import API with Background Processing

A high-performance FastAPI application for importing and managing product data with background processing using Celery and Redis.

## Features

- **CSV Import**: Upload and process large CSV files asynchronously  
- **Real-time Progress Tracking**: Monitor import progress with server-sent events (SSE)  
- **Webhook Support**: Configure webhooks for product-related events  
- **Webhook Testing**: Validate a webhook instantly from the UI or API  
- **Webhook Toggle**: Enable or disable any webhook  
- **RESTful API**: Full CRUD operations for products  
- **Background Processing**: Long-running tasks handled by Celery workers  
- **Docker Support**: Easy containerization with Docker and Docker Compose  

## Tech Stack

- **Backend**: Python 3.12, FastAPI  
- **Task Queue**: Celery with Redis as broker and result backend  
- **Database**: PostgreSQL  
- **Caching / Queueing**: Redis  
- **Containerization**: Docker, Docker Compose  

## Prerequisites

- Docker and Docker Compose  
- Python 3.12+  
- Redis  
- PostgreSQL  

---

## Getting Started

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd assignment
````

### 2. Environment Variables (.env)

```env
# PostgreSQL
DATABASE_URL=postgresql://user:password@postgres:5432/dbname

# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2
```

### 3. Start Docker Services

```bash
docker-compose up --build
```

### 4. API Access

* Swagger Docs → [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

# API Endpoints

## 🛒 **Products**

### List Products

`GET /products/list`

### Create Product

`POST /products/create`

### Get Product

`GET /products/get/{product_id}`

### Update Product

`PUT /products/update/{product_id}`

### Toggle Active Status

`POST /products/set_status/{product_id}`
Body:

```json
{ "status": true }
```

### Delete Single

`DELETE /products/delete/{product_id}`

### Delete All

`DELETE /products/delete/delete_all?msg=delete all products`

---

# 📦 CSV Upload

### Upload CSV

`POST /upload`
Example:

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@products.csv;type=text/csv"
```

### Import Progress (SSE)

`GET /stream/progress/{task_id}`

---

# 🔔 Webhooks

Your application supports full webhook lifecycle:

* Create webhook
* List webhook
* Test webhook
* Toggle webhook (active / inactive)
* Delete webhook
* Automatically invoked by product events

## Supported Webhook Events

```
product_created
product_updated
product_deleted
product_deleted_all
product_imported
```

---

## 📌 Webhook Endpoints

### Create Webhook

`POST /webhooks/create`
Body:

```json
{
  "url": "https://webhook.site/123",
  "event_type": "product_created",
  "active": true
}
```

---

### List Webhooks

`GET /webhooks/list`

---

### Get a Webhook

`GET /webhooks/get/{webhook_id}`

---

### Update Webhook

`PUT /webhooks/update/{webhook_id}`
Body supports partial updates.

---

### Delete Webhook

`DELETE /webhooks/delete/{webhook_id}`

---

### ✔ Test Webhook (Send test POST request)

`POST /webhooks/test/{webhook_id}`

Returns:

```json
{
  "status": 200,
  "response_time_ms": 123,
  "body": "OK"
}
```

---

### 🔄 Toggle Webhook Active Status

`POST /webhooks/set_status/{webhook_id}`
Body:

```json
{ "status": false }
```

Response:

```json
{ "status": false }
```

---

# Project Structure

```
.
├── routes/
│   ├── products.py
│   ├── upload.py
│   └── webhooks.py
├── workers/
│   ├── celery_app.py
│   └── tasks.py
├── models/
├── schemas/
├── template/index.html      # Frontend dashboard
├── main.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

# Development

Install dependencies:

```bash
pip install -r requirements.txt
```

Run FastAPI server:

```bash
uvicorn main:app --reload
```

Run Celery worker:

```bash
celery -A workers.celery_app worker --loglevel=info
```

---

# Deployment

```bash
docker-compose up -d
```

---
