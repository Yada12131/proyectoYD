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

# Catálogo completo con imágenes de alta definición hiper-realistas y acordes a cada producto
EMBEDDED_PRODUCTS = [
  {
    "id": "prod-001",
    "title": "Casco de Seguridad Industrial Tipo II Dieléctrico",
    "category": "proteccion_personal",
    "category_name": "Protección Personal",
    "short_description": "Casco dieléctrico de polietileno de alta densidad con suspensión de 4 puntos y ajuste de perilla.",
    "description": "Casco de seguridad de máxima resistencia contra impactos superiores y laterales. Cumple norma ANSI Z89.1 Clase E (hasta 20.000V). Incluye barboquejo reforzado y ranuras para protectores auditivos.",
    "price": "Cotizar",
    "badge": "MÁS VENDIDO",
    "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80",
    "specs": [
      "Norma: ANSI Z89.1 Tipo II Clase E",
      "Material: Polietileno de alta densidad (HDPE)",
      "Ajuste: Perilla de trinquete micrométrico",
      "Aislamiento eléctrico: Hasta 20.000 Voltios"
    ]
  },
  {
    "id": "prod-002",
    "title": "Gafas de Seguridad Policarbonato UV400 Anti-Fog",
    "category": "proteccion_personal",
    "category_name": "Protección Personal",
    "short_description": "Lentes de seguridad antiempañantes con filtro ultravioleta 99.9% y protección lateral.",
    "description": "Gafas de protección ocular de alto impacto. Marco ergonómico ultraliviano con patas ajustables, resistencia a rayaduras y filtro de luz UV400.",
    "price": "Cotizar",
    "badge": "POPULAR",
    "image": "https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=800&q=80",
    "specs": [
      "Norma: ANSI Z87.1+",
      "Protección: UV400 (99.9% radiación UV)",
      "Tratamiento: Antiempañante (Anti-Fog)",
      "Peso: 24 gramos ultraliviano"
    ]
  },
  {
    "id": "prod-003",
    "title": "Guantes Tácticos y de Rescate Anti-Corte Nivel 5",
    "category": "proteccion_personal",
    "category_name": "Protección Personal",
    "short_description": "Guantes de protección con refuerzo de TPR en nudillos y palma de alta fricción.",
    "description": "Guantes de uso rudo diseñados para rescate, brigadas y manipulación de herramientas. Ofrecen protección contra cortes, impactos y abrasión intensa.",
    "price": "Cotizar",
    "badge": "RECOMENDADO",
    "image": "https://images.unsplash.com/photo-1584483766114-2cea6facdf57?auto=format&fit=crop&w=800&q=80",
    "specs": [
      "Resistencia a corte: EN388 Nivel 5 / ANSI A4",
      "Material: Microfibra sintética y caucho TPR",
      "Cierre: Ajuste de velcro reforzado",
      "Superficie: Antideslizante de agarre seguro"
    ]
  },
  {
    "id": "prod-004",
    "title": "Botiquín de Primeros Auxilios Tipo B en Lona Impermeable",
    "category": "emergencias_rescate",
    "category_name": "Emergencias y Rescate",
    "short_description": "Botiquín reglamentario equipado para empresas, brigadas de rescate y vehículos.",
    "description": "Equipamiento reglamentario de atención médica inmediata. Confeccionado en lona tifón de alta resistencia con divisiones organizadoras y reata para hombro.",
    "price": "Cotizar",
    "badge": "NORMATIVO",
    "image": "https://images.unsplash.com/photo-1603398938378-e54eab446dde?auto=format&fit=crop&w=800&q=80",
    "specs": [
      "Cumplimiento: Resolución de Primeros Auxilios",
      "Contenido: Insumos de curación, inmovilización y antisépticos",
      "Material: Lona tifón impermeable reflectiva",
      "Portabilidad: Manijas de agarre y correa de hombro"
    ]
  },
  {
    "id": "prod-005",
    "title": "Linterna Táctica LED Recargable 2000 Lúmenes IPX8",
    "category": "emergencias_rescate",
    "category_name": "Emergencias y Rescate",
    "short_description": "Linterna impermeable de aluminio aeronáutico de alto alcance con 5 modos de iluminación.",
    "description": "Linterna táctica profesional de alta potencia para búsqueda y rescate nocturno. Resiste impactos y sumersión en agua. Incluye batería de litio recargable por USB.",
    "price": "Cotizar",
    "badge": "PRO",
    "image": "https://images.unsplash.com/photo-1546554137-f86b9593a222?auto=format&fit=crop&w=800&q=80",
    "specs": [
      "Potencia: 2000 Lúmenes CREE LED",
      "Modos: Alto, Medio, Bajo, Estroboscópico, SOS",
      "Resistencia: IPX8 Sumergible",
      "Batería: Litio 18650 recargable por USB"
    ]
  },
  {
    "id": "prod-006",
    "title": "Kit de Rescate en Alturas y Cuerdas Estáticas 11mm",
    "category": "emergencias_rescate",
    "category_name": "Emergencias y Rescate",
    "short_description": "Equipo completo para descenso, ascenso y maniobras de socorro en vertical.",
    "description": "Kit integral para operaciones de rescate en alturas y espacios confinados. Incluye cuerdas certificadas, mosquetones de acero auto-lock y arnés de cuerpo entero.",
    "price": "Cotizar",
    "badge": "EQUIPO CLAVE",
    "image": "https://images.unsplash.com/photo-1522163182402-834f871fd851?auto=format&fit=crop&w=800&q=80",
    "specs": [
      "Cuerdas: Estática 11mm certificada CE/EN1891",
      "Mosquetones: Acero forjado 50kN cierre automático",
      "Arnés: 5 puntos de anclaje ANSI Z359",
      "Incluye: Descendedor en 8 y poleas de rescate"
    ]
  },
  {
    "id": "prod-007",
    "title": "Chaleco Táctico Operativo Defensa Civil con Cintas 3M",
    "category": "defensa_civil",
    "category_name": "Defensa Civil & Brigadas",
    "short_description": "Chaleco multibolsillos de alta visibilidad con parches removibles en velcro.",
    "description": "Chaleco de dotación institucional para personal socorrista y brigadistas. Tela Ripstop antidesgarro con cintas reflectivas microesféricas 3M y funda para radio de comunicación.",
    "price": "Cotizar",
    "badge": "DESTACADO",
    "image": "https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&w=800&q=80",
    "specs": [
      "Material: Tela Ripstop 65% Poli/35% Algodón",
      "Reflectivo: Cintas 3M de 2 pulgadas de alta visibilidad",
      "Bolsillos: 8 compartimentos y portarradio",
      "Parches: Velcros porta-nombres e insignias"
    ]
  },
  {
    "id": "prod-008",
    "title": "Cono de Señalización Vial Flexible 90 cm Reflectivo",
    "category": "senalizacion_seguridad",
    "category_name": "Señalización y Seguridad",
    "short_description": "Cono de PVC indeformable de alta resistencia con base de caucho pesada.",
    "description": "Cono vial de 90 cm para control de tráfico y delimitación de áreas de emergencia. Soporta ser pisado por vehículos sin romperse y recupera su forma inmediatamente.",
    "price": "Cotizar",
    "badge": "NORMATIVO",
    "image": "https://images.unsplash.com/photo-1508873696983-2df515122519?auto=format&fit=crop&w=800&q=80",
    "specs": [
      "Altura: 90 cm (36 pulgadas)",
      "Material: PVC virgen flexible indeformable",
      "Reflectivo: Doble cinta High Intensity Grado Ingeniería",
      "Base: Caucho reciclado antideslizante de gran peso"
    ]
  },
  {
    "id": "prod-009",
    "title": "Megáfono de Emergencia Profesional 50W con Sirena y Grabador",
    "category": "equipos_brigadas",
    "category_name": "Equipos para Brigadas",
    "short_description": "Amplificador de voz de alto alcance para evacuación y manejo de contingencias.",
    "description": "Megáfono imprescindible para coordinadores de brigadas y evacuación de personal. Alcance auditivo de 1000 metros, sirena de alarma incorporada y micrófono desmontable.",
    "price": "Cotizar",
    "badge": "EVACUACIÓN",
    "image": "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=800&q=80",
    "specs": [
      "Potencia: 50 Watts Peak (Alcance 1000m)",
      "Funciones: Hablar, Sirena de Emergencia, Grabador",
      "Micrófono: De mano extensible tipo espiral",
      "Alimentación: Batería recargable incluida"
    ]
  }
]

# Estilos CSS de diseño ultra profesional (Gobernado por paleta institucional + diseño moderno)
EMBEDDED_CSS = """
:root {
    --navy: #0B1C30;
    --navy-dark: #06101D;
    --orange: #FF6600;
    --orange-hover: #E65C00;
    --white: #FFFFFF;
    --light-bg: #F4F6F8;
    --text-dark: #1E293B;
    --text-light: #64748B;
    --card-shadow: 0 10px 25px -5px rgba(0,0,0,0.08), 0 8px 10px -6px rgba(0,0,0,0.04);
    --hover-shadow: 0 20px 35px -5px rgba(255,102,0,0.2), 0 10px 15px -5px rgba(11,28,48,0.1);
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Roboto', sans-serif;
    background-color: var(--light-bg);
    color: var(--text-dark);
    line-height: 1.6;
    overflow-x: hidden;
}

h1, h2, h3, h4 { font-family: 'Montserrat', sans-serif; text-transform: uppercase; font-weight: 800; }

.container { max-width: 1240px; margin: 0 auto; padding: 0 20px; }

/* TOPBAR ELEGANTE */
.top-bar {
    background-color: var(--navy-dark);
    color: var(--white);
    padding: 14px 0;
    border-bottom: 3px solid var(--orange);
    position: sticky; top: 0; z-index: 1000;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.top-bar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.brand-title {
    font-size: 1.3rem;
    font-weight: 900;
    letter-spacing: 1px;
    color: var(--white);
    text-transform: uppercase;
}
.brand-title span { color: var(--orange); }

.btn-analytics {
    background: linear-gradient(135deg, var(--orange), #FF8533);
    color: var(--white);
    padding: 9px 20px;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 700;
    font-size: 0.88rem;
    box-shadow: 0 4px 12px rgba(255,102,0,0.3);
    transition: all 0.3s ease;
}
.btn-analytics:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(255,102,0,0.5); }

/* HERO SECCIÓN IMPACTANTE */
.hero {
    background: linear-gradient(180deg, var(--navy) 0%, var(--navy-dark) 100%);
    color: var(--white);
    text-align: center;
    padding: 70px 20px 90px;
    position: relative;
}
.hero-tag {
    display: inline-block;
    background: rgba(255,102,0,0.15);
    border: 1px solid var(--orange);
    color: var(--orange);
    padding: 6px 18px;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 20px;
}
.hero h2 { font-size: 1.3em; font-weight: 400; letter-spacing: 2px; margin-bottom: 15px; color: #E2E8F0; }
.hero h3 { font-size: 2.5em; margin-bottom: 15px; text-shadow: 0 2px 10px rgba(0,0,0,0.4); color: var(--white); }
.hero p { font-size: 1.15em; max-width: 650px; margin: 0 auto 35px; color: #CBD5E1; }

/* BARRA DE BÚSQUEDA INTERACTIVA EN TIEMPO REAL */
.search-wrapper {
    max-width: 600px;
    margin: 0 auto;
    position: relative;
}
.search-input {
    width: 100%;
    padding: 16px 20px 16px 50px;
    border-radius: 50px;
    border: 2px solid var(--orange);
    background: #FFFFFF;
    font-size: 1.05rem;
    outline: none;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    transition: all 0.3s ease;
}
.search-input:focus {
    box-shadow: 0 0 25px rgba(255,102,0,0.4);
}
.search-icon {
    position: absolute;
    left: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.2rem;
}

/* SECCIONES Y TITULOS */
section { padding: 75px 0; }
.section-title {
    text-align: center;
    color: var(--navy);
    font-size: 2.3em;
    margin-bottom: 15px;
    position: relative;
    padding-bottom: 20px;
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
.section-subtitle { text-align: center; font-size: 1.15em; color: var(--text-light); margin-bottom: 45px; }

/* QUIÉNES SOMOS & PILARES */
.grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 30px; text-align: center; }
.card-pilar {
    background-color: var(--white);
    padding: 40px 28px;
    border-radius: 14px;
    box-shadow: var(--card-shadow);
    border-top: 5px solid var(--orange);
    transition: all 0.35s ease;
}
.card-pilar.border-navy { border-top: none; border-bottom: 5px solid var(--navy); }
.card-pilar:hover { transform: translateY(-8px); box-shadow: var(--hover-shadow); }

/* NUESTRAS CATEGORÍAS */
.categories-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 22px; }
.category-item {
    background-color: var(--navy);
    color: var(--white);
    padding: 26px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border-left: 6px solid transparent;
}
.category-item:hover, .category-item.active {
    background-color: #112844;
    border-left: 6px solid var(--orange);
    transform: translateX(8px);
    box-shadow: 0 10px 25px rgba(11,28,48,0.25);
}
.category-item .number {
    font-family: 'Montserrat', sans-serif;
    font-size: 2.5em;
    font-weight: 900;
    color: var(--orange);
    margin-right: 22px;
}

/* TARJETAS DE PRODUCTO CON FOTOS DE ALTA DEFINICIÓN */
.product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 35px; }
.product-card {
    background-color: var(--white);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: var(--card-shadow);
    display: flex;
    flex-direction: column;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    border: 1px solid rgba(0,0,0,0.06);
}
.product-card:hover {
    transform: translateY(-10px);
    box-shadow: var(--hover-shadow);
}
.product-image-box {
    background-color: #0F172A;
    height: 240px;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}
.product-image-box img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s ease;
}
.product-card:hover .product-image-box img {
    transform: scale(1.08);
}
.product-badge {
    position: absolute;
    top: 14px; right: 14px;
    background: rgba(11, 28, 48, 0.9);
    border: 1px solid var(--orange);
    color: var(--orange);
    padding: 4px 12px;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    backdrop-filter: blur(4px);
}
.product-info { padding: 25px 22px; flex-grow: 1; display: flex; flex-direction: column; }
.product-category-tag {
    color: var(--orange);
    font-size: 0.78rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.product-info h4 { color: var(--navy); margin-bottom: 10px; font-size: 1.25em; line-height: 1.35; }
.product-info p { font-size: 0.95em; color: var(--text-light); margin-bottom: 18px; flex-grow: 1; }

.product-specs {
    list-style: none;
    margin-bottom: 20px;
    padding: 0;
    border-top: 1px solid #F1F5F9;
    padding-top: 14px;
}
.product-specs li {
    font-size: 0.84rem;
    color: #475569;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.product-specs li::before {
    content: '✓';
    color: var(--orange);
    font-weight: bold;
}

.btn-group { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: auto; }
.btn-detail {
    background: #F1F5F9;
    color: var(--navy);
    border: 1px solid #CBD5E1;
    padding: 11px 16px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.85em;
    cursor: pointer;
    transition: all 0.3s ease;
}
.btn-detail:hover { background: #E2E8F0; }
.btn-wa {
    background-color: #25D366;
    color: #FFF;
    border: none;
    padding: 11px 16px;
    border-radius: 8px;
    font-weight: 800;
    font-size: 0.85em;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(37,211,102,0.25);
}
.btn-wa:hover { background-color: #1EBE57; transform: translateY(-2px); box-shadow: 0 6px 16px rgba(37,211,102,0.4); }

/* MODAL DE VISTA COMPLETA */
.modal-backdrop {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    background: rgba(0,0,0,0.85); backdrop-filter: blur(6px);
    z-index: 2000; display: flex; align-items: center; justify-content: center;
    opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
}
.modal-backdrop.active { opacity: 1; pointer-events: all; }
.modal-card {
    background: #FFF; border-radius: 20px; width: 90%; max-width: 800px;
    padding: 35px; position: relative; max-height: 90vh; overflow-y: auto;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.4);
}
.modal-close {
    position: absolute; top: 15px; right: 20px; background: #F1F5F9; border: none;
    width: 38px; height: 38px; border-radius: 50%; font-size: 1.3rem; cursor: pointer;
}

/* BANNER DOTACIÓN */
.dotacion-banner {
    background: linear-gradient(135deg, var(--orange) 0%, #E65C00 100%);
    color: var(--white);
    padding: 75px 20px;
    text-align: center;
}
.dotacion-banner h2 { font-size: 2.4em; margin-bottom: 12px; }
.dotacion-list {
    list-style: none; display: flex; flex-wrap: wrap; justify-content: center;
    gap: 15px; margin-top: 35px; max-width: 950px; margin-left: auto; margin-right: auto;
}
.dotacion-list li {
    background-color: rgba(255,255,255,0.18);
    padding: 12px 26px; border-radius: 50px; font-weight: 700; border: 1px solid rgba(255,255,255,0.3);
}

/* FOOTER */
footer {
    background-color: var(--navy-dark);
    color: var(--white);
    padding: 75px 20px 35px;
    text-align: center;
    border-top: 5px solid var(--orange);
}
footer h2 { color: var(--orange); font-size: 2.1em; margin-bottom: 15px; }
footer .contact-info { margin: 35px 0; font-size: 1.1em; line-height: 2.2; }
footer .contact-info span { font-weight: 800; color: var(--orange); margin-right: 10px; }
.footer-bottom { margin-top: 50px; padding-top: 25px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.88em; color: #94A3B8; }
.bg-white { background-color: var(--white); }
.mt-5 { margin-top: 45px; }
"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo Oficial - YD Protección</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800;900&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>""" + EMBEDDED_CSS + """</style>
</head>
<body>

    <!-- TOPBAR CORPORATIVA -->
    <div class="top-bar">
        <div class="container top-bar-content">
            <div class="brand-title">YD <span>PROTECCIÓN</span></div>
            <a href="/dashboard" class="btn-analytics">📊 Panel de Analítica</a>
        </div>
    </div>

    <!-- PORTADA / HERO IMPACTANTE -->
    <header class="hero">
        <div class="container">
            <span class="hero-tag">SEGURIDAD QUE SALVA VIDAS ★ YESIKA & DANIEL</span>
            <h2>Seguridad y Emergencia a tu Alcance</h2>
            <h3>CATÁLOGO DE PRODUCTOS</h3>
            <p>Equipos especializados para Defensa Civil, Brigadas de Emergencia y Protección Industrial.</p>
            
            <div class="search-wrapper">
                <span class="search-icon">🔍</span>
                <input type="text" id="searchInput" class="search-input" placeholder="Buscar producto, casco, botiquín, chaleco, linterna..." summary="Buscador de productos">
            </div>
        </div>
    </header>

    <!-- QUIÉNES SOMOS -->
    <section class="bg-white">
        <div class="container">
            <h2 class="section-title">Quiénes Somos</h2>
            <p class="section-subtitle">Seguridad que salva vidas.</p>
            <p style="text-align: center; max-width: 820px; margin: 0 auto; font-size: 1.15em; color: var(--text-dark);">
                Somos una empresa enfocada en suministrar equipos y soluciones de protección de alta confiabilidad para prevención, atención de emergencias, rescate y seguridad operacional.
            </p>
            
            <div class="grid-3 mt-5">
                <div class="card-pilar">
                    <h4>PREVENCIÓN</h4>
                    <p>Soluciones para anticipar y controlar amenazas en el entorno laboral y operativo.</p>
                </div>
                <div class="card-pilar">
                    <h4>RESPUESTA</h4>
                    <p>Elementos de primera respuesta para emergencias, rescate y socorrismo.</p>
                </div>
                <div class="card-pilar">
                    <h4>SERVICIO</h4>
                    <p>Asesoría personalizada y acompañamiento técnico para cada tipo de necesidad.</p>
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
                        <p>Cascos dieléctricos, gafas UV, guantes tácticos y protección auditiva.</p>
                    </div>
                </div>
                <div class="category-item" data-category="emergencias_rescate">
                    <span class="number">02</span>
                    <div>
                        <h4>EMERGENCIAS Y RESCATE</h4>
                        <p>Botiquines A/B/C, linternas tácticas, kits de rescate y cuerdas estáticas.</p>
                    </div>
                </div>
                <div class="category-item" data-category="defensa_civil">
                    <span class="number">03</span>
                    <div>
                        <h4>DEFENSA CIVIL</h4>
                        <p>Dotación reglamentaria, chalecos 3M y elementos para brigadas.</p>
                    </div>
                </div>
                <div class="category-item" data-category="senalizacion_seguridad">
                    <span class="number">04</span>
                    <div>
                        <h4>SEÑALIZACIÓN Y SEGURIDAD</h4>
                        <p>Conos flexibles de 90cm, cintas de prevención y paletas de control.</p>
                    </div>
                </div>
                <div class="category-item" data-category="equipos_brigadas">
                    <span class="number">05</span>
                    <div>
                        <h4>EQUIPOS PARA BRIGADAS</h4>
                        <p>Megáfonos de 50W, estaciones lavaojos y equipos de evacuación.</p>
                    </div>
                </div>
                <div class="category-item" data-category="dotacion_personalizada">
                    <span class="number">06</span>
                    <div>
                        <h4>DOTACIÓN PERSONALIZADA</h4>
                        <p>Uniformes normativos, parches bordados y marcas corporativas.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- PRODUCTOS EN EXHIBICIÓN CON FOTOS ALTA DEFINICIÓN -->
    <section class="bg-white">
        <div class="container">
            <h2 class="section-title">Catálogo de Productos</h2>
            <p class="section-subtitle" id="productCountSub">{{ products|length }} productos disponibles en catálogo</p>
            
            <div class="product-grid mt-5" id="productGrid">
                {% for product in products %}
                <article class="product-card" data-id="{{ product.id }}" data-category="{{ product.category }}">
                    <div class="product-image-box">
                        <img src="{{ product.image }}" alt="{{ product.title }}" loading="lazy">
                        {% if product.badge %}
                        <span class="product-badge">{{ product.badge }}</span>
                        {% endif %}
                    </div>
                    <div class="product-info">
                        <span class="product-category-tag">{{ product.category_name }}</span>
                        <h4>{{ product.title }}</h4>
                        <p>{{ product.short_description }}</p>
                        
                        <ul class="product-specs">
                            {% for spec in product.specs[:3] %}
                            <li>{{ spec }}</li>
                            {% endfor %}
                        </ul>

                        <div class="btn-group">
                            <button class="btn-detail" onclick="openModal('{{ product.id }}')">Ver Detalles</button>
                            <button class="btn-wa" onclick="sendWhatsAppQuote('{{ product.id }}', '{{ product.title|escape }}', '{{ product.category }}')">
                                <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.705 1.754zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-1.14 4.162 4.223-1.106z"/></svg>
                                Cotizar
                            </button>
                        </div>
                    </div>
                </article>
                {% endfor %}
            </div>
        </div>
    </section>

    <!-- MODAL DE DETALLES TÉCNICOS -->
    <div class="modal-backdrop" id="modalBackdrop">
        <div class="modal-card">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px;">
                <div style="height: 260px; border-radius: 12px; overflow: hidden; background: #000;">
                    <img id="mImg" src="" style="width:100%; height:100%; object-fit:cover;">
                </div>
                <div>
                    <span id="mCat" class="product-category-tag">CATEGORÍA</span>
                    <h3 id="mTitle" style="color: var(--navy); margin-bottom: 10px;">Título del producto</h3>
                    <p id="mDesc" style="color: var(--text-light); font-size: 0.95rem; margin-bottom: 15px;">Descripción del producto</p>
                    
                    <h4 style="color: var(--orange); font-size: 0.9rem; margin-bottom: 8px;">ESPECIFICACIONES:</h4>
                    <ul id="mSpecs" class="product-specs"></ul>

                    <button id="mBtnWa" class="btn-wa" style="width: 100%; padding: 14px; font-size: 1rem; margin-top: 15px;">
                        Solicitar Cotización por WhatsApp
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- BANNER DOTACIÓN Y PERSONALIZACIÓN -->
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
                    <p>Selección estricta enfocada en alta seguridad y rendimiento en campo.</p>
                </div>
                <div class="card-pilar border-navy">
                    <h4>ASESORÍA PERSONALIZADA</h4>
                    <p>Te ayudamos a elegir la dotación ideal según tu riesgo operativo.</p>
                </div>
                <div class="card-pilar border-navy">
                    <h4>ENTREGA Y LOGÍSTICA</h4>
                    <p>Envíos ágiles para compras individuales y grandes brigadas corporativas.</p>
                </div>
                <div class="card-pilar border-navy">
                    <h4>ATENCIÓN POSTVENTA</h4>
                    <p>Acompañamiento continuo antes, durante y después de tu compra.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- FOOTER / CONTACTO -->
    <footer id="contacto">
        <div class="container">
            <h2>HABLEMOS DE TU SEGURIDAD</h2>
            <p>Solicita cotización y asesoría personalizada de inmediato</p>
            
            <div class="contact-info">
                <p><span>WHATSAPP:</span> +57 (300) 000-0000</p>
                <p><span>CORREO:</span> contacto@ydproteccion.com</p>
                <p><span>INSTAGRAM:</span> @ydproteccion</p>
                <p><span>UBICACIÓN:</span> Medellín, Antioquia, Colombia</p>
            </div>
            
            <div class="footer-bottom">
                <p>YESIKA & DANIEL | SEGURIDAD QUE SALVA VIDAS &copy; 2026</p>
            </div>
        </div>
    </footer>

    <!-- LÓGICA DE INTERACTIVIDAD -->
    <script>
        const WHATSAPP_PHONE = '573000000000';
        const productsData = """ + json.dumps(EMBEDDED_PRODUCTS) + """;

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
                    document.getElementById('productGrid').scrollIntoView({ behavior: 'smooth' });
                });
            });
        });

        function openModal(id) {
            const p = productsData.find(x => x.id === id);
            if (!p) return;

            document.getElementById('mImg').src = p.image;
            document.getElementById('mCat').textContent = p.category_name;
            document.getElementById('mTitle').textContent = p.title;
            document.getElementById('mDesc').textContent = p.description;
            
            const specsList = document.getElementById('mSpecs');
            specsList.innerHTML = p.specs.map(s => `<li>${s}</li>`).join('');

            document.getElementById('mBtnWa').onclick = () => sendWhatsAppQuote(p.id, p.title, p.category);

            document.getElementById('modalBackdrop').classList.add('active');
        }

        function closeModal() {
            document.getElementById('modalBackdrop').classList.remove('active');
        }

        function sendWhatsAppQuote(productId, title, category) {
            fetch('/api/track', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ event: 'quote_whatsapp', product_id: productId, category: category })
            }).catch(e => console.log(e));

            const msg = `Hola *YD Protección*, solicito cotización de:\n\n📌 *Producto:* ${title}\n🆔 *Código:* ${productId}\n\nPor favor me comparten precio y disponibilidad. ¡Gracias!`;
            window.open(`https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(msg)}`, '_blank');
        }
    </script>
</body>
</html>"""

# HTML del Dashboard de Analítica
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Analítica - YD Protección</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>""" + EMBEDDED_CSS + """</style>
</head>
<body>
    <div class="top-bar">
        <div class="container top-bar-content">
            <div class="brand-title">YD <span>PROTECCIÓN</span> - ANALÍTICA DE CLIENTES</div>
            <a href="/" class="btn-analytics">← Volver al Catálogo</a>
        </div>
    </div>

    <div class="container" style="padding: 60px 20px;">
        <h2 class="section-title">Métricas de Interés de Clientes</h2>
        <p class="section-subtitle">Panel de Monitoreo para Yesika & Daniel</p>

        <div class="grid-3 mt-5">
            <div class="card-pilar">
                <h4>Vistas e Interacciones</h4>
                <div style="font-size: 2.8em; font-weight: 900; color: var(--orange);" id="totalViews">0</div>
                <p style="color: var(--text-light); font-size: 0.9rem;">Consultas realizadas por visitantes</p>
            </div>
            <div class="card-pilar">
                <h4>Cotizaciones WhatsApp</h4>
                <div style="font-size: 2.8em; font-weight: 900; color: #25D366;" id="totalQuotes">0</div>
                <p style="color: var(--text-light); font-size: 0.9rem;">Chats de cotización iniciados</p>
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
    "total_quotes": 0
}

@app.get("/")
@app.get("/api")
@app.get("/api/index")
@app.get("/api/index.py")
async def home_page(request: Request):
    try:
        rendered = Template(INDEX_HTML).render(products=EMBEDDED_PRODUCTS)
        return HTMLResponse(content=rendered)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error renderizando sitio</h1><p>{str(e)}</p>")

@app.get("/dashboard")
@app.get("/api/dashboard")
async def dashboard_page(request: Request):
    try:
        rendered = Template(DASHBOARD_HTML).render()
        return HTMLResponse(content=rendered)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error cargando analítica</h1><p>{str(e)}</p>")

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
