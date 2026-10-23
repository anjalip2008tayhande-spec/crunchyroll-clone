from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Crunchyroll Clone API")

# In-memory database for Hero Carousel & Trending Anime
HERO_SLIDES = [
    {
        "id": "dbs-beerus",
        "title": "DRAGON BALL SUPER: BEERUS",
        "logo_text": "DRAGON BALL SUPER",
        "sub_logo": "BEERUS",
        "rating": "U/A 13+",
        "audio": "Subtitled",
        "genres": ["Action", "Adventure", "Fantasy", "Shonen"],
        "description": "Years after Majin Buu's defeat, Earth has returned to peace. But when Beerus, the God of Destruction, awakens, that peace is shattered. Drawn to Earth by rumors of the Saiyan who defeated Frieza, Beerus seeks to challenge Goku with...",
        "episode_btn": "START WATCHING E1",
        "bg_image": "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1920&auto=format&fit=crop",
        "bookmarked": False
    },
    {
        "id": "solo-leveling",
        "title": "SOLO LEVELING",
        "logo_text": "SOLO LEVELING",
        "sub_logo": "ARISE",
        "rating": "U/A 16+",
        "audio": "Sub | Dub",
        "genres": ["Action", "Adventure", "Fantasy"],
        "description": "Ten years ago, 'the Gate' appeared and connected the real world with the realm of magic and monsters. Ordinary hunter Sung Jinwoo discovers a hidden double dungeon that changes his fate forever.",
        "episode_btn": "START WATCHING S1 E1",
        "bg_image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1920&auto=format&fit=crop",
        "bookmarked": False
    },
    {
        "id": "jjk",
        "title": "JUJUTSU KAISEN",
        "logo_text": "JUJUTSU KAISEN",
        "sub_logo": "SHIBUYA INCIDENT",
        "rating": "U/A 16+",
        "audio": "Sub | Dub",
        "genres": ["Action", "Supernatural", "Shonen"],
        "description": "Yuji Itadori eats a cursed finger to save a classmate, and now Ryomen Sukuna, a powerfully evil sorcerer known as the King of Curses, lives in his soul.",
        "episode_btn": "START WATCHING S1 E1",
        "bg_image": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=1920&auto=format&fit=crop",
        "bookmarked": False
    }
]

TRENDING_INDIA = [
    {
        "id": "demon-slayer",
        "title": "Demon Slayer: Kimetsu no Yaiba",
        "meta": "Sub | Dub",
        "poster": "https://images.unsplash.com/photo-1578632767115-351597cf2477?q=80&w=600&auto=format&fit=crop",
        "bookmarked": True
    },
    {
        "id": "one-piece",
        "title": "One Piece",
        "meta": "Subtitled",
        "poster": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?q=80&w=600&auto=format&fit=crop",
        "bookmarked": True
    },
    {
        "id": "naruto-shippuden",
        "title": "Naruto Shippuden",
        "meta": "Sub | Dub",
        "poster": "https://images.unsplash.com/photo-1560972550-aba3456b5564?q=80&w=600&auto=format&fit=crop",
        "bookmarked": True
    },
    {
        "id": "kaiju-no-8",
        "title": "Kaiju No. 8",
        "meta": "Sub | Dub",
        "poster": "https://images.unsplash.com/photo-1618336753974-aae8e04506aa?q=80&w=600&auto=format&fit=crop",
        "bookmarked": False
    },
    {
        "id": "black-clover",
        "title": "Black Clover",
        "meta": "Sub | Dub",
        "poster": "https://images.unsplash.com/photo-1541562232579-512a21360020?q=80&w=600&auto=format&fit=crop",
        "bookmarked": True
    }
]

class BookmarkRequest(BaseModel):
    item_id: str

@app.get("/api/home")
def get_home_data():
    return {
        "hero_slides": HERO_SLIDES,
        "trending_india": TRENDING_INDIA
    }

@app.post("/api/bookmark")
def toggle_bookmark(req: BookmarkRequest):
    for slide in HERO_SLIDES:
        if slide["id"] == req.item_id:
            slide["bookmarked"] = not slide["bookmarked"]
            return {"status": "success", "id": slide["id"], "bookmarked": slide["bookmarked"]}
    
    for anime in TRENDING_INDIA:
        if anime["id"] == req.item_id:
            anime["bookmarked"] = not anime["bookmarked"]
            return {"status": "success", "id": anime["id"], "bookmarked": anime["bookmarked"]}
            
    raise HTTPException(status_code=404, detail="Anime not found")

@app.get("/api/watchlist")
def get_watchlist():
    saved_hero = [s for s in HERO_SLIDES if s["bookmarked"]]
    saved_trending = [a for a in TRENDING_INDIA if a["bookmarked"]]
    return {"watchlist": saved_hero + saved_trending}

# Serve static frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")