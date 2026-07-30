import json
import os
from pathlib import Path
from typing import Optional, List, Dict
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="YD Protección - Catálogo Profesional API",
    description="API Serverless para el catálogo de productos de YD Protección",
    version="2.0.0"
)

# Definición de rutas base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "products.json"
PUBLIC_DIR = BASE_DIR / "public"
TEMPLATES_DIR = BASE_DIR / "templates"

# Montar estáticos si existen
if PUBLIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(PUBLIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Memoria de métricas en sesión (Analytics)
METRICS_DATA = {
    "total_views": 0,
    "total_quotes": 0,
    "searches": [],
    "product_clicks": {},
    "product_quotes": {},
    "category_interest": {
        "proteccion_personal": 0,
        "emergencias_rescate": 0,
        "defensa_civil": 0,
        "senalizacion_seguridad": 0,
        "equipos_brigadas": 0,
        "dotacion_personalizada": 0
    }
}

def load_products():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Página principal del catálogo"""
    products = load_products()
    categories = [
        {"id": "todos", "name": "Todos los Productos"},
        {"id": "proteccion_personal", "name": "Protección Personal"},
        {"id": "emergencias_rescate", "name": "Emergencias y Rescate"},
        {"id": "defensa_civil", "name": "Defensa Civil & Brigadas"},
        {"id": "senalizacion_seguridad", "name": "Señalización y Seguridad"},
        {"id": "equipos_brigadas", "name": "Equipos para Brigadas"},
        {"id": "dotacion_personalizada", "name": "Dotación Personalizada"}
    ]
    return templates.TemplateResponse("index.html", {
        "request": request,
        "products": products,
        "categories": categories
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Página de control y analítica de clientes"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request
    })

@app.get("/api/products")
async def get_products(category: Optional[str] = None, q: Optional[str] = None):
    """Endpoint API para obtener productos con búsqueda y filtros"""
    products = load_products()
    
    if category and category != "todos":
        products = [p for p in products if p.get("category") == category]
        
    if q:
        query_lower = q.lower().strip()
        # Registrar término de búsqueda en métricas
        if query_lower and query_lower not in METRICS_DATA["searches"]:
            METRICS_DATA["searches"].append(query_lower)
            
        products = [
            p for p in products
            if query_lower in p.get("title", "").lower() 
            or query_lower in p.get("short_description", "").lower()
            or query_lower in p.get("category_name", "").lower()
        ]
        
    return JSONResponse(content={"status": "success", "count": len(products), "products": products})

@app.post("/api/track")
async def track_event(payload: Dict):
    """Registra interacciones y eventos de interés de los usuarios"""
    event_type = payload.get("event")
    product_id = payload.get("product_id")
    category = payload.get("category")
    
    METRICS_DATA["total_views"] += 1
    
    if category in METRICS_DATA["category_interest"]:
        METRICS_DATA["category_interest"][category] += 1
        
    if event_type == "view_product" and product_id:
        METRICS_DATA["product_clicks"][product_id] = METRICS_DATA["product_clicks"].get(product_id, 0) + 1
        
    elif event_type == "quote_whatsapp" and product_id:
        METRICS_DATA["total_quotes"] += 1
        METRICS_DATA["product_quotes"][product_id] = METRICS_DATA["product_quotes"].get(product_id, 0) + 1

    return JSONResponse(content={"status": "tracked", "event": event_type})

@app.get("/api/analytics")
async def get_analytics():
    """Devuelve las métricas de interés de los clientes para el Dashboard"""
    products = load_products()
    prod_map = {p["id"]: p["title"] for p in products}
    
    # Formatear el TOP de productos más vistos
    top_viewed = [
        {"id": pid, "title": prod_map.get(pid, pid), "views": count}
        for pid, count in sorted(METRICS_DATA["product_clicks"].items(), key=lambda x: x[1], reverse=True)[:5]
    ]
    
    # Formatear el TOP de productos más cotizados
    top_quoted = [
        {"id": pid, "title": prod_map.get(pid, pid), "quotes": count}
        for pid, count in sorted(METRICS_DATA["product_quotes"].items(), key=lambda x: x[1], reverse=True)[:5]
    ]
    
    return JSONResponse(content={
        "total_views": METRICS_DATA["total_views"],
        "total_quotes": METRICS_DATA["total_quotes"],
        "category_interest": METRICS_DATA["category_interest"],
        "top_viewed": top_viewed,
        "top_quoted": top_quoted,
        "recent_searches": METRICS_DATA["searches"][-10:]
    })

# Exportar handler para Vercel
handler = app
