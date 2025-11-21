from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio
from fastapi.responses import JSONResponse
from utils import get_news, get_gadgets, get_summary

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    news_task = asyncio.create_task(get_news())
    gadgets_task = asyncio.create_task(get_gadgets())

    news = await news_task
    gadgets = await gadgets_task
    summary = await get_summary(news)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "news": news,
            "gadgets": gadgets,
            "summary": summary,
        }
    )
# ===== NUEVO ENDPOINT JSON SOLO PARA NOTICIAS =====
@app.get("/api/news-json")
async def news_json():
    news = await get_news()
    return JSONResponse({"news": news})