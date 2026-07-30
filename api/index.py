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

# Catálogo oficial con fotos de alta definición 100% exactas y respaldos garantizados
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
    "image": "/images/casco_industrial.jpg",
    "fallback_image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80",
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
    "image": "/images/gafas_proteccion.jpg",
    "fallback_image": "https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?auto=format&fit=crop&w=800&q=80",
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
    "image": "/images/guantes_rescate.jpg",
    "fallback_image": "https://images.unsplash.com/photo-1617347454431-f49d7ff5c3b1?auto=format&fit=crop&w=800&q=80",
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
    "image": "/images/botiquin_lona.jpg",
    "fallback_image": "https://images.unsplash.com/photo-1603398938378-e54eab446dde?auto=format&fit=crop&w=800&q=80",
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
    "image": "/images/linterna_led.jpg",
    "fallback_image": "https://images.unsplash.com/photo-1546554137-f86b9593a222?auto=format&fit=crop&w=800&q=80",
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
    "image": "/images/kit_rescate_cuerdas.jpg",
    "fallback_image": "https://images.unsplash.com/photo-1522163182402-834f871fd851?auto=format&fit=crop&w=800&q=80",
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
    "image": "/images/chaleco_defensa_civil.jpg",
    "fallback_image": "https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&w=800&q=80",
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
    "image": "/images/cono_vial.jpg",
    "fallback_image": "https://images.unsplash.com/photo-1508873696983-2df515122519?auto=format&fit=crop&w=800&q=80",
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
    "image": "/images/megafono_50w.jpg",
    "fallback_image": "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=800&q=80",
    "specs": [
      "Potencia: 50 Watts Peak (Alcance 1000m)",
      "Funciones: Hablar, Sirena de Emergencia, Grabador",
      "Micrófono: De mano extensible tipo espiral",
      "Alimentación: Batería recargable incluida"
    ]
  }
]

# Estilos CSS de sitio web profesional premium
EMBEDDED_CSS = """
:root {
    --navy: #0B1C30;
    --navy-dark: #06101D;
    --orange: #FF6600;
    --orange-hover: #E65C00;
    --white: #FFFFFF;
    --light-bg: #F8FAFC;
    --text-dark: #1E293B;
    --text-light: #64748B;
    --card-shadow: 0 10px 30px -5px rgba(0,0,0,0.06), 0 4px 6px -2px rgba(0,0,0,0.03);
    --hover-shadow: 0 20px 40px -5px rgba(255,102,0,0.22), 0 12px 18px -4px rgba(11,28,48,0.12);
}

html { scroll-behavior: smooth; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--light-bg);
    color: var(--text-dark);
    line-height: 1.6;
    overflow-x: hidden;
}

h1, h2, h3, h4, h5 { font-family: 'Montserrat', sans-serif; text-transform: uppercase; font-weight: 800; }

.container { max-width: 1240px; margin: 0 auto; padding: 0 20px; }

/* HEADER / NAVBAR FLOTANTE PROFESIONAL */
.top-bar {
    background: rgba(6, 16, 29, 0.95);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    color: var(--white);
    padding: 16px 0;
    border-bottom: 3px solid var(--orange);
    position: sticky; top: 0; z-index: 1000;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.top-bar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.brand-logo-group {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
}
.brand-badge {
    background: linear-gradient(135deg, var(--orange), #FF8533);
    color: #FFF;
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 1.2rem;
    padding: 4px 10px;
    border-radius: 6px;
}
.brand-title {
    font-size: 1.3rem;
    font-weight: 900;
    letter-spacing: 1px;
    color: var(--white);
}
.brand-title span { color: var(--orange); }

.nav-links { display: flex; gap: 24px; align-items: center; }
.nav-links a {
    color: #E2E8F0; text-decoration: none; font-weight: 600; font-size: 0.92rem;
    transition: all 0.3s ease; position: relative; padding: 4px 0;
}
.nav-links a:hover { color: var(--orange); }
.nav-links a::after {
    content: ''; position: absolute; bottom: 0; left: 0; width: 0; height: 2px;
    background: var(--orange); transition: width 0.3s ease;
}
.nav-links a:hover::after { width: 100%; }

.btn-analytics {
    background: linear-gradient(135deg, var(--orange), #FF8533);
    color: var(--white);
    padding: 9px 22px;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 700;
    font-size: 0.88rem;
    box-shadow: 0 4px 14px rgba(255,102,0,0.35);
    transition: all 0.3s ease;
}
.btn-analytics:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255,102,0,0.5); }

/* HERO IMPACTANTE */
.hero {
    background: radial-gradient(circle at 50% 20%, rgba(255,102,0,0.12) 0%, rgba(6,16,29,1) 75%);
    color: var(--white);
    text-align: center;
    padding: 85px 20px 100px;
    position: relative;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.hero-tag {
    display: inline-block;
    background: rgba(255,102,0,0.15);
    border: 1px solid var(--orange);
    color: var(--orange);
    padding: 6px 20px;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 22px;
    text-transform: uppercase;
}
.hero h2 { font-size: 1.35em; font-weight: 400; letter-spacing: 2.5px; margin-bottom: 15px; color: #E2E8F0; }
.hero h3 { font-size: 2.7em; margin-bottom: 18px; text-shadow: 0 4px 15px rgba(0,0,0,0.4); color: var(--white); letter-spacing: -0.5px; }
.hero p { font-size: 1.2em; max-width: 700px; margin: 0 auto 38px; color: #CBD5E1; line-height: 1.7; }

.search-wrapper { max-width: 620px; margin: 0 auto; position: relative; }
.search-input {
    width: 100%;
    padding: 17px 22px 17px 52px;
    border-radius: 50px;
    border: 2px solid var(--orange);
    background: #FFFFFF;
    font-size: 1.05rem;
    outline: none;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}
.search-input:focus { box-shadow: 0 0 30px rgba(255,102,0,0.45); }
.search-icon { position: absolute; left: 22px; top: 50%; transform: translateY(-50%); font-size: 1.2rem; }

/* SECCIONES Y ENCABEZADOS */
section { padding: 85px 0; }
.section-title {
    text-align: center;
    color: var(--navy);
    font-size: 2.5em;
    margin-bottom: 15px;
    position: relative;
    padding-bottom: 22px;
    letter-spacing: -0.5px;
}
.section-title::after {
    content: ''; position: absolute; bottom: 0; left: 50%;
    transform: translateX(-50%); width: 85px; height: 5px;
    background-color: var(--orange); border-radius: 5px;
}
.section-subtitle { text-align: center; font-size: 1.18em; color: var(--text-light); margin-bottom: 50px; }

/* GRIDS Y TARJETAS SECCIÓN QUIÉNES SOMOS */
.grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 32px; }
.grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 26px; }
.grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 32px; }

.card-box {
    background: var(--white);
    padding: 42px 30px;
    border-radius: 16px;
    box-shadow: var(--card-shadow);
    border-top: 5px solid var(--orange);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    border-left: 1px solid rgba(0,0,0,0.04);
    border-right: 1px solid rgba(0,0,0,0.04);
}
.card-box.navy-top { border-top: 5px solid var(--navy); }
.card-box:hover { transform: translateY(-8px); box-shadow: var(--hover-shadow); }
.card-box h4 { color: var(--navy); margin-bottom: 14px; font-size: 1.35em; }

/* NUESTRAS CATEGORÍAS */
.categories-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 24px; }
.category-item {
    background-color: var(--navy);
    color: var(--white);
    padding: 28px;
    border-radius: 16px;
    display: flex; align-items: center;
    cursor: pointer; transition: all 0.35s ease;
    border-left: 6px solid transparent;
}
.category-item:hover, .category-item.active {
    background-color: #112844;
    border-left: 6px solid var(--orange);
    transform: translateX(10px);
    box-shadow: 0 12px 30px rgba(11,28,48,0.28);
}
.category-item .number {
    font-family: 'Montserrat', sans-serif;
    font-size: 2.6em; font-weight: 900;
    color: var(--orange); margin-right: 24px;
}

/* TARJETAS DE PRODUCTO */
.product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 36px; }
.product-card {
    background-color: var(--white);
    border-radius: 18px; overflow: hidden;
    box-shadow: var(--card-shadow);
    display: flex; flex-direction: column;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(0,0,0,0.06);
}
.product-card:hover { transform: translateY(-10px); box-shadow: var(--hover-shadow); }
.product-image-box {
    background-color: #0F172A;
    height: 250px; position: relative; overflow: hidden;
    display: flex; align-items: center; justify-content: center;
}
.product-image-box img {
    width: 100%; height: 100%; object-fit: cover;
    transition: transform 0.6s ease;
}
.product-card:hover .product-image-box img { transform: scale(1.08); }
.product-badge {
    position: absolute; top: 14px; right: 14px;
    background: rgba(11, 28, 48, 0.92);
    border: 1px solid var(--orange); color: var(--orange);
    padding: 5px 14px; border-radius: 50px; font-size: 0.75rem; font-weight: 800;
    letter-spacing: 0.5px;
}
.product-info { padding: 26px 24px; flex-grow: 1; display: flex; flex-direction: column; }
.product-category-tag { color: var(--orange); font-size: 0.8rem; font-weight: 800; letter-spacing: 1px; margin-bottom: 6px; }
.product-info h4 { color: var(--navy); margin-bottom: 10px; font-size: 1.28em; line-height: 1.35; }
.product-info p { font-size: 0.96em; color: var(--text-light); margin-bottom: 20px; flex-grow: 1; }

.product-specs { list-style: none; margin-bottom: 22px; padding: 0; border-top: 1px solid #F1F5F9; padding-top: 14px; }
.product-specs li { font-size: 0.85rem; color: #475569; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
.product-specs li::before { content: '✓'; color: var(--orange); font-weight: bold; }

.btn-group { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: auto; }
.btn-detail {
    background: #F1F5F9; color: var(--navy); border: 1px solid #CBD5E1;
    padding: 12px 18px; border-radius: 8px; font-weight: 700; font-size: 0.88em; cursor: pointer;
    transition: all 0.3s;
}
.btn-detail:hover { background: #E2E8F0; }
.btn-wa {
    background-color: #25D366; color: #FFF; border: none;
    padding: 12px 18px; border-radius: 8px; font-weight: 800; font-size: 0.88em;
    cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px;
    box-shadow: 0 4px 12px rgba(37,211,102,0.25); transition: all 0.3s ease;
}
.btn-wa:hover { background-color: #1EBE57; transform: translateY(-2px); box-shadow: 0 6px 18px rgba(37,211,102,0.4); }

/* SECCIONES Y FORMULARIO DE CONTACTO */
.contact-section-wrapper {
    display: grid; grid-template-columns: 1fr 1fr; gap: 45px;
    background: var(--white); padding: 50px; border-radius: 20px;
    box-shadow: var(--card-shadow); border: 1px solid rgba(0,0,0,0.06);
}
@media (max-width: 900px) { .contact-section-wrapper { grid-template-columns: 1fr; } }
.contact-form-group { margin-bottom: 20px; }
.contact-form-group label { display: block; font-weight: 700; margin-bottom: 8px; color: var(--navy); font-size: 0.92rem; }
.contact-form-input {
    width: 100%; padding: 14px 18px; border-radius: 8px; border: 1px solid #CBD5E1;
    font-size: 1rem; outline: none; transition: border-color 0.3s;
}
.contact-form-input:focus { border-color: var(--orange); }
.btn-submit-contact {
    background: linear-gradient(135deg, var(--orange), #FF8533); color: var(--white); border: none;
    padding: 16px 30px; border-radius: 8px; font-weight: 800; font-size: 1.05rem;
    cursor: pointer; width: 100%; box-shadow: 0 4px 15px rgba(255,102,0,0.3); transition: all 0.3s;
}
.btn-submit-contact:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255,102,0,0.5); }

/* FOOTER PROFESIONAL */
footer {
    background-color: var(--navy-dark); color: var(--white);
    padding: 85px 20px 40px; text-align: center; border-top: 5px solid var(--orange);
}
footer h2 { color: var(--orange); font-size: 2.2em; margin-bottom: 15px; }
footer .contact-info { margin: 38px 0; font-size: 1.12em; line-height: 2.3; }
footer .contact-info span { font-weight: 800; color: var(--orange); margin-right: 10px; }
.footer-bottom { margin-top: 55px; padding-top: 28px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.9em; color: #94A3B8; }
.bg-white { background-color: var(--white); }
.mt-5 { margin-top: 50px; }
"""

# HTML completo formateado de sitio web corporativo
INDEX_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YD Protección | Equipos de Seguridad & Prevención</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800;900&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>""" + EMBEDDED_CSS + """</style>
</head>
<body>

    <!-- TOPBAR / NAVBAR NAVEGACIÓN -->
    <header class="top-bar">
        <div class="container top-bar-content">
            <a href="/" class="brand-logo-group">
                <div class="brand-badge">YD</div>
                <div class="brand-title">PROTECCIÓN <span>EQUIPOS</span></div>
            </a>
            <nav class="nav-links">
                <a href="#quienes-somos">Quiénes Somos</a>
                <a href="#categorias">Categorías</a>
                <a href="#productos">Productos</a>
                <a href="#contacto">Contacto</a>
                <a href="/dashboard" class="btn-analytics">📊 Analítica</a>
            </nav>
        </div>
    </header>

    <!-- PORTADA / HERO PRINCIPAL -->
    <section class="hero">
        <div class="container">
            <span class="hero-tag">Seguridad que salva vidas ★ Yesika & Daniel</span>
            <h2>Seguridad y Emergencia a tu Alcance</h2>
            <h3>EQUIPOS DE PROTECCIÓN Y PREVENCIÓN</h3>
            <p>Soluciones especializadas para Defensa Civil, Brigadas de Emergencia, Protección Industrial y Dotación Institucional.</p>
            
            <div class="search-wrapper">
                <span class="search-icon">🔍</span>
                <input type="text" id="searchInput" class="search-input" placeholder="Buscar producto, casco, botiquín, chaleco, linterna..." summary="Buscador de productos">
            </div>
        </div>
    </section>

    <!-- SECCIÓN QUIÉNES SOMOS COMPLETA -->
    <section class="bg-white" id="quienes-somos">
        <div class="container">
            <h2 class="section-title">Quiénes Somos</h2>
            <p class="section-subtitle">Seguridad que salva vidas — Yesika & Daniel</p>
            
            <p style="text-align: center; max-width: 860px; margin: 0 auto 55px; font-size: 1.18em; color: var(--text-dark); line-height: 1.8;">
                <strong>YD Protección</strong> es una empresa dedicada al suministro de equipos y soluciones integrales de seguridad industrial, elementos de protección personal (EPP), brigadas de emergencia y respuesta en socorrismo. Acompañamos a industrias e instituciones con productos 100% normativos y asesoría técnica especializada.
            </p>
            
            <!-- MISIÓN Y VISIÓN -->
            <div class="grid-2" style="margin-bottom: 55px;">
                <div class="card-box">
                    <h4>🚀 Nuestra Misión</h4>
                    <p style="font-size: 1.05em; color: var(--text-dark);">
                        Suministrar equipos de protección, emergencia y prevención de la más alta calidad y normatividad, brindando asesoría integral a empresas, brigadas e instituciones de socorro para preservar la vida y controlar riesgos operacionales.
                    </p>
                </div>
                <div class="card-box navy-top">
                    <h4>👁️ Nuestra Visión</h4>
                    <p style="font-size: 1.05em; color: var(--text-dark);">
                        Ser reconocidos a nivel nacional como la empresa líder y aliada estratégica en soluciones de seguridad, prevención y atención de emergencias, destacándonos por la confiabilidad de nuestros productos, excelencia en el servicio y compromiso humano.
                    </p>
                </div>
            </div>

            <!-- VALORES CORPORATIVOS -->
            <h3 style="text-align: center; color: var(--navy); margin-bottom: 35px; font-size: 1.7em;">Valores Corporativos</h3>
            <div class="grid-4" style="margin-bottom: 65px;">
                <div class="card-box" style="padding: 30px 22px; border-top: 4px solid var(--orange);">
                    <h4 style="font-size: 1.15em; margin-bottom: 10px;">INTEGRIDAD</h4>
                    <p style="font-size: 0.94em; color: var(--text-light);">Transparencia, honestidad y ética en cada recomendación y producto entregado.</p>
                </div>
                <div class="card-box" style="padding: 30px 22px; border-top: 4px solid var(--navy);">
                    <h4 style="font-size: 1.15em; margin-bottom: 10px;">COMPROMISO</h4>
                    <p style="font-size: 0.94em; color: var(--text-light);">Priorizamos la salud y la vida humana sobre todo en cada operación.</p>
                </div>
                <div class="card-box" style="padding: 30px 22px; border-top: 4px solid var(--orange);">
                    <h4 style="font-size: 1.15em; margin-bottom: 10px;">NORMATIVIDAD</h4>
                    <p style="font-size: 0.94em; color: var(--text-light);">Equipos homologados bajo normas internacionales (ANSI, CE, ISO, EN).</p>
                </div>
                <div class="card-box" style="padding: 30px 22px; border-top: 4px solid var(--navy);">
                    <h4 style="font-size: 1.15em; margin-bottom: 10px;">EXCELENCIA</h4>
                    <p style="font-size: 0.94em; color: var(--text-light);">Acompañamiento técnico continuo y atención inmediata ante imprevistos.</p>
                </div>
            </div>

            <!-- POR QUÉ ESCOGERNOS -->
            <h3 style="text-align: center; color: var(--navy); margin-bottom: 35px; font-size: 1.7em;">¿Por Qué Escogernos?</h3>
            <div class="grid-4">
                <div class="card-box navy-top" style="text-align: center;">
                    <h4 style="font-size: 1.15em;">EQUIPOS CERTIFICADOS</h4>
                    <p style="font-size: 0.94em; color: var(--text-light);">Garantía de desempeño para tareas de alto riesgo operacional.</p>
                </div>
                <div class="card-box" style="text-align: center;">
                    <h4 style="font-size: 1.15em;">ASESORÍA ESPECIALIZADA</h4>
                    <p style="font-size: 0.94em; color: var(--text-light);">Te ayudamos a seleccionar según tu matriz de riesgo y sector industrial.</p>
                </div>
                <div class="card-box navy-top" style="text-align: center;">
                    <h4 style="font-size: 1.15em;">AGILIDAD Y LOGÍSTICA</h4>
                    <p style="font-size: 0.94em; color: var(--text-light);">Suministro oportuno para compras individuales y dotaciones institucionales.</p>
                </div>
                <div class="card-box" style="text-align: center;">
                    <h4 style="font-size: 1.15em;">PERSONALIZACIÓN</h4>
                    <p style="font-size: 0.94em; color: var(--text-light);">Bordados, parches y marcas corporativas a medida de tu institución.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- NUESTRAS CATEGORÍAS -->
    <section id="categorias">
        <div class="container">
            <h2 class="section-title">Nuestras Categorías</h2>
            <p class="section-subtitle">Selecciona una categoría para filtrar el catálogo al instante</p>
            
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

    <!-- PRODUCTOS EN EXHIBICIÓN CON FOTOS DE ALTA DEFINICIÓN -->
    <section class="bg-white" id="productos">
        <div class="container">
            <h2 class="section-title">Catálogo de Productos</h2>
            <p class="section-subtitle" id="productCountSub">{{ products|length }} productos disponibles en catálogo</p>
            
            <div class="product-grid mt-5" id="productGrid">
                {% for product in products %}
                <article class="product-card" data-id="{{ product.id }}" data-category="{{ product.category }}">
                    <div class="product-image-box">
                        <img src="{{ product.image }}" alt="{{ product.title }}" loading="lazy" onerror="this.src='{{ product.fallback_image }}'">
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

    <!-- BANNER DOTACIÓN Y PERSONALIZACIÓN -->
    <section class="dotacion-banner">
        <div class="container">
            <h2>DOTACIÓN Y PERSONALIZACIÓN</h2>
            <p style="font-size: 1.25em;">Lleva la identidad de tu equipo e institución a cada operación.</p>
            
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

    <!-- SECCIÓN CONTÁCTENOS COMPLETA -->
    <section id="contacto">
        <div class="container">
            <h2 class="section-title">Contáctenos</h2>
            <p class="section-subtitle">Estamos listos para atender tus requerimientos de seguridad</p>
            
            <div class="contact-section-wrapper">
                <!-- FORMULARIO DIRECTO -->
                <div>
                    <h3 style="color: var(--navy); margin-bottom: 22px; font-size: 1.4em;">Envíanos un Mensaje</h3>
                    <form id="contactForm" onsubmit="handleContactSubmit(event)">
                        <div class="contact-form-group">
                            <label for="cName">Nombre Completo / Empresa *</label>
                            <input type="text" id="cName" class="contact-form-input" placeholder="Tu nombre o empresa" required>
                        </div>
                        <div class="contact-form-group">
                            <label for="cPhone">Teléfono / WhatsApp *</label>
                            <input type="tel" id="cPhone" class="contact-form-input" placeholder="Ej: +57 300 123 4567" required>
                        </div>
                        <div class="contact-form-group">
                            <label for="cEmail">Correo Electrónico *</label>
                            <input type="email" id="cEmail" class="contact-form-input" placeholder="correo@ejemplo.com" required>
                        </div>
                        <div class="contact-form-group">
                            <label for="cProduct">Producto de Interés</label>
                            <select id="cProduct" class="contact-form-input">
                                <option value="Consulta General">Consulta General</option>
                                <option value="Casco Dieléctrico">Casco Dieléctrico</option>
                                <option value="Gafas de Seguridad">Gafas de Seguridad</option>
                                <option value="Guantes Tácticos">Guantes Tácticos</option>
                                <option value="Botiquín de Lona">Botiquín de Lona</option>
                                <option value="Linterna Táctica">Linterna Táctica</option>
                                <option value="Kit de Rescate">Kit de Rescate</option>
                                <option value="Chaleco Defensa Civil">Chaleco Defensa Civil</option>
                                <option value="Cono Vial 90cm">Cono Vial 90cm</option>
                                <option value="Megáfono 50W">Megáfono 50W</option>
                            </select>
                        </div>
                        <div class="contact-form-group">
                            <label for="cMsg">Mensaje *</label>
                            <textarea id="cMsg" class="contact-form-input" rows="4" placeholder="Describe los productos o cantidades que necesitas cotizar..." required></textarea>
                        </div>
                        <button type="submit" class="btn-submit-contact">💬 Enviar Solicitud por WhatsApp</button>
                    </form>
                </div>

                <!-- INFORMACIÓN DE CONTACTO -->
                <div style="background: var(--navy-dark); color: var(--white); padding: 40px; border-radius: 16px; display: flex; flex-direction: column; justify-content: center;">
                    <h3 style="color: var(--orange); margin-bottom: 25px; font-size: 1.5em;">Información Directa</h3>
                    
                    <div style="margin-bottom: 30px; font-size: 1.12em; line-height: 2.2;">
                        <p><strong style="color: var(--orange);">📱 WHATSAPP:</strong> +57 (300) 000-0000</p>
                        <p><strong style="color: var(--orange);">✉️ CORREO:</strong> contacto@ydproteccion.com</p>
                        <p><strong style="color: var(--orange);">📸 INSTAGRAM:</strong> @ydproteccion</p>
                        <p><strong style="color: var(--orange);">📍 UBICACIÓN:</strong> Medellín, Antioquia, Colombia</p>
                    </div>

                    <div style="background: rgba(255,102,0,0.15); border: 1px solid var(--orange); padding: 22px; border-radius: 12px;">
                        <h4 style="color: var(--orange); margin-bottom: 8px; font-size: 1.08em;">⏰ HORARIOS DE ATENCIÓN</h4>
                        <p style="font-size: 0.96em; color: #E2E8F0;">Lunes a Viernes: 8:00 AM – 6:00 PM<br>Sábados: 8:00 AM – 1:00 PM</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- FOOTER -->
    <footer>
        <div class="container">
            <h2>HABLEMOS DE TU SEGURIDAD</h2>
            <p>Solicita cotización y asesoría personalizada de inmediato</p>
            
            <div class="footer-bottom">
                <p>YESIKA & DANIEL | YD PROTECCIÓN &copy; 2026 — Todos los Derechos Reservados</p>
            </div>
        </div>
    </footer>

    <!-- LÓGICA INTERACTIVA -->
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
                    card.style.display = (matchCat && matchSearch) ? 'flex' : 'none';
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

        function handleContactSubmit(e) {
            e.preventDefault();
            const name = document.getElementById('cName').value;
            const phone = document.getElementById('cPhone').value;
            const email = document.getElementById('cEmail').value;
            const product = document.getElementById('cProduct').value;
            const msg = document.getElementById('cMsg').value;

            const text = `Hola *YD Protección*, mi nombre es *${name}*.\n\n` +
                         `📱 *Teléfono:* ${phone}\n` +
                         `✉️ *Correo:* ${email}\n` +
                         `📌 *Interés:* ${product}\n` +
                         `💬 *Mensaje:* ${msg}`;

            window.open(`https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(text)}`, '_blank');
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

# Dashboard HTML
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel de Analítica - YD Protección</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>""" + EMBEDDED_CSS + """</style>
</head>
<body>
    <div class="top-bar">
        <div class="container top-bar-content">
            <a href="/" class="brand-logo-group">
                <div class="brand-badge">YD</div>
                <div class="brand-title">PROTECCIÓN <span>ANALÍTICA</span></div>
            </a>
            <a href="/" class="btn-analytics">← Volver al Catálogo</a>
        </div>
    </div>
    <div class="container" style="padding: 65px 20px;">
        <h2 class="section-title">Métricas de Interés</h2>
        <div class="grid-2 mt-5">
            <div class="card-box">
                <h4>Total Vistas</h4>
                <div style="font-size: 2.8em; font-weight: 800; color: var(--orange);" id="totalViews">0</div>
            </div>
            <div class="card-box">
                <h4>Cotizaciones WhatsApp</h4>
                <div style="font-size: 2.8em; font-weight: 800; color: #25D366;" id="totalQuotes">0</div>
            </div>
        </div>
    </div>
    <script>
        fetch('/api/analytics').then(r=>r.json()).then(d=>{
            document.getElementById('totalViews').textContent = d.total_views || 0;
            document.getElementById('totalQuotes').textContent = d.total_quotes || 0;
        });
    </script>
</body>
</html>"""

METRICS_DATA = {"total_views": 0, "total_quotes": 0}

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
    return JSONResponse(content={"total_views": METRICS_DATA["total_views"], "total_quotes": METRICS_DATA["total_quotes"]})

@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, full_path: str):
    if full_path.startswith("api/"):
        return JSONResponse(status_code=404, content={"detail": "Not Found"})
    return await home_page(request)

handler = app
