import json
import os
from pathlib import Path
from typing import Optional, Dict
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template

app = FastAPI(
    title="YD Protección - Catálogo Profesional API",
    description="API Serverless para el catálogo de productos de YD Protección",
    version="2.0.0"
)

# Catálogo completo embebido (Garantiza funcionamiento 100% libre de fallos en Vercel)
EMBEDDED_PRODUCTS = [
  {
    "id": "prod-001",
    "title": "Casco de Seguridad Industrial Tipo II",
    "category": "proteccion_personal",
    "category_name": "Protección Personal",
    "short_description": "Casco de protección dieléctrico con suspensión de 4 puntos y ajuste de perilla.",
    "description": "Casco de seguridad de alta resistencia contra impactos y descargas eléctricas. Diseñado bajo normativa ANSI Z89.1.",
    "price": "Cotizar",
    "badge": "Más Vendido",
    "image": "/images/casco_seguridad.jpg",
    "specs": [
      "Norma: ANSI Z89.1 Tipo II Clase E",
      "Material: Polietileno de alta densidad (HDPE)",
      "Ajuste: Perilla de trinquete micrométrico",
      "Resistencia eléctrica: Hasta 20.000 voltios"
    ]
  },
  {
    "id": "prod-002",
    "title": "Gafas de Seguridad Policarbonato UV400",
    "category": "proteccion_personal",
    "category_name": "Protección Personal",
    "short_description": "Lentes de seguridad antiempañantes y antirrayaduras con protección UV.",
    "description": "Gafas de protección ocular ergonómicas con marco ultraliviano y brazos ajustables.",
    "price": "Cotizar",
    "badge": "Popular",
    "image": "/images/gafas_seguridad.jpg",
    "specs": [
      "Norma: ANSI Z87.1+",
      "Protección: UV400 (99.9% filtros radiación)",
      "Recubrimiento: Anti-fog (antiempañante)",
      "Peso: 24 gramos"
    ]
  },
  {
    "id": "prod-003",
    "title": "Guantes Tácticos y de Rescate Multipropósito",
    "category": "proteccion_personal",
    "category_name": "Protección Personal",
    "short_description": "Guantes reforzados anti-corte y anti-impacto con agarre sintético.",
    "description": "Guantes diseñados para operaciones de rescate, brigadas y manipulación de equipos.",
    "price": "Cotizar",
    "badge": "Recomendado",
    "image": "/images/guantes_tacticos.jpg",
    "specs": [
      "Nivel de corte: EN388 Nivel 5 / ANSI A4",
      "Material: Microfibra sintética y TPR",
      "Cierre: Ajuste de velcro reforzado en muñeca",
      "Tallas disponibles: S, M, L, XL"
    ]
  },
  {
    "id": "prod-004",
    "title": "Botiquín Tipo B de Primeros Auxilios con Lona Resistente",
    "category": "emergencias_rescate",
    "category_name": "Emergencias y Rescate",
    "short_description": "Botiquín reglamentario para empresas, vehículos y brigadas de emergencia.",
    "description": "Equipamiento completo de atención inmediata para emergencias médicas e insumos de primeros auxilios.",
    "price": "Cotizar",
    "badge": "Esencial",
    "image": "/images/botiquin_rescate.jpg",
    "specs": [
      "Normativa: Cumple resolución de primeros auxilios",
      "Contenido: Insumos de curación, inmovilización y antisépticos",
      "Material bolso: Lona tifón impermeable reflectiva",
      "Portabilidad: Manijas reforzadas y reata de hombro"
    ]
  },
  {
    "id": "prod-005",
    "title": "Camilla Rígida de Inmovilización con Inmovilizador de Cabeza",
    "category": "emergencias_rescate",
    "category_name": "Emergencias y Rescate",
    "short_description": "Camilla espinal plástica de alta flotabilidad con sujetadores de correa.",
    "description": "Camilla de rescate de una sola pieza en polietileno de alta resistencia.",
    "price": "Cotizar",
    "badge": "Equipo Clave",
    "image": "/images/camilla_rigida.jpg",
    "specs": [
      "Capacidad de carga: 180 kg",
      "Material: Polietileno HDPE soplado",
      "Incluye: Inmovilizador lateral de cabeza y 3 arneses de sujeción",
      "Radiolúcida: 100% compatible con rayos X"
    ]
  },
  {
    "id": "prod-006",
    "title": "Linterna Táctica LED Recargable de Alta Potencia",
    "category": "emergencias_rescate",
    "category_name": "Emergencias y Rescate",
    "short_description": "Linterna recargable de 2000 lúmenes contra agua e impactos.",
    "description": "Linterna profesional para operaciones nocturnas de rescate y patrullaje.",
    "price": "Cotizar",
    "badge": "Pro",
    "image": "/images/linterna_tactica.jpg",
    "specs": [
      "Potencia: 2000 Lúmenes CREE LED",
      "Batería: Litio recargable 18650 USB",
      "Resistencia al agua: Certificación IPX8",
      "Autonomía: Hasta 12 horas seguidas"
    ]
  },
  {
    "id": "prod-007",
    "title": "Chaleco Táctico Operativo para Defensa Civil y Brigadas",
    "category": "defensa_civil",
    "category_name": "Defensa Civil & Brigadas",
    "short_description": "Chaleco multibolsillos con cintas reflectivas 3M y parches removibles.",
    "description": "Chaleco de alta visibilidad para personal socorrista y brigadistas.",
    "price": "Cotizar",
    "badge": "Destacado",
    "image": "/images/chaleco_tactico.jpg",
    "specs": [
      "Material: Tela Ripstop 65% poliéster 35% algodón",
      "Reflectivo: Cintas de microesferas de vidrio de 2 pulgadas",
      "Compartimentos: 8 bolsillos frontales y portarradio",
      "Personalización: Velcros porta-nombres y porta-escudos"
    ]
  },
  {
    "id": "prod-008",
    "title": "Kit de Dotación Institucional Defensa Civil",
    "category": "defensa_civil",
    "category_name": "Defensa Civil & Brigadas",
    "short_description": "Conjunto de gorra, camiseta, parches bordados y reata operativa.",
    "description": "Kit oficial para socorristas e integrantes de brigadas de atención de desastres.",
    "price": "Cotizar",
    "badge": "Completo",
    "image": "/images/kit_dotacion.jpg",
    "specs": [
      "Incluye: Gorra bordada, camiseta dry-fit, parches y reata",
      "Bordados: Alta definición con hilos de resistencia UV",
      "Color: Naranja reglamentario / Azul marino"
    ]
  },
  {
    "id": "prod-009",
    "title": "Cono de Señalización Flexible 90 cm Reflectivo",
    "category": "senalizacion_seguridad",
    "category_name": "Señalización y Seguridad",
    "short_description": "Cono vial indeformable de PVC naranja con doble cinta reflectiva.",
    "description": "Cono de tráfico de 90 cm con base pesada de caucho para excelente estabilidad.",
    "price": "Cotizar",
    "badge": "Normativo",
    "image": "/images/cono_senalizacion.jpg",
    "specs": [
      "Altura: 90 cm (36 pulgadas)",
      "Material: PVC virgen flexible de alta resistencia",
      "Cintas reflectivas: Doble banda Grado Ingeniería High Intensity",
      "Base: Caucho pesado reciclado antideslizante"
    ]
  },
  {
    "id": "prod-010",
    "title": "Megáfono de Emergencia Profesional 50W con Sirena",
    "category": "equipos_brigadas",
    "category_name": "Equipos para Brigadas",
    "short_description": "Megáfono de alto alcance con micrófono de mano y sonido de alarma.",
    "description": "Equipo de amplificación de voz esencial para evacuación de edificios y manejo de masas.",
    "price": "Cotizar",
    "badge": "Evacuación",
    "image": "/images/megafono_emergencia.jpg",
    "specs": [
      "Potencia máxima: 50 Watts Peak",
      "Alcance eficaz: 800 - 1000 metros",
      "Funciones: Hablar, Sirena de emergencia, Grabador de voz",
      "Alimentación: Batería recargable o pilas tipo C"
    ]
  },
  {
    "id": "prod-011",
    "title": "Estación Lavaojos Portátil de Emergencia 32 Litros",
    "category": "equipos_brigadas",
    "category_name": "Equipos para Brigadas",
    "short_description": "Dispositivo lavaojos por gravedad de accionamiento rápido.",
    "description": "Lavaojos autónomo por gravedad para lugares de trabajo sin suministro continuo de agua.",
    "price": "Cotizar",
    "badge": "Seguridad Industrial",
    "image": "/images/estacion_lavaojos.jpg",
    "specs": [
      "Capacidad: 32 Litros / 8 Galones",
      "Norma: ANSI Z358.1-2014",
      "Tiempo de lavado: 15 minutos continuo",
      "Material: Polietileno virgen aprobado por la FDA"
    ]
  },
  {
    "id": "prod-012",
    "title": "Servicio de Bordado y Personalización de Dotación",
    "category": "dotacion_personalizada",
    "category_name": "Dotación Personalizada",
    "short_description": "Bordados institucionales, parches en velcro y estampado de logos.",
    "description": "Personalización completa para empresas, brigadas privadas e instituciones de socorro.",
    "price": "Cotizar",
    "badge": "Personalizado",
    "image": "/images/dotacion_personalizada.jpg",
    "specs": [
      "Técnicas: Bordado computarizado 3D, DTF, Vinilo textil y Serigrafía",
      "Resistencia: Soportan lavados industriales intensos",
      "Diseño: Matrizado digital personalizado a partir de tu logo"
    ]
  }
]

# Plantilla HTML Embebida (Index)
INDEX_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YD Protección | Catálogo de Equipos de Seguridad y Emergencia</title>
    <meta name="description" content="Catálogo profesional de equipos para Defensa Civil, brigadas de emergencia, protección personal y señalización. Medellín, Colombia.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800;900&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/main.css">
</head>
<body>
    <nav class="navbar">
        <div class="container navbar-content">
            <a href="/" class="brand-logo">
                <div class="brand-badge">YD</div>
                <div class="brand-name">PROTECCIÓN <span>EQUIPOS</span></div>
            </a>
            <div class="nav-actions">
                <a href="/dashboard" class="btn-dashboard-link" title="Ver analítica e interés de clientes">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                    Panel Analítica
                </a>
            </div>
        </div>
    </nav>

    <header class="hero">
        <div class="container">
            <span class="hero-tag">Seguridad que salva vidas ★ Yesika & Daniel</span>
            <h1>CATÁLOGO OFICIAL DE EQUIPOS</h1>
            <p>Soluciones especializadas para Defensa Civil, Brigadas de Emergencia, Protección Industrial y Dotación Institucional.</p>
            <div class="search-box-wrapper">
                <span class="search-icon">🔍</span>
                <input type="text" id="searchInput" class="search-input" placeholder="Buscar casco, botiquín, chaleco, linterna...">
            </div>
        </div>
    </header>

    <main class="container">
        <div class="categories-nav" id="categoriesNav">
            <button class="category-pill active" data-category="todos">Todos los Productos</button>
            <button class="category-pill" data-category="proteccion_personal">Protección Personal</button>
            <button class="category-pill" data-category="emergencias_rescate">Emergencias y Rescate</button>
            <button class="category-pill" data-category="defensa_civil">Defensa Civil & Brigadas</button>
            <button class="category-pill" data-category="senalizacion_seguridad">Señalización y Seguridad</button>
            <button class="category-pill" data-category="equipos_brigadas">Equipos para Brigadas</button>
            <button class="category-pill" data-category="dotacion_personalizada">Dotación Personalizada</button>
        </div>

        <div class="product-section-title">
            <h2>Productos Disponibles</h2>
            <span class="product-count" id="productCount">{{ products|length }} productos disponibles</span>
        </div>

        <div class="products-grid" id="productsGrid">
            {% for product in products %}
            <article class="product-card" data-id="{{ product.id }}" data-category="{{ product.category }}">
                <div class="product-image-container">
                    <img src="{{ product.image }}" alt="{{ product.title }}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=600&q=80'">
                    {% if product.badge %}
                    <span class="product-badge">{{ product.badge }}</span>
                    {% endif %}
                </div>
                <div class="product-body">
                    <span class="product-category-tag">{{ product.category_name }}</span>
                    <h3 class="product-title">{{ product.title }}</h3>
                    <p class="product-desc">{{ product.short_description }}</p>
                    
                    <ul class="product-specs-list">
                        {% for spec in product.specs[:3] %}
                        <li>{{ spec }}</li>
                        {% endfor %}
                    </ul>
                    
                    <div class="product-actions">
                        <button class="btn-secondary" onclick="openProductModal('{{ product.id }}')">Ver Detalles</button>
                        <button class="btn-whatsapp" onclick="sendWhatsAppQuote('{{ product.id }}', '{{ product.title|escape }}', '{{ product.category }}')">
                            <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.705 1.754zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-1.14 4.162 4.223-1.106z"/></svg>
                            Cotizar
                        </button>
                    </div>
                </div>
            </article>
            {% endfor %}
        </div>
    </main>

    <div class="modal-backdrop" id="modalBackdrop">
        <div class="modal-content">
            <button class="modal-close" id="modalCloseBtn">&times;</button>
            <div class="modal-grid">
                <div class="modal-image">
                    <img id="modalImage" src="" alt="Producto YD">
                </div>
                <div>
                    <span class="product-category-tag" id="modalCategory">Categoría</span>
                    <h2 id="modalTitle" style="font-size: 1.6rem; margin-bottom: 1rem;">Título Producto</h2>
                    <p id="modalDesc" style="color: var(--color-text-muted); margin-bottom: 1.5rem;">Descripción detallada.</p>
                    
                    <h4 style="color: var(--color-accent-amber); margin-bottom: 0.8rem;">Especificaciones Técnicas:</h4>
                    <ul class="product-specs-list" id="modalSpecs"></ul>
                    
                    <div style="margin-top: 2rem;">
                        <button id="modalQuoteBtn" class="btn-whatsapp" style="width: 100%; padding: 1rem; font-size: 1rem;">
                            <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.705 1.754zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-1.14 4.162 4.223-1.106z"/></svg>
                            Solicitar Cotización Inmediata por WhatsApp
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer>
        <div class="container footer-content">
            <h2>HABLEMOS DE TU SEGURIDAD</h2>
            <p style="color: var(--color-text-muted);">Asesoría personalizada en suministros de protección y prevención de riesgos.</p>
            <div class="footer-contacts">
                <p><span>WHATSAPP:</span> +57 (300) 000-0000</p>
                <p><span>CORREO:</span> contacto@ydproteccion.com</p>
                <p><span>INSTAGRAM:</span> @ydproteccion</p>
                <p><span>UBICACIÓN:</span> Medellín, Antioquia, Colombia</p>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 YD PROTECCIÓN — YESIKA & DANIEL | Seguridad que Salva Vidas</p>
            </div>
        </div>
    </footer>
    <script src="/js/main.js"></script>
</body>
</html>"""

# Plantilla HTML Embebida (Dashboard)
DASHBOARD_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Analítica & Interés de Clientes | YD Protección</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800;900&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/dashboard.css">
</head>
<body>
    <nav class="navbar">
        <div class="container navbar-content">
            <a href="/" class="brand-logo">
                <div class="brand-badge">YD</div>
                <div class="brand-name">PANEL DE <span>ANALÍTICA</span></div>
            </a>
            <div class="nav-actions">
                <a href="/" class="btn-dashboard-link">← Volver al Catálogo</a>
            </div>
        </div>
    </nav>

    <header class="container dashboard-header">
        <div class="dashboard-title">
            <div>
                <h1>Métricas e Interés de Clientes</h1>
                <p style="color: var(--color-text-muted);">Monitoreo en tiempo real de productos más consultados, búsquedas y cotizaciones.</p>
            </div>
            <div>
                <span class="hero-tag" style="margin-bottom:0;">Panel Privado Daniel & Yesika</span>
            </div>
        </div>
    </header>

    <main class="container">
        <div class="metrics-overview-grid">
            <div class="metric-card">
                <div class="metric-icon">👁</div>
                <div>
                    <div class="metric-val" id="metricTotalViews">0</div>
                    <div class="metric-label">Vistas e Interacciones Totales</div>
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-icon" style="background: rgba(37,211,102,0.15); color:#25D366;">💬</div>
                <div>
                    <div class="metric-val" id="metricTotalQuotes">0</div>
                    <div class="metric-label">Cotizaciones Iniciadas (WhatsApp)</div>
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-icon" style="background: rgba(234,88,12,0.15); color:var(--color-accent-orange);">🔥</div>
                <div>
                    <div class="metric-val" id="metricPopularCategory">Protección</div>
                    <div class="metric-label">Categoría Más Consultada</div>
                </div>
            </div>
        </div>

        <div class="dashboard-grid-2">
            <div class="analytics-panel">
                <h3><span>⭐</span> Productos Más Consultados</h3>
                <ul class="rank-list" id="topViewedList"></ul>
            </div>
            <div class="analytics-panel">
                <h3><span style="color:#25D366;">📱</span> Productos Más Cotizados (WhatsApp)</h3>
                <ul class="rank-list" id="topQuotedList"></ul>
            </div>
        </div>

        <div class="analytics-panel" style="margin-bottom: 4rem;">
            <h3><span>🔎</span> Términos de Búsqueda de los Clientes</h3>
            <p style="color: var(--color-text-muted); font-size: 0.9rem; margin-bottom: 1.2rem;">Palabras clave que buscan los visitantes:</p>
            <div class="tag-cloud" id="recentSearchesCloud"></div>
        </div>
    </main>
    <script src="/js/dashboard.js"></script>
</body>
</html>"""

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
    return EMBEDDED_PRODUCTS

@app.get("/")
@app.get("/api")
@app.get("/api/index")
@app.get("/api/index.py")
async def home_page(request: Request):
    """Página principal del catálogo renderizada sin dependencias externas"""
    try:
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
        rendered = Template(INDEX_HTML_TEMPLATE).render(products=products, categories=categories)
        return HTMLResponse(content=rendered)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error cargando catálogo</h1><p>{str(e)}</p>")

@app.get("/dashboard")
@app.get("/api/dashboard")
async def dashboard_page(request: Request):
    """Página de control y analítica de clientes"""
    try:
        rendered = Template(DASHBOARD_HTML_TEMPLATE).render()
        return HTMLResponse(content=rendered)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error cargando dashboard</h1><p>{str(e)}</p>")

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

# Ruta comodín para capturar cualquier subruta no encontrada
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, full_path: str):
    if full_path.startswith("api/"):
        return JSONResponse(status_code=404, content={"detail": f"Path '{full_path}' not found"})
    return await home_page(request)

# Handler exportado para Vercel Serverless
handler = app
