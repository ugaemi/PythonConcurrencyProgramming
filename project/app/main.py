from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.book_scraper import NaverBookScraper
from app.models import mongodb
from app.models.book import BookModel

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("./index.html", {"request": request, "title": "콜렉터 북북이"})


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    if not q:
        return templates.TemplateResponse(
            "./index.html",
            {"request": request},
        )
    if await mongodb.engine.find_one(BookModel, BookModel.keyword == q):
        books = await mongodb.engine.find(BookModel, BookModel.keyword == q)
        return templates.TemplateResponse(
            "./index.html",
            {"request": request, "keyword": q, "books": books},
        )
    naver_book_scraper = NaverBookScraper()
    books = await naver_book_scraper.search(q, 10)
    book_models = []
    for book in books:
        book_model = BookModel(
            keyword=q,
            publisher=book["publisher"],
            discount=book["discount"],
            image=book["image"],
        )
        book_models.append(book_model)
    await mongodb.engine.save_all(book_models)
    return templates.TemplateResponse(
        "./index.html",
        {"request": request, "keyword": q, "books": books},
    )


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    mongodb.close()
