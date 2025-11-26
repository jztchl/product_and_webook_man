from fastapi import FastAPI
from routes import products, upload, webhooks, stream
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Product Importer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(products.router)
app.include_router(upload.router)
app.include_router(webhooks.router)
app.include_router(stream.router)
