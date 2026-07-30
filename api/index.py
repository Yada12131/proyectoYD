import json
import os
from pathlib import Path
from typing import Optional, Dict
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="YD Protección - Catálogo Profesional API",
    description="API Serverless para el catálogo de productos de YD Protección",
    version="2.0.0"
)

# Resolución dinámica y segura de rutas para Vercel Serverless
CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent

# Buscar directorio public
PUBLIC_DIR = None
for candidate in [PARENT_DIR / "public", CURRENT_DIR / "public", Path.cwd() / "public"]:
    if candidate.exists() and candidate.is_dir():
        PUBLIC_DIR = candidate
        break

if PUBLIC_DIR:
    app.mount("/static", StaticFiles(directory=str(PUBLIC_DIR)), name="static")
    app.mount("/css", StaticFiles(directory=str(PUBLIC_DIR / "css")), name="css")
    app.mount("/js", StaticFiles(directory=str(PUBLIC_DIR / "js")), name="js")
    app.mount("/images", StaticFiles(directory=str(PUBLIC_DIR / "images")), name="images")

# Buscar directorio de plantillas
TEMPLATES_DIR = None
for candidate in [CURRENT_DIR / "templates", PARENT_DIR / "templates", Path.cwd() / "templates", Path.cwd() / "api" / "templates"]:
    if candidate.exists() and candidate.is_dir():
        TEMPLATES_DIR = candidate
        break

templates = Jinja2Templates(directory=str(TEMPLATES_DIR)) if TEMPLATES_DIR else None

# Buscar archivo de productos
DATA_FILE = None
for candidate in [CURRENT_DIR / "data" / "products.json", CURRENT_DIR / "products.json", PARENT_DIR / "data" / "products.json", Path.cwd() / "api" / "data" / "products.json", Path.cwd() / "data" / "products.json"]:
    if candidate.exists():
        DATA_FILE = candidate
        break

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

FALLBACK_PRODUCTS = [
    {
        "id": "prod-001",
        "title": "Casco de Seguridad Industrial Tipo II",
        "category": "proteccion_personal",
        "category_name": "Protección Personal",
        "short_description": "Casco de protección dieléctrico con suspensión de 4 puntos y ajuste de perilla.",
        "description": "Casco de seguridad de alta resistencia contra impactos y descargas eléctricas.",
        "price": "Cotizar",
        "badge": "Más Vendido",
        "image": "/images/casco_seguridad.jpg",
        "specs": ["Norma: ANSI Z89.1", "Material: HDPE", "Resistencia: 20.000V"]
    },
    {
        "id": "prod-004",
        "title": "Botiquín Tipo B de Primeros Auxilios",
        "category": "emergencias_rescate",
        "category_name": "Emergencias y Rescate",
        "short_description": "Botiquín reglamentario para empresas, vehículos y brigadas.",
        "description": "Equipamiento completo de atención inmediata para emergencias médicas.",
        "price": "Cotizar",
        "badge": "Esencial",
        "image": "/images/botiquin_rescate.jpg",
        "specs": ["Normativa completa", "Lona impermeable", "Manijas reforzadas"]
    }
]

def load_products():
    if DATA_FILE and DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return FALLBACK_PRODUCTS

# Mapeo de rutas múltiples para Vercel Serverless Rewrites
@app.get("/")
@app.get("/api")
@app.get("/api/index.py")
@app.get("/api/index")
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
    if templates:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "products": products,
            "categories": categories
        })
    return HTMLResponse(content="<h1>YD Protección Catálogo</h1><p>Cargando aplicación...</p>")

@app.get("/dashboard")
@app.get("/api/dashboard")
async def dashboard_page(request: Request):
    """Página de control y analítica de clientes"""
    if templates:
        return templates.TemplateResponse("dashboard.html", {
            "request": request
        })
    return HTMLResponse(content="<h1>Panel de Analítica YD Protección</h1>")

@app.get("/api/products")
@app.get("/products")
async def get_products(category: Optional[str] = None, q: Optional[str] = None):
    """Endpoint API para obtener productos con búsqueda y filtros"""
    products = load_products()
    
    if category and category != "todos":
        products = [p for p in products if p.get("category") == category]
        
    if q:
        query_lower = q.lower().strip()
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
@app.post("/track")
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
@app.get("/analytics")
async def get_analytics():
    """Devuelve las métricas de interés de los clientes para el Dashboard"""
    products = load_products()
    prod_map = {p["id"]: p["title"] for p in products}
    
    top_viewed = [
        {"id": pid, "title": prod_map.get(pid, pid), "views": count}
        for pid, count in sorted(METRICS_DATA["product_clicks"].items(), key=lambda x: x[1], reverse=True)[:5]
    ]
    
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

# Ruta comodín para capturar cualquier ruta no encontrada y servir el catálogo
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, full_path: str):
    if full_path.startswith("api/"):
        return JSONResponse(status_code=404, content={"detail": f"Path '{full_path}' not found"})
    return await home_page(request)

# Handler para Vercel
handler = app
