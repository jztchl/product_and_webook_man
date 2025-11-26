from fastapi import FastAPI
from routes import products, upload, webhooks, stream
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
app = FastAPI(title="Product Importer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="templates")


app.include_router(products.router)
app.include_router(upload.router)
app.include_router(webhooks.router)
app.include_router(stream.router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})