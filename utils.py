import cohere
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_KEY = os.getenv("NEWSAPI_KEY")
PIXABAY_KEY = os.getenv("PIXABAY_KEY")
# ------------------ NEWS API ------------------

async def get_news():
    url = f"https://newsapi.org/v2/top-headlines?category=technology&country=us&pageSize=20&apiKey={NEWS_KEY}"

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            data = resp.json()

            articles = data.get("articles", [])

            return [{
                "title": a.get("title", "Sin título"),
                "url": a.get("url"),
                "source": a.get("source", {}).get("name")
            } for a in articles]

    except Exception as e:
        print("ERROR EN NEWS API:", e)
        return []


# ------------------ FAKE STORE GADGETS ------------------

async def get_gadgets():
    url = "https://fakestoreapi.com/products?limit=15"

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            data = resp.json()

            return [{
                "title": p["title"],
                "price": p.get("price"),
                "category": p.get("category")
            } for p in data]

    except Exception as e:
        print("ERROR EN GADGETS API:", e)
        return []



# ------------------ PIXABAY TECNOLOGÍA ------------------
async def get_summary(news):
    """
    Devuelve la URL de una imagen aleatoria de tecnología usando Pixabay.
    """
    try:
        query = "technology"
        url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={query}&image_type=photo&per_page=10"

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            data = resp.json()
            hits = data.get("hits", [])
            if not hits:
                return "https://via.placeholder.com/600x400?text=Imagen+no+disponible"
            
            # Elegir una imagen aleatoria de los resultados
            import random
            image_url = random.choice(hits).get("webformatURL")
            return image_url
    except Exception as e:
        print("ERROR EN RESUMEN PIXABAY:", e)
        return "https://via.placeholder.com/600x400?text=Imagen+no+disponible"