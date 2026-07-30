import json
from typing import Optional, Dict
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Template

app = FastAPI(
    title="YD Protección - Catálogo Profesional API",
    description="API Serverless para el catálogo de productos de YD Protección",
    version="2.0.0"
)

# Catálogo completo de productos
EMBEDDED_PRODUCTS = [
  {
    "id": "prod-001",
    "title": "Casco de Seguridad Industrial Tipo II",
    "category": "proteccion_personal",
    "category_name": "Protección Personal",
    "short_description": "Casco de protección dieléctrico con suspensión de 4 puntos y ajuste de perilla.",
    "description": "Casco de seguridad de alta resistencia contra impactos y descargas eléctricas. Diseñado bajo normativa ANSI Z89.1.",
    "price": "Consultar",
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
    "price": "Consultar",
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
    "price": "Consultar",
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
    "title": "Botiquín Tipo B de Primeros Auxilios",
    "category": "emergencias_rescate",
    "category_name": "Emergencias y Rescate",
    "short_description": "Botiquín reglamentario para empresas, vehículos y brigadas de emergencia.",
    "description": "Equipamiento completo de atención inmediata para emergencias médicas e insumos de primeros auxilios.",
    "price": "Consultar",
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
    "title": "Linterna Táctica LED Recargable",
    "category": "emergencias_rescate",
    "category_name": "Emergencias y Rescate",
    "short_description": "Linterna recargable de 2000 lúmenes contra agua e impactos.",
    "description": "Linterna profesional para operaciones nocturnas de rescate y patrullaje.",
    "price": "Consultar",
    "badge": "Pro",
    "image": "/images/linterna_tactica.jpg",
    "specs": [
      "Potencia: 2000 Lúmenes CREE LED",
      "Batería: Litio recargable USB",
      "Resistencia al agua: Certificación IPX8",
      "Autonomía: Hasta 12 horas seguidas"
    ]
  },
  {
    "id": "prod-006",
    "title": "Kit de Rescate y Cuerdas Estáticas",
    "category": "emergencias_rescate",
    "category_name": "Emergencias y Rescate",
    "short_description": "Elementos configurables según necesidad operativa de rescate en alturas.",
    "description": "Kit integral para operaciones de descenso, ascenso e inmovilización en lugares de difícil acceso.",
    "price": "Consultar",
    "badge": "Equipo Clave",
    "image": "/images/camilla_rigida.jpg",
    "specs": [
      "Cuerdas: Estáticas certificadas 11mm",
      "Mosquetones: Acero forjado 50kN auto-lock",
      "Arnés: Cuerpo entero norma ANSI Z359"
    ]
  },
  {
    "id": "prod-007",
    "title": "Chaleco Táctico Operativo Defensa Civil",
    "category": "defensa_civil",
    "category_name": "Defensa Civil & Brigadas",
    "short_description": "Chaleco multibolsillos con cintas reflectivas 3M y parches removibles.",
    "description": "Chaleco de alta visibilidad para personal socorrista y brigadistas.",
    "price": "Consultar",
    "badge": "Destacado",
    "image": "/images/chaleco_tactico.jpg",
    "specs": [
      "Material: Tela Ripstop 65% poliéster 35% algodón",
      "Reflectivo: Cintas de microesferas de vidrio de 2 pulgadas",
      "Compartimentos: 8 bolsillos frontales y portarradio"
    ]
  },
  {
    "id": "prod-008",
    "title": "Cono de Señalización Flexible 90 cm Reflectivo",
    "category": "senalizacion_seguridad",
    "category_name": "Señalización y Seguridad",
    "short_description": "Cono vial indeformable de PVC naranja con doble cinta reflectiva.",
    "description": "Cono de tráfico de 90 cm con base pesada de caucho para excelente estabilidad.",
    "price": "Consultar",
    "badge": "Normativo",
    "image": "/images/cono_senalizacion.jpg",
    "specs": [
      "Altura: 90 cm (36 pulgadas)",
      "Material: PVC virgen flexible",
      "Cintas reflectivas: Doble banda High Intensity"
    ]
  },
  {
    "id": "prod-009",
    "title": "Megáfono de Emergencia Profesional 50W",
    "category": "equipos_brigadas",
    "category_name": "Equipos para Brigadas",
    "short_description": "Megáfono de alto alcance con micrófono de mano y sonido de alarma.",
    "description": "Equipo de amplificación de voz esencial para evacuación de edificios.",
    "price": "Consultar",
    "badge": "Evacuación",
    "image": "/images/megafono_emergencia.jpg",
    "specs": [
      "Potencia máxima: 50 Watts Peak",
      "Alcance eficaz: 800 - 1000 metros",
      "Funciones: Hablar, Sirena de emergencia"
    ]
  }
]

# Estilos CSS embebidos para garantrizar renderizado 100% impecable en Vercel
EMBEDDED_CSS = """
:root {
    --navy: #0B1C30;
    --orange: #FF6600;
    --white: #FFFFFF;
    --light-bg: #F4F6F8;
    --text-dark: #333333;
    --text-light: #777777;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Roboto', sans-serif;
    background-color: var(--light-bg);
    color: var(--text-dark);
    line-height: 1.6;
    overflow-x: hidden;
}

h1, h2, h3, h4 { font-family: 'Montserrat', sans-serif; text-transform: uppercase; }

.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

/* NAVBAR DE NAVEGACIÓN Y ANALÍTICA */
.top-bar {
    background-color: #06111f;
    color: var(--white);
    padding: 12px 0;
    border-bottom: 1px solid rgba(255,102,0,0.3);
}
.top-bar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.brand-title {
    font-weight: 800;
    font-size: 1.2rem;
    color: var(--white);
}
.brand-title span { color: var(--orange); }
.btn-analytics {
    background-color: var(--orange);
    color: var(--white);
    padding: 8px 18px;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 700;
    font-size: 0.85rem;
    transition: all 0.3s ease;
}
.btn-analytics:hover { background-color: #e65c00; transform: translateY(-2px); }

/* HERO / PORTADA ORIGINAL CON ANIMACIONES */
.hero {
    background-color: var(--navy);
    color: var(--white);
    text-align: center;
    padding: 60px 20px 80px;
    border-bottom: 8px solid var(--orange);
    position: relative;
}
.hero h2 { font-size: 1.2em; font-weight: 400; letter-spacing: 2px; margin-bottom: 20px; color: #e0e0e0; }
.hero h3 { font-size: 2.2em; margin-bottom: 15px; text-shadow: 0 2px 4px rgba(0,0,0,0.3); color: var(--white); }
.hero p { font-size: 1.1em; max-width: 600px; margin: 0 auto 30px; color: #cccccc; }

/* BARRA DE BÚSQUEDA INTERACTIVA */
.search-wrapper {
    max-width: 550px;
    margin: 0 auto;
    position: relative;
}
.search-input {
    width: 100%;
    padding: 15px 20px 15px 45px;
    border-radius: 50px;
    border: 2px solid var(--orange);
    background: #FFFFFF;
    font-size: 1rem;
    outline: none;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.search-icon {
    position: absolute;
    left: 18px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.1rem;
}

/* SECCIONES GENERALES */
section { padding: 70px 0; }
.section-title {
    text-align: center;
    color: var(--navy);
    font-size: 2.4em;
    margin-bottom: 20px;
    position: relative;
    padding-bottom: 20px;
    font-weight: 800;
}
.section-title::after {
    content: '';
    position: absolute;
    bottom: 0; left: 50%;
    transform: translateX(-50%);
    width: 80px; height: 5px;
    background-color: var(--orange);
    border-radius: 5px;
}
.section-subtitle { text-align: center; font-size: 1.2em; color: var(--text-light); margin-bottom: 40px; }

/* PILARES Y CATEGORÍAS */
.grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; text-align: center; }
.card-pilar {
    background-color: var(--white);
    padding: 35px 25px;
    border-radius: 12px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    border-top: 5px solid var(--orange);
    transition: all 0.4s ease;
}
.card-pilar.border-navy { border-top: none; border-bottom: 5px solid var(--navy); }
.card-pilar:hover { transform: translateY(-8px); box-shadow: 0 15px 30px rgba(0,0,0,0.1); }

.categories-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; }
.category-item {
    background-color: var(--navy);
    color: var(--white);
    padding: 25px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border-left: 5px solid transparent;
}
.category-item:hover, .category-item.active {
    background-color: #122b4a;
    border-left: 5px solid var(--orange);
    transform: translateX(8px);
}
.category-item .number {
    font-family: 'Montserrat', sans-serif;
    font-size: 2.5em;
    font-weight: 800;
    color: var(--orange);
    margin-right: 20px;
}

/* PRODUCTOS */
.product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; }
.product-card {
    background-color: var(--white);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    text-align: center;
    display: flex;
    flex-direction: column;
    transition: all 0.4s ease;
}
.product-card:hover { transform: translateY(-8px); box-shadow: 0 15px 30px rgba(0,0,0,0.12); }
.product-image-box {
    background-color: #e9ecef;
    height: 220px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #adb5bd;
    font-weight: 600;
    position: relative;
    overflow: hidden;
}
.product-image-box img { width: 100%; height: 100%; object-fit: cover; }
.product-info { padding: 25px 20px; flex-grow: 1; display: flex; flex-direction: column; }
.product-info h4 { color: var(--navy); margin-bottom: 10px; font-size: 1.2em; }
.product-info p { font-size: 0.95em; color: var(--text-light); margin-bottom: 20px; flex-grow: 1; }

.btn-group { display: flex; gap: 10px; justify-content: center; }
.btn {
    display: inline-block;
    background-color: var(--orange);
    color: var(--white);
    text-decoration: none;
    padding: 12px 24px;
    font-weight: 800;
    border-radius: 6px;
    text-transform: uppercase;
    font-size: 0.85em;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    border: 2px solid var(--orange);
    cursor: pointer;
}
.btn:hover { background-color: transparent; color: var(--orange); }
.btn-wa { background-color: #25D366; border-color: #25D366; }
.btn-wa:hover { background-color: transparent; color: #25D366; }

/* BANNER DOTACIÓN */
.dotacion-banner {
    background-color: var(--orange);
    background-image: linear-gradient(135deg, var(--orange) 0%, #e65c00 100%);
    color: var(--white);
    padding: 70px 20px;
    text-align: center;
}
.dotacion-banner h2 { font-size: 2.3em; margin-bottom: 15px; }
.dotacion-list {
    list-style: none; display: flex; flex-wrap: wrap; justify-content: center;
    gap: 15px; margin-top: 30px; max-width: 900px; margin-left: auto; margin-right: auto;
}
.dotacion-list li {
    background-color: rgba(255,255,255,0.15);
    padding: 10px 22px; border-radius: 50px; font-weight: 600; border: 1px solid rgba(255,255,255,0.2);
}

/* FOOTER */
footer {
    background-color: var(--navy);
    color: var(--white);
    padding: 70px 20px 30px;
    text-align: center;
    border-top: 5px solid var(--orange);
}
footer h2 { color: var(--orange); font-size: 2em; margin-bottom: 15px; }
footer .contact-info { margin: 30px 0; font-size: 1.1em; line-height: 2.2; }
footer .contact-info span { font-weight: 800; color: var(--orange); margin-right: 10px; }
.footer-bottom { margin-top: 40px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.85em; color: #888; }
.bg-white { background-color: var(--white); }
.mt-5 { margin-top: 40px; }
"""

# HTML completo con el diseño original enriquecido de YD Protección
INDEX_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo - YD Protección</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>""" + EMBEDDED_CSS + """</style>
</head>
<body>

    <!-- BARRA SUPERIOR DE NAVEGACIÓN -->
    <div class="top-bar">
        <div class="container top-bar-content">
            <div class="brand-title">YD <span>PROTECCIÓN</span></div>
            <a href="/dashboard" class="btn-analytics">📊 Panel de Analítica</a>
        </div>
    </div>

    <!-- PORTADA / HERO -->
    <header class="hero">
        <div class="container">
            <h2>Seguridad y Emergencia a tu Alcance</h2>
            <h3>CATÁLOGO DE PRODUCTOS</h3>
            <p>Equipos para Defensa Civil, emergencias y protección personal.</p>
            
            <div class="search-wrapper" style="margin-top: 25px;">
                <span class="search-icon">🔍</span>
                <input type="text" id="searchInput" class="search-input" placeholder="Buscar producto, casco, botiquín, chaleco..." summary="Buscador de productos">
            </div>
        </div>
    </header>

    <!-- QUIÉNES SOMOS -->
    <section class="bg-white">
        <div class="container">
            <h2 class="section-title">Quiénes Somos</h2>
            <p class="section-subtitle">Seguridad que salva vidas.</p>
            <p style="text-align: center; max-width: 800px; margin: 0 auto; font-size: 1.1em;">
                Somos una empresa enfocada en suministrar equipos y soluciones de protección para prevención, atención de emergencias, rescate y seguridad.
            </p>
            
            <div class="grid-3 mt-5">
                <div class="card-pilar">
                    <h4>PREVENCIÓN</h4>
                    <p>Soluciones para anticipar y controlar amenazas.</p>
                </div>
                <div class="card-pilar">
                    <h4>RESPUESTA</h4>
                    <p>Elementos para emergencias y rescate.</p>
                </div>
                <div class="card-pilar">
                    <h4>SERVICIO</h4>
                    <p>Asesoría y acompañamiento al cliente.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- NUESTRAS CATEGORÍAS -->
    <section>
        <div class="container">
            <h2 class="section-title">Nuestras Categorías</h2>
            
            <div class="categories-grid mt-5" id="categoriesGrid">
                <div class="category-item active" data-category="todos">
                    <span class="number">00</span>
                    <div>
                        <h4>TODOS LOS PRODUCTOS</h4>
                        <p>Catálogo general completo.</p>
                    </div>
                </div>
                <div class="category-item" data-category="proteccion_personal">
                    <span class="number">01</span>
                    <div>
                        <h4>PROTECCIÓN PERSONAL</h4>
                        <p>Cascos, gafas, guantes, protección auditiva y respiratoria.</p>
                    </div>
                </div>
                <div class="category-item" data-category="emergencias_rescate">
                    <span class="number">02</span>
                    <div>
                        <h4>EMERGENCIAS Y RESCATE</h4>
                        <p>Botiquines, linternas, herramientas y equipos de respuesta.</p>
                    </div>
                </div>
                <div class="category-item" data-category="defensa_civil">
                    <span class="number">03</span>
                    <div>
                        <h4>DEFENSA CIVIL</h4>
                        <p>Dotación y elementos para brigadas y organismos de atención.</p>
                    </div>
                </div>
                <div class="category-item" data-category="senalizacion_seguridad">
                    <span class="number">04</span>
                    <div>
                        <h4>SEÑALIZACIÓN Y SEGURIDAD</h4>
                        <p>Señales, conos, cintas, iluminación y control de áreas.</p>
                    </div>
                </div>
                <div class="category-item" data-category="equipos_brigadas">
                    <span class="number">05</span>
                    <div>
                        <h4>EQUIPOS PARA BRIGADAS</h4>
                        <p>Soluciones para empresas, industrias e instituciones.</p>
                    </div>
                </div>
                <div class="category-item" data-category="dotacion_personalizada">
                    <span class="number">06</span>
                    <div>
                        <h4>DOTACIÓN PERSONALIZADA</h4>
                        <p>Uniformes, parches, bordados y elementos corporativos.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- PRODUCTOS -->
    <section class="bg-white">
        <div class="container">
            <h2 class="section-title">Catálogo de Productos</h2>
            <p class="section-subtitle" id="productCountSub">{{ products|length }} productos en exhibición</p>
            
            <div class="product-grid mt-5" id="productGrid">
                {% for product in products %}
                <article class="product-card" data-id="{{ product.id }}" data-category="{{ product.category }}">
                    <div class="product-image-box">
                        <img src="{{ product.image }}" alt="{{ product.title }}" onerror="this.src='https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=600&q=80'">
                    </div>
                    <div class="product-info">
                        <h4>{{ product.title }}</h4>
                        <p>{{ product.short_description }}</p>
                        <div class="btn-group">
                            <button class="btn btn-wa" onclick="sendWhatsAppQuote('{{ product.id }}', '{{ product.title|escape }}', '{{ product.category }}')">
                                Cotizar en WhatsApp
                            </button>
                        </div>
                    </div>
                </article>
                {% endfor %}
            </div>
        </div>
    </section>

    <!-- DOTACIÓN Y PERSONALIZACIÓN -->
    <section class="dotacion-banner">
        <div class="container">
            <h2>DOTACIÓN Y PERSONALIZACIÓN</h2>
            <p style="font-size: 1.2em;">Lleva la identidad de tu equipo a cada operación.</p>
            
            <ul class="dotacion-list">
                <li>Uniformes y prendas de trabajo</li>
                <li>Bordados y estampados</li>
                <li>Parches institucionales</li>
                <li>Personalización de cascos</li>
                <li>Kits para brigadas</li>
                <li>Dotación empresarial</li>
            </ul>
        </div>
    </section>

    <!-- POR QUÉ ELEGIRNOS -->
    <section class="bg-white">
        <div class="container">
            <h2 class="section-title">¿Por qué elegir YD Protección?</h2>
            
            <div class="grid-3 mt-5">
                <div class="card-pilar border-navy">
                    <h4>PRODUCTOS CONFIABLES</h4>
                    <p>Selección enfocada en seguridad y desempeño.</p>
                </div>
                <div class="card-pilar border-navy">
                    <h4>ASESORÍA PERSONALIZADA</h4>
                    <p>Te ayudamos a elegir según tu necesidad.</p>
                </div>
                <div class="card-pilar border-navy">
                    <h4>ENTREGA Y LOGÍSTICA</h4>
                    <p>Soluciones para compras individuales y empresariales.</p>
                </div>
                <div class="card-pilar border-navy">
                    <h4>ATENCIÓN POSTVENTA</h4>
                    <p>Acompañamiento antes, durante y después de tu compra.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- FOOTER / CONTACTO -->
    <footer id="contacto">
        <div class="container">
            <h2>HABLEMOS DE TU SEGURIDAD</h2>
            <p>Solicita cotización y asesoría personalizada</p>
            
            <div class="contact-info">
                <p><span>WHATSAPP:</span> +57 (300) 000-0000</p>
                <p><span>CORREO:</span> contacto@ydproteccion.com</p>
                <p><span>INSTAGRAM:</span> @ydproteccion</p>
                <p><span>CIUDAD:</span> Medellín, Antioquia, Colombia</p>
            </div>
            
            <div class="footer-bottom">
                <p>YESIKA & DANIEL | SEGURIDAD QUE SALVA VIDAS</p>
            </div>
        </div>
    </footer>

    <!-- LÓGICA DE BÚSQUEDA Y COTIZACIÓN EN WHATSAPP -->
    <script>
        const WHATSAPP_PHONE = '573000000000';
        
        document.addEventListener('DOMContentLoaded', () => {
            const searchInput = document.getElementById('searchInput');
            const categoryItems = document.querySelectorAll('.category-item');
            const productCards = document.querySelectorAll('.product-card');
            
            let currentCat = 'todos';
            let currentSearch = '';
            
            function filterProducts() {
                productCards.forEach(card => {
                    const cat = card.getAttribute('data-category');
                    const text = card.textContent.toLowerCase();
                    
                    const matchCat = (currentCat === 'todos') || (cat === currentCat);
                    const matchSearch = text.includes(currentSearch);
                    
                    if (matchCat && matchSearch) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });
            }
            
            if (searchInput) {
                searchInput.addEventListener('input', (e) => {
                    currentSearch = e.target.value.toLowerCase().trim();
                    filterProducts();
                });
            }
            
            categoryItems.forEach(item => {
                item.addEventListener('click', () => {
                    categoryItems.forEach(i => i.classList.remove('active'));
                    item.classList.add('active');
                    currentCat = item.getAttribute('data-category');
                    filterProducts();
                    
                    // Desplazarse suavemente a productos
                    document.getElementById('productGrid').scrollIntoView({ behavior: 'smooth' });
                });
            });
        });

        function sendWhatsAppQuote(productId, title, category) {
            fetch('/api/track', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ event: 'quote_whatsapp', product_id: productId, category: category })
            }).catch(e => console.log(e));

            const msg = `Hola *YD Protección*, quiero solicitar cotización de:\n\n📌 *Producto:* ${title}\n🆔 *Código:* ${productId}\n\nPor favor me brindan información de disponibilidad y precio. Gracias!`;
            window.open(`https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(msg)}`, '_blank');
        }
    </script>
</body>
</html>"""

# HTML completo del Dashboard
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Analítica - YD Protección</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        """ + EMBEDDED_CSS + """
        .dashboard-card { background: #FFF; padding: 25px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 25px; }
        .metric-box { font-size: 2.5em; font-weight: 800; color: var(--orange); }
    </style>
</head>
<body>
    <div class="top-bar">
        <div class="container top-bar-content">
            <div class="brand-title">YD <span>PROTECCIÓN</span> - ANALÍTICA</div>
            <a href="/" class="btn-analytics">← Volver al Catálogo</a>
        </div>
    </div>

    <div class="container" style="padding: 50px 20px;">
        <h2 class="section-title">Métricas de Interés de Clientes</h2>
        <p class="section-subtitle">Panel de Control para Yesika & Daniel</p>

        <div class="grid-3 mt-5">
            <div class="dashboard-card">
                <h4>Total Interacciones</h4>
                <div class="metric-box" id="totalViews">0</div>
                <p style="color:#777;">Clics e interés en productos</p>
            </div>
            <div class="dashboard-card">
                <h4>Cotizaciones WhatsApp</h4>
                <div class="metric-box" id="totalQuotes" style="color:#25D366;">0</div>
                <p style="color:#777;">Clientes que iniciaron chat</p>
            </div>
        </div>
    </div>

    <script>
        fetch('/api/analytics')
            .then(res => res.json())
            .then(data => {
                document.getElementById('totalViews').textContent = data.total_views || 0;
                document.getElementById('totalQuotes').textContent = data.total_quotes || 0;
            }).catch(e => console.log(e));
    </script>
</body>
</html>"""

METRICS_DATA = {
    "total_views": 0,
    "total_quotes": 0,
    "searches": [],
    "product_clicks": {},
    "product_quotes": {},
    "category_interest": {}
}

@app.get("/")
@app.get("/api")
@app.get("/api/index")
@app.get("/api/index.py")
async def home_page(request: Request):
    """Página principal del catálogo con diseño original de YD Protección"""
    try:
        rendered = Template(INDEX_HTML).render(products=EMBEDDED_PRODUCTS)
        return HTMLResponse(content=rendered)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error renderizando diseño</h1><p>{str(e)}</p>")

@app.get("/dashboard")
@app.get("/api/dashboard")
async def dashboard_page(request: Request):
    """Página de analítica"""
    try:
        rendered = Template(DASHBOARD_HTML).render()
        return HTMLResponse(content=rendered)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error cargando dashboard</h1><p>{str(e)}</p>")

@app.get("/api/products")
async def get_products(category: Optional[str] = None, q: Optional[str] = None):
    products = EMBEDDED_PRODUCTS
    if category and category != "todos":
        products = [p for p in products if p.get("category") == category]
    if q:
        query_lower = q.lower().strip()
        products = [p for p in products if query_lower in p.get("title", "").lower() or query_lower in p.get("short_description", "").lower()]
    return JSONResponse(content={"status": "success", "count": len(products), "products": products})

@app.post("/api/track")
@app.post("/track")
async def track_event(payload: Dict):
    event_type = payload.get("event")
    product_id = payload.get("product_id")
    METRICS_DATA["total_views"] += 1
    if event_type == "quote_whatsapp":
        METRICS_DATA["total_quotes"] += 1
    return JSONResponse(content={"status": "tracked"})

@app.get("/api/analytics")
async def get_analytics():
    return JSONResponse(content={
        "total_views": METRICS_DATA["total_views"],
        "total_quotes": METRICS_DATA["total_quotes"]
    })

@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, full_path: str):
    if full_path.startswith("api/"):
        return JSONResponse(status_code=404, content={"detail": "Not Found"})
    return await home_page(request)

handler = app
