import json
from typing import Optional, Dict
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Template

app = FastAPI(
    title="YD Protección - Sitio Web Oficial & CMS Admin",
    description="Plataforma Web Corporativa y Panel de Administración CMS para YD Protección",
    version="4.1.0"
)

# Catálogo oficial base de YD Protección
EMBEDDED_PRODUCTS = [
  {
    "id": "prod-001",
    "title": "Casco de Seguridad Industrial Tipo II Dieléctrico",
    "category": "proteccion_personal",
    "category_name": "Protección Personal",
    "short_description": "Casco dieléctrico de polietileno de alta densidad con suspensión de 4 puntos y ajuste de perilla.",
    "description": "Casco de seguridad de máxima resistencia contra impactos superiores y laterales. Cumple norma ANSI Z89.1 Clase E (hasta 20.000V). Incluye barboquejo reinforced y ranuras para protectores auditivos.",
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

# Lista de Servicios Profesionales
SERVICES_LIST = [
  {
    "id": "serv-01",
    "icon": "🛡️",
    "title": "Suministro de EPP Certificados",
    "desc": "Provisión integral de Elementos de Protección Personal (Cascos, Gafas, Guantes, Calzado, Protección Auditiva y Respiratoria) bajo normas ANSI, CE e ISO para todo sector industrial."
  },
  {
    "id": "serv-02",
    "icon": "🚨",
    "title": "Equipamiento para Brigadas de Emergencia",
    "desc": "Armado de kits integrales de respuesta rápida para brigadas empresariales e institucionales: Botiquines Tipo A/B/C, camillas espinales, megáfonos, linternas tácticas y extintores."
  },
  {
    "id": "serv-03",
    "icon": "🦺",
    "title": "Personalización, Bordados y Marca Institucional",
    "desc": "Confección y personalización de uniformes, chalecos tácticos, prendas reflectivas, parches en velcro y rotulación corporativa en cascos con el logo de tu organización."
  },
  {
    "id": "serv-04",
    "icon": "📐",
    "title": "Asesoría Técnica en Matriz de Riesgo",
    "desc": "Acompañamiento especializado para la correcta selección e inspección de equipos según el tipo de riesgo operacional y normativa legal vigente."
  },
  {
    "id": "serv-05",
    "icon": "🧗",
    "title": "Suministro e Inspección de Equipos de Rescate Vertical",
    "desc": "Venta y asesoramiento de arneses, cuerdas estáticas, mosquetones forjados y sistemas de anclaje para trabajos en alturas y socorrismo en espacios confinados."
  }
]

# Estilos CSS
EMBEDDED_CSS = """
:root {
    --navy: #0B1C30;
    --navy-dark: #050E1A;
    --orange: #FF6600;
    --orange-light: #FF8533;
    --orange-hover: #E65C00;
    --white: #FFFFFF;
    --light-bg: #F8FAFC;
    --text-dark: #0F172A;
    --text-muted: #64748B;
    --card-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
    --hover-shadow: 0 20px 40px -5px rgba(255, 102, 0, 0.22), 0 12px 20px -4px rgba(11, 28, 48, 0.12);
}

html { scroll-behavior: smooth; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: var(--light-bg);
    color: var(--text-dark);
    line-height: 1.6;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4, h5 { font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif; text-transform: uppercase; font-weight: 800; }
img { max-width: 100%; height: auto; display: block; }
.container { max-width: 1240px; margin: 0 auto; padding: 0 20px; }

/* HEADER / NAVBAR */
.top-bar {
    background: rgba(5, 14, 26, 0.96);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    color: var(--white);
    padding: 14px 0;
    border-bottom: 3px solid var(--orange);
    position: sticky; top: 0; z-index: 1000;
    box-shadow: 0 4px 25px rgba(0,0,0,0.3);
}
.top-bar-content {
    display: flex; justify-content: space-between; align-items: center; gap: 15px;
}
.brand-logo-group {
    display: flex; align-items: center; gap: 10px; text-decoration: none; cursor: pointer; flex-shrink: 0;
}
.brand-badge {
    background: linear-gradient(135deg, var(--orange), var(--orange-light));
    color: #FFF; font-family: 'Montserrat', sans-serif; font-weight: 900; font-size: 1.15rem;
    padding: 4px 10px; border-radius: 8px; box-shadow: 0 4px 12px rgba(255,102,0,0.3);
}
.brand-title { font-size: 1.25rem; font-weight: 900; letter-spacing: 0.5px; color: var(--white); }
.brand-title span { color: var(--orange); }

.nav-links { display: flex; gap: 18px; align-items: center; flex-wrap: wrap; }
.nav-link-btn {
    color: #E2E8F0; text-decoration: none; font-weight: 700; font-size: 0.9rem;
    transition: all 0.3s ease; position: relative; padding: 6px 2px; background: none; border: none; cursor: pointer; white-space: nowrap;
}
.nav-link-btn:hover, .nav-link-btn.active-page { color: var(--orange); }
.nav-link-btn::after {
    content: ''; position: absolute; bottom: 0; left: 0; width: 0; height: 3px;
    background: var(--orange); transition: width 0.3s ease; border-radius: 2px;
}
.nav-link-btn:hover::after, .nav-link-btn.active-page::after { width: 100%; }

.btn-analytics {
    background: linear-gradient(135deg, var(--orange), var(--orange-light));
    color: var(--white); padding: 8px 18px; border-radius: 50px; text-decoration: none;
    font-weight: 700; font-size: 0.85rem; box-shadow: 0 4px 14px rgba(255,102,0,0.35); transition: all 0.3s ease;
    white-space: nowrap; flex-shrink: 0; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;
}
.btn-analytics:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255,102,0,0.5); }

/* VISTAS */
.page-view { display: none; opacity: 0; transition: opacity 0.35s ease-in-out; }
.page-view.active-view { display: block; opacity: 1; }

/* HERO */
.hero {
    background: radial-gradient(circle at 50% 20%, rgba(255,102,0,0.12) 0%, rgba(5,14,26,1) 75%);
    color: var(--white); text-align: center; padding: 70px 20px 85px; position: relative; border-bottom: 1px solid rgba(255,255,255,0.08);
}
.hero-tag {
    display: inline-block; background: rgba(255,102,0,0.15); border: 1px solid var(--orange);
    color: var(--orange); padding: 6px 18px; border-radius: 50px; font-size: 0.8rem; font-weight: 800; letter-spacing: 1.2px; margin-bottom: 20px; text-transform: uppercase;
}
.hero h2 { font-size: clamp(1rem, 2.5vw, 1.4rem); font-weight: 400; letter-spacing: 2px; margin-bottom: 12px; color: #E2E8F0; }
.hero h3 { font-size: clamp(1.6rem, 5vw, 2.7rem); margin-bottom: 16px; text-shadow: 0 4px 15px rgba(0,0,0,0.4); color: var(--white); letter-spacing: -0.5px; line-height: 1.25; }
.hero p { font-size: clamp(1rem, 2.2vw, 1.2rem); max-width: 720px; margin: 0 auto 35px; color: #CBD5E1; line-height: 1.6; }

.search-wrapper { max-width: 640px; margin: 0 auto; position: relative; }
.search-input {
    width: 100%; padding: 16px 20px 16px 50px; border-radius: 50px; border: 2px solid var(--orange);
    background: #FFFFFF; font-size: 1rem; outline: none; box-shadow: 0 10px 30px rgba(0,0,0,0.3); transition: all 0.3s ease;
}
.search-input:focus { box-shadow: 0 0 30px rgba(255,102,0,0.5); }
.search-icon { position: absolute; left: 20px; top: 50%; transform: translateY(-50%); font-size: 1.15rem; }

/* SECCIONES Y ENCABEZADOS DE PÁGINA */
.page-header-banner {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-dark) 100%);
    color: var(--white); padding: 50px 20px; text-align: center; border-bottom: 4px solid var(--orange); margin-bottom: 35px;
}
.page-header-banner h1 { font-size: clamp(1.6rem, 4vw, 2.4rem); margin-bottom: 10px; color: var(--white); }
.page-header-banner p { font-size: clamp(0.95rem, 2vw, 1.15rem); color: #CBD5E1; max-width: 700px; margin: 0 auto; }

section { padding: 60px 0; }
.section-title {
    text-align: center; color: var(--navy); font-size: clamp(1.8rem, 4vw, 2.5rem);
    margin-bottom: 12px; position: relative; padding-bottom: 18px; letter-spacing: -0.5px;
}
.section-title::after {
    content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); width: 75px; height: 4px; background-color: var(--orange); border-radius: 4px;
}
.section-subtitle { text-align: center; font-size: clamp(0.95rem, 2vw, 1.15rem); color: var(--text-muted); margin-bottom: 40px; }

/* DESGLOSE Y GRILLAS */
.category-breakdown-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 24px; margin-top: 30px; }
.category-breakdown-card {
    background: var(--white); border-radius: 18px; padding: 28px 22px; box-shadow: var(--card-shadow);
    border: 1px solid rgba(0,0,0,0.06); border-top: 6px solid var(--orange); transition: all 0.35s ease;
}
.category-breakdown-card:hover { transform: translateY(-6px); box-shadow: var(--hover-shadow); }
.breakdown-num { display: inline-block; background: rgba(255,102,0,0.12); color: var(--orange); font-weight: 900; font-size: 1rem; padding: 4px 12px; border-radius: 50px; margin-bottom: 12px; }
.breakdown-title { color: var(--navy); font-size: 1.25em; margin-bottom: 10px; }
.breakdown-list { list-style: none; padding: 0; margin: 15px 0; }
.breakdown-list li { font-size: 0.9rem; color: var(--text-dark); margin-bottom: 8px; padding-left: 20px; position: relative; }
.breakdown-list li::before { content: '▶'; position: absolute; left: 0; color: var(--orange); font-size: 0.7rem; top: 3px; }

.grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 24px; }
.grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; }
.grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; }

.card-box {
    background: var(--white); padding: 32px 24px; border-radius: 16px; box-shadow: var(--card-shadow);
    border-top: 5px solid var(--orange); transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    border-left: 1px solid rgba(0,0,0,0.04); border-right: 1px solid rgba(0,0,0,0.04);
}
.card-box.navy-top { border-top: 5px solid var(--navy); }
.card-box:hover { transform: translateY(-6px); box-shadow: var(--hover-shadow); }
.card-box h4 { color: var(--navy); margin-bottom: 12px; font-size: 1.25em; }

.categories-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; }
.category-item {
    background-color: var(--navy); color: var(--white); padding: 22px; border-radius: 16px;
    display: flex; align-items: center; cursor: pointer; transition: all 0.35s ease; border-left: 5px solid transparent;
}
.category-item:hover, .category-item.active {
    background-color: #112844; border-left: 5px solid var(--orange); transform: translateX(6px); box-shadow: 0 10px 25px rgba(11,28,48,0.25);
}
.category-item .number { font-family: 'Montserrat', sans-serif; font-size: 2.2em; font-weight: 900; color: var(--orange); margin-right: 18px; flex-shrink: 0; }

.product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 26px; }
.product-card {
    background-color: var(--white); border-radius: 16px; overflow: hidden; box-shadow: var(--card-shadow);
    display: flex; flex-direction: column; transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1); border: 1px solid rgba(0,0,0,0.06);
}
.product-card:hover { transform: translateY(-8px); box-shadow: var(--hover-shadow); }
.product-image-box { background-color: #0F172A; height: 220px; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; }
.product-image-box img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s ease; }
.product-card:hover .product-image-box img { transform: scale(1.08); }
.product-badge { position: absolute; top: 12px; right: 12px; background: rgba(11, 28, 48, 0.92); border: 1px solid var(--orange); color: var(--orange); padding: 4px 12px; border-radius: 50px; font-size: 0.72rem; font-weight: 800; }
.product-info { padding: 22px 20px; flex-grow: 1; display: flex; flex-direction: column; }
.product-category-tag { color: var(--orange); font-size: 0.78rem; font-weight: 800; letter-spacing: 0.8px; margin-bottom: 5px; }
.product-info h4 { color: var(--navy); margin-bottom: 8px; font-size: 1.18em; line-height: 1.3; }
.product-info p { font-size: 0.92em; color: var(--text-muted); margin-bottom: 16px; flex-grow: 1; }
.product-specs { list-style: none; margin-bottom: 18px; padding: 0; border-top: 1px solid #F1F5F9; padding-top: 12px; }
.product-specs li { font-size: 0.82rem; color: #475569; margin-bottom: 5px; display: flex; align-items: center; gap: 6px; }
.product-specs li::before { content: '✓'; color: var(--orange); font-weight: bold; }

.btn-group { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: auto; }
.btn-detail { background: #F1F5F9; color: var(--navy); border: 1px solid #CBD5E1; padding: 10px 14px; border-radius: 8px; font-weight: 700; font-size: 0.84em; cursor: pointer; transition: all 0.3s; text-align: center; }
.btn-detail:hover { background: #E2E8F0; }
.btn-wa { background-color: #25D366; color: #FFF; border: none; padding: 10px 14px; border-radius: 8px; font-weight: 800; font-size: 0.84em; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 5px; box-shadow: 0 4px 12px rgba(37,211,102,0.25); transition: all 0.3s ease; }
.btn-wa:hover { background-color: #1EBE57; transform: translateY(-2px); box-shadow: 0 6px 18px rgba(37,211,102,0.4); }

/* MODAL */
.modal-backdrop { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); backdrop-filter: blur(6px); z-index: 2000; display: flex; align-items: center; justify-content: center; opacity: 0; pointer-events: none; transition: opacity 0.3s ease; }
.modal-backdrop.active { opacity: 1; pointer-events: all; }
.modal-card { background: #FFF; border-radius: 18px; width: 92%; max-width: 800px; padding: 30px 22px; position: relative; max-height: 90vh; overflow-y: auto; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.4); }
.modal-close { position: absolute; top: 14px; right: 16px; background: #F1F5F9; border: none; width: 36px; height: 36px; border-radius: 50%; font-size: 1.3rem; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background 0.3s; z-index: 10; }
.modal-close:hover { background: #E2E8F0; }

/* CONTÁCTENOS */
.contact-section-wrapper { display: grid; grid-template-columns: 1fr 1fr; gap: 35px; background: var(--white); padding: 45px 35px; border-radius: 20px; box-shadow: var(--card-shadow); border: 1px solid rgba(0,0,0,0.06); }
.contact-form-group { margin-bottom: 18px; }
.contact-form-group label { display: block; font-weight: 700; margin-bottom: 6px; color: var(--navy); font-size: 0.9rem; }
.contact-form-input { width: 100%; padding: 13px 16px; border-radius: 8px; border: 1px solid #CBD5E1; font-size: 0.96rem; outline: none; transition: border-color 0.3s; }
.contact-form-input:focus { border-color: var(--orange); }
.btn-submit-contact { background: linear-gradient(135deg, var(--orange), var(--orange-light)); color: var(--white); border: none; padding: 15px 24px; border-radius: 8px; font-weight: 800; font-size: 1rem; cursor: pointer; width: 100%; box-shadow: 0 4px 15px rgba(255,102,0,0.3); transition: all 0.3s; }
.btn-submit-contact:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255,102,0,0.5); }

/* TABLAS Y CMS ADMIN */
.admin-table { width: 100%; border-collapse: collapse; margin-top: 20px; background: var(--white); border-radius: 12px; overflow: hidden; box-shadow: var(--card-shadow); }
.admin-table th { background: var(--navy); color: var(--white); padding: 14px; text-align: left; font-size: 0.9rem; }
.admin-table td { padding: 14px; border-bottom: 1px solid #E2E8F0; font-size: 0.9rem; vertical-align: middle; }
.admin-table tr:hover { background: #F8FAFC; }
.badge-admin { padding: 4px 10px; border-radius: 50px; font-size: 0.75rem; font-weight: bold; background: rgba(255,102,0,0.12); color: var(--orange); }
.admin-sidebar { background: var(--navy-dark); color: var(--white); padding: 30px 20px; border-radius: 16px; }
.admin-menu { list-style: none; margin-top: 25px; padding: 0; }
.admin-menu-item { padding: 12px 18px; border-radius: 10px; margin-bottom: 8px; cursor: pointer; font-weight: 700; display: flex; align-items: center; gap: 10px; color: #CBD5E1; transition: all 0.3s; }
.admin-menu-item:hover, .admin-menu-item.active { background: var(--orange); color: var(--white); }

/* FOOTER */
footer { background-color: var(--navy-dark); color: var(--white); padding: 65px 20px 35px; text-align: center; border-top: 5px solid var(--orange); }
footer h2 { color: var(--orange); font-size: clamp(1.5rem, 3.5vw, 2.2rem); margin-bottom: 12px; }
.footer-bottom { margin-top: 45px; padding-top: 22px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.85em; color: #94A3B8; }
.bg-white { background-color: var(--white); }
.mt-5 { margin-top: 35px; }

@media (max-width: 860px) {
    .top-bar-content { flex-direction: column; align-items: stretch; gap: 12px; }
    .brand-logo-group { justify-content: center; }
    .nav-links { justify-content: center; overflow-x: auto; padding-bottom: 6px; -webkit-overflow-scrolling: touch; gap: 14px; }
    .btn-analytics { align-self: center; }
    .contact-section-wrapper { grid-template-columns: 1fr; padding: 30px 20px; }
}

@media (max-width: 600px) {
    .container { padding: 0 14px; }
    .hero { padding: 50px 14px 65px; }
    .hero h3 { font-size: 1.65rem; }
    .nav-link-btn { font-size: 0.84rem; padding: 4px 2px; }
    .search-input { font-size: 0.92rem; padding: 14px 16px 14px 44px; }
    .search-icon { left: 16px; font-size: 1rem; }
    .product-grid, .grid-2, .grid-3, .grid-4, .categories-grid, .category-breakdown-grid { grid-template-columns: 1fr; }
    .btn-group { grid-template-columns: 1fr; }
    .modal-card { padding: 24px 16px; }
}
"""

# Template HTML Completo con Integración Garantizada de Redirección e Interfaz Admin Integrada
INDEX_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YD Protección | Plataforma Web Oficial</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800;900&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>""" + EMBEDDED_CSS + """</style>
</head>
<body>

    <!-- TOPBAR CON NAVEGACIÓN COMPLETA -->
    <header class="top-bar">
        <div class="container top-bar-content">
            <div class="brand-logo-group" onclick="navigateToPage('home')">
                <div class="brand-badge">YD</div>
                <div class="brand-title">PROTECCIÓN <span>EQUIPOS</span></div>
            </div>
            <nav class="nav-links">
                <button class="nav-link-btn active-page" id="nav-home" onclick="navigateToPage('home')">Home</button>
                <button class="nav-link-btn" id="nav-quienes-somos" onclick="navigateToPage('quienes-somos')">Quiénes Somos</button>
                <button class="nav-link-btn" id="nav-categorias" onclick="navigateToPage('categorias')">Categorías</button>
                <button class="nav-link-btn" id="nav-tienda" onclick="navigateToPage('tienda')">Tienda</button>
                <button class="nav-link-btn" id="nav-servicios" onclick="navigateToPage('servicios')">Servicios</button>
                <button class="nav-link-btn" id="nav-contacto" onclick="navigateToPage('contacto')">Contacto</button>
            </nav>
            <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                <button class="btn-analytics" style="background: linear-gradient(135deg, var(--navy), #112844);" onclick="navigateToPage('admin')">⚙️ Panel Admin</button>
                <a href="/dashboard" class="btn-analytics">📊 Analítica</a>
            </div>
        </div>
    </header>

    <!-- ==================== PÁGINA 1: HOME ==================== -->
    <div id="page-home" class="page-view active-view">
        <section class="hero">
            <div class="container">
                <span class="hero-tag">Seguridad que salva vidas ★ Yesika & Daniel</span>
                <h2>Seguridad y Emergencia a tu Alcance</h2>
                <h3>EQUIPOS DE PROTECCIÓN Y PREVENCIÓN</h3>
                <p>Soluciones especializadas para Defensa Civil, Brigadas de Emergencia, Protección Industrial y Dotación Institucional.</p>
                
                <div class="search-wrapper">
                    <span class="search-icon">🔍</span>
                    <input type="text" class="search-input" id="searchHomeInput" placeholder="Buscar producto en la tienda (casco, botiquín, chaleco, linterna...)">
                </div>

                <div style="margin-top: 32px; display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
                    <button class="btn-analytics" style="padding: 13px 26px; font-size: 0.95rem; border-radius: 8px;" onclick="navigateToPage('categorias')">Ver Categorías y Desglose</button>
                    <button class="btn-analytics" style="padding: 13px 26px; font-size: 0.95rem; border-radius: 8px; background: linear-gradient(135deg, var(--navy), #112844);" onclick="navigateToPage('tienda')">Ir a la Tienda</button>
                    <button class="btn-detail" style="padding: 13px 26px; font-size: 0.95rem; border-radius: 8px;" onclick="navigateToPage('contacto')">Contactar Asesor</button>
                </div>
            </div>
        </section>

        <section class="bg-white">
            <div class="container">
                <h2 class="section-title">Soluciones Integrales</h2>
                <p class="section-subtitle">Atención inmediata a requerimientos de seguridad industrial y emergencias</p>
                
                <div class="grid-3 mt-5">
                    <div class="card-box" style="text-align: center;">
                        <h4 style="font-size: 1.25em;">PROTECCIÓN PERSONAL (EPP)</h4>
                        <p style="margin-bottom: 18px; color: var(--text-muted);">Cascos dieléctricos, gafas UV400, guantes anti-corte y protección auditiva certificada.</p>
                        <button class="btn-detail" style="width:100%;" onclick="navigateToPage('tienda', 'proteccion_personal')">Ver en Tienda</button>
                    </div>
                    <div class="card-box navy-top" style="text-align: center;">
                        <h4 style="font-size: 1.25em;">EMERGENCIAS & RESCATE</h4>
                        <p style="margin-bottom: 18px; color: var(--text-muted);">Botiquines Tipo B, linternas tácticas 2000 lúmenes y equipos verticales de rescate.</p>
                        <button class="btn-detail" style="width:100%;" onclick="navigateToPage('tienda', 'emergencias_rescate')">Ver en Tienda</button>
                    </div>
                    <div class="card-box" style="text-align: center;">
                        <h4 style="font-size: 1.25em;">DEFENSA CIVIL & BRIGADAS</h4>
                        <p style="margin-bottom: 18px; color: var(--text-muted);">Chalecos reflectivos 3M, conos viales 90cm, megáfonos 50W y dotación personalizada.</p>
                        <button class="btn-detail" style="width:100%;" onclick="navigateToPage('tienda', 'defensa_civil')">Ver en Tienda</button>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- ==================== PÁGINA 2: QUIÉNES SOMOS ==================== -->
    <div id="page-quienes-somos" class="page-view">
        <div class="page-header-banner">
            <div class="container">
                <h1>Quiénes Somos</h1>
                <p>Conoce la historia, Misión, Visión y Valores de Yesika & Daniel en YD Protección.</p>
            </div>
        </div>

        <section class="bg-white" style="padding-top: 15px;">
            <div class="container">
                <p style="text-align: center; max-width: 880px; margin: 0 auto 45px; font-size: 1.12em; color: var(--text-dark); line-height: 1.75;">
                    <strong>YD Protección</strong> es una empresa dedicada al suministro de equipos y soluciones integrales de seguridad industrial, elementos de protección personal (EPP), brigadas de emergencia y respuesta en socorrismo. Acompañamos a industrias e instituciones con productos 100% normativos y asesoría técnica especializada.
                </p>
                
                <div class="grid-2" style="margin-bottom: 45px;">
                    <div class="card-box">
                        <h4>🚀 Nuestra Misión</h4>
                        <p style="font-size: 1.02em; color: var(--text-dark);">
                            Suministrar equipos de protección, emergencia y prevención de la más alta calidad y normatividad, brindando asesoría integral a empresas, brigadas e instituciones de socorro para preservar la vida y controlar riesgos operacionales.
                        </p>
                    </div>
                    <div class="card-box navy-top">
                        <h4>👁️ Nuestra Visión</h4>
                        <p style="font-size: 1.02em; color: var(--text-dark);">
                            Ser reconocidos a nivel nacional como la empresa líder y aliada estratégica en soluciones de seguridad, prevención y atención de emergencias, destacándonos por la confiabilidad de nuestros productos, excelencia en el servicio y compromiso humano.
                        </p>
                    </div>
                </div>

                <h3 style="text-align: center; color: var(--navy); margin-bottom: 30px; font-size: 1.6em;">Valores Corporativos</h3>
                <div class="grid-4" style="margin-bottom: 50px;">
                    <div class="card-box" style="padding: 26px 20px; border-top: 4px solid var(--orange);">
                        <h4 style="font-size: 1.1em; margin-bottom: 8px;">INTEGRIDAD</h4>
                        <p style="font-size: 0.9em; color: var(--text-muted);">Transparencia, honestidad y ética en cada recomendación y producto entregado.</p>
                    </div>
                    <div class="card-box" style="padding: 26px 20px; border-top: 4px solid var(--navy);">
                        <h4 style="font-size: 1.1em; margin-bottom: 8px;">COMPROMISO</h4>
                        <p style="font-size: 0.9em; color: var(--text-muted);">Priorizamos la salud y la vida humana sobre todo en cada operación.</p>
                    </div>
                    <div class="card-box" style="padding: 26px 20px; border-top: 4px solid var(--orange);">
                        <h4 style="font-size: 1.1em; margin-bottom: 8px;">NORMATIVIDAD</h4>
                        <p style="font-size: 0.9em; color: var(--text-muted);">Equipos homologados bajo normas internacionales (ANSI, CE, ISO, EN).</p>
                    </div>
                    <div class="card-box" style="padding: 26px 20px; border-top: 4px solid var(--navy);">
                        <h4 style="font-size: 1.1em; margin-bottom: 8px;">EXCELENCIA</h4>
                        <p style="font-size: 0.9em; color: var(--text-muted);">Acompañamiento técnico continuo y atención inmediata ante imprevistos.</p>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- ==================== PÁGINA 3: CATEGORÍAS ==================== -->
    <div id="page-categorias" class="page-view">
        <div class="page-header-banner">
            <div class="container">
                <h1>Nuestras Categorías y Desglose Detallado</h1>
                <p>Explora el catálogo por líneas de protección y conoce los insumos, elementos y certificaciones específicas que incluye cada una</p>
            </div>
        </div>

        <section class="bg-white" style="padding-top: 10px;">
            <div class="container">
                <h2 class="section-title">Nuestras Categorías</h2>
                <p class="section-subtitle">Selecciona una categoría para filtrar los productos al instante en la tienda</p>

                <div class="categories-grid" style="margin-bottom: 50px;">
                    <div class="category-item active" onclick="navigateToPage('tienda', 'todos')">
                        <span class="number">00</span>
                        <div>
                            <h4 style="font-size: 1.1em;">TODOS LOS PRODUCTOS</h4>
                            <p style="font-size: 0.88em;">Catálogo general completo.</p>
                        </div>
                    </div>
                    <div class="category-item" onclick="navigateToPage('tienda', 'proteccion_personal')">
                        <span class="number">01</span>
                        <div>
                            <h4 style="font-size: 1.1em;">PROTECCIÓN PERSONAL</h4>
                            <p style="font-size: 0.88em;">Cascos dieléctricos, gafas UV, guantes tácticos y protección auditiva.</p>
                        </div>
                    </div>
                    <div class="category-item" onclick="navigateToPage('tienda', 'emergencias_rescate')">
                        <span class="number">02</span>
                        <div>
                            <h4 style="font-size: 1.1em;">EMERGENCIAS Y RESCATE</h4>
                            <p style="font-size: 0.88em;">Botiquines A/B/C, linternas tácticas, kits de rescate y cuerdas estáticas.</p>
                        </div>
                    </div>
                    <div class="category-item" onclick="navigateToPage('tienda', 'defensa_civil')">
                        <span class="number">03</span>
                        <div>
                            <h4 style="font-size: 1.1em;">DEFENSA CIVIL</h4>
                            <p style="font-size: 0.88em;">Dotación reglamentaria, chalecos 3M y elementos para brigadas.</p>
                        </div>
                    </div>
                    <div class="category-item" onclick="navigateToPage('tienda', 'senalizacion_seguridad')">
                        <span class="number">04</span>
                        <div>
                            <h4 style="font-size: 1.1em;">SEÑALIZACIÓN Y SEGURIDAD</h4>
                            <p style="font-size: 0.88em;">Conos flexibles de 90cm, cintas de prevención y paletas de control.</p>
                        </div>
                    </div>
                    <div class="category-item" onclick="navigateToPage('tienda', 'equipos_brigadas')">
                        <span class="number">05</span>
                        <div>
                            <h4 style="font-size: 1.1em;">EQUIPOS PARA BRIGADAS</h4>
                            <p style="font-size: 0.88em;">Megáfonos de 50W, estaciones lavaojos y equipos de evacuación.</p>
                        </div>
                    </div>
                    <div class="category-item" onclick="navigateToPage('tienda', 'dotacion_personalizada')">
                        <span class="number">06</span>
                        <div>
                            <h4 style="font-size: 1.1em;">DOTACIÓN PERSONALIZADA</h4>
                            <p style="font-size: 0.88em;">Uniformes normativos, parches bordados y marcas corporativas.</p>
                        </div>
                    </div>
                </div>

                <div style="border-top: 3px solid var(--orange); padding-top: 50px;">
                    <h2 class="section-title">Desglose Detallado por Categoría</h2>
                    <p class="section-subtitle">Conoce los insumos, elementos y certificaciones específicas que incluye cada línea de protección</p>

                    <div class="category-breakdown-grid">
                        <div class="category-breakdown-card">
                            <span class="breakdown-num">Categoría 01</span>
                            <h3 class="breakdown-title">Protección Personal (EPP)</h3>
                            <p style="color: var(--text-muted); font-size: 0.9rem;">Elementos de protección individual para resguardar la salud e integridad física del trabajador.</p>
                            <ul class="breakdown-list">
                                <li><strong>Protección de Cabeza:</strong> Cascos dieléctricos Tipo I y II Clase E (hasta 20.000V), barboquejos de 4 puntos y arneses de trinquete.</li>
                                <li><strong>Protección Visual & Facial:</strong> Gafas de policarbonato UV400, monogafas herméticas anti-empañantes y caretas de esmerilar.</li>
                                <li><strong>Protección Auditiva:</strong> Tapones de silicona con cordón reutilizables y protectores de copa tipo fono adaptables a casco.</li>
                                <li><strong>Protección Respiratoria:</strong> Respiradores de media cara de doble cartucho para vapores y mascarillas N95 / FFP2.</li>
                                <li><strong>Protección Manual:</strong> Guantes tácticos anti-corte Nivel 5, dieléctricos, nitrilo industrial y vaqueta.</li>
                            </ul>
                            <button class="btn-detail" style="width: 100%; margin-top: 10px;" onclick="navigateToPage('tienda', 'proteccion_personal')">Ver Productos EPP en Tienda</button>
                        </div>

                        <div class="category-breakdown-card" style="border-top-color: var(--navy);">
                            <span class="breakdown-num" style="background: rgba(11,28,48,0.12); color: var(--navy);">Categoría 02</span>
                            <h3 class="breakdown-title">Emergencias y Rescate</h3>
                            <p style="color: var(--text-muted); font-size: 0.9rem;">Equipamiento médico y operativo especializado para respuesta en contingencias y desastres.</p>
                            <ul class="breakdown-list">
                                <li><strong>Primeros Auxilios:</strong> Botiquines reglamentarios Tipo A, B y C confeccionados en lona tifón impermeable con insumos de curación.</li>
                                <li><strong>Inmovilización & Transporte:</strong> Camillas espinales rígidas plásticas en polietileno HDPE, inmovilizadores laterales y cuellos cervicales.</li>
                                <li><strong>Iluminación Operativa:</strong> Linternas tácticas LED 2000 lúmenes recargables por USB, contra impactos y certificación IPX8.</li>
                                <li><strong>Rescate Vertical:</strong> Cuerdas estáticas 11mm certificadas, arneses de cuerpo entero, mosquetones forjados 50kN y poleas.</li>
                            </ul>
                            <button class="btn-detail" style="width: 100%; margin-top: 10px;" onclick="navigateToPage('tienda', 'emergencias_rescate')">Ver Productos Rescate en Tienda</button>
                        </div>

                        <div class="category-breakdown-card">
                            <span class="breakdown-num">Categoría 03</span>
                            <h3 class="breakdown-title">Defensa Civil & Socorrismo</h3>
                            <p style="color: var(--text-muted); font-size: 0.9rem;">Dotación institucional y prendaje oficial para integrantes de brigadas y organismos de atención.</p>
                            <ul class="breakdown-list">
                                <li><strong>Indumentaria Operativa:</strong> Uniformes de trabajo y prendas en tela Ripstop antidesgarro de alta durabilidad.</li>
                                <li><strong>Visibilidad & Seguridad:</strong> Chalecos tácticos multibolsillos con cintas reflectivas microesféricas 3M de 2 pulgadas.</li>
                                <li><strong>Identificación Institucional:</strong> Parches bordados en velcro, insignias removibles de cargo y rotulación corporativa en cascos.</li>
                                <li><strong>Equipamiento de Campo:</strong> Fundas para radio de comunicación, mochilas de socorrista y cinturones de reata reforzados.</li>
                            </ul>
                            <button class="btn-detail" style="width: 100%; margin-top: 10px;" onclick="navigateToPage('tienda', 'defensa_civil')">Ver Productos Defensa Civil en Tienda</button>
                        </div>

                        <div class="category-breakdown-card" style="border-top-color: var(--navy);">
                            <span class="breakdown-num" style="background: rgba(11,28,48,0.12); color: var(--navy);">Categoría 04</span>
                            <h3 class="breakdown-title">Señalización & Seguridad Vial</h3>
                            <p style="color: var(--text-muted); font-size: 0.9rem;">Dispositivos físicos para delimitación, prevención y control de áreas de peligro.</p>
                            <ul class="breakdown-list">
                                <li><strong>Canalización Vial:</strong> Conos de PVC virgen flexible de 90 cm indeformables con doble cinta reflectiva High Intensity.</li>
                                <li><strong>Control de Tránsito:</strong> Paletas manuales Pare / Siga reflectivas y linternas de canalización para tráfico nocturno.</li>
                                <li><strong>Demarcación de Áreas:</strong> Cintas de señalización de peligro "Peligro No Pase" y "Precaución Obras".</li>
                                <li><strong>Señalización Fotoluminiscente:</strong> Avisos de rutas de evacuación, salidas de emergencia y extintores.</li>
                            </ul>
                            <button class="btn-detail" style="width: 100%; margin-top: 10px;" onclick="navigateToPage('tienda', 'senalizacion_seguridad')">Ver Productos Señalización en Tienda</button>
                        </div>

                        <div class="category-breakdown-card">
                            <span class="breakdown-num">Categoría 05</span>
                            <h3 class="breakdown-title">Equipos para Brigadas</h3>
                            <p style="color: var(--text-muted); font-size: 0.9rem;">Soluciones integrales de comunicación y control de contingencias en empresas e industrias.</p>
                            <ul class="breakdown-list">
                                <li><strong>Comunicación & Evacuación:</strong> Megáfonos profesionales de 50W con sirena de emergencia, grabador y alcance de 1000m.</li>
                                <li><strong>Higiene Industrial:</strong> Estaciones lavaojos portátiles por gravedad de 32 litros según norma ANSI Z358.1.</li>
                                <li><strong>Protección Incendio:</strong> Extintores multipropósito ABC, CO2 y Gabinetes de manguera contra incendio.</li>
                            </ul>
                            <button class="btn-detail" style="width: 100%; margin-top: 10px;" onclick="navigateToPage('tienda', 'equipos_brigadas')">Ver Productos Brigadas en Tienda</button>
                        </div>

                        <div class="category-breakdown-card" style="border-top-color: var(--navy);">
                            <span class="breakdown-num" style="background: rgba(11,28,48,0.12); color: var(--navy);">Categoría 06</span>
                            <h3 class="breakdown-title">Dotación Personalizada</h3>
                            <p style="color: var(--text-muted); font-size: 0.9rem;">Servicio completo de bordado, estampado e identidad de marca institucional.</p>
                            <ul class="breakdown-list">
                                <li><strong>Bordados Computarizados:</strong> Bordados en 3D de alta definición para camisetas, gorras, chaquetas y mochilas.</li>
                                <li><strong>Marcación de Cascos:</strong> Rotulación con vinilos reflectivos de alta adherencia y logos institucionales.</li>
                                <li><strong>Uniformes Corporativos:</strong> Overalls industriales, camisas y jeans de trabajo en dril normativo.</li>
                            </ul>
                            <button class="btn-detail" style="width: 100%; margin-top: 10px;" onclick="navigateToPage('contacto')">Solicitar Personalización</button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- ==================== PÁGINA 4: TIENDA ==================== -->
    <div id="page-tienda" class="page-view">
        <div class="page-header-banner">
            <div class="container">
                <h1>Tienda Oficial YD Protección</h1>
                <p>Explora nuestras referencias normativas con ficha técnica y opción de cotización directa por WhatsApp</p>
                
                <div class="search-wrapper" style="margin-top: 20px;">
                    <span class="search-icon">🔍</span>
                    <input type="text" class="search-input" id="searchCatalogInput" placeholder="Buscar producto en tienda por nombre, norma o palabra clave...">
                </div>
            </div>
        </div>

        <section class="bg-white" style="padding-top: 10px;">
            <div class="container">
                <h3 style="color: var(--navy); margin-bottom: 20px; text-align: center;">Filtrar Productos en Tienda</h3>
                <div class="categories-grid" id="categoriesGrid" style="margin-bottom: 40px;">
                    <div class="category-item active" data-category="todos" onclick="filterCatalogCategory('todos', this)">
                        <span class="number">00</span>
                        <div>
                            <h4 style="font-size: 1.05em;">TODOS LOS PRODUCTOS</h4>
                            <p style="font-size: 0.85em;">Catálogo general completo.</p>
                        </div>
                    </div>
                    <div class="category-item" data-category="proteccion_personal" onclick="filterCatalogCategory('proteccion_personal', this)">
                        <span class="number">01</span>
                        <div>
                            <h4 style="font-size: 1.05em;">PROTECCIÓN PERSONAL</h4>
                            <p style="font-size: 0.85em;">Cascos dieléctricos, gafas UV, guantes tácticos y protección auditiva.</p>
                        </div>
                    </div>
                    <div class="category-item" data-category="emergencias_rescate" onclick="filterCatalogCategory('emergencias_rescate', this)">
                        <span class="number">02</span>
                        <div>
                            <h4 style="font-size: 1.05em;">EMERGENCIAS Y RESCATE</h4>
                            <p style="font-size: 0.85em;">Botiquines A/B/C, linternas tácticas, kits de rescate y cuerdas estáticas.</p>
                        </div>
                    </div>
                    <div class="category-item" data-category="defensa_civil" onclick="filterCatalogCategory('defensa_civil', this)">
                        <span class="number">03</span>
                        <div>
                            <h4 style="font-size: 1.05em;">DEFENSA CIVIL</h4>
                            <p style="font-size: 0.85em;">Dotación reglamentaria, chalecos 3M y elementos para brigadas.</p>
                        </div>
                    </div>
                    <div class="category-item" data-category="senalizacion_seguridad" onclick="filterCatalogCategory('senalizacion_seguridad', this)">
                        <span class="number">04</span>
                        <div>
                            <h4 style="font-size: 1.05em;">SEÑALIZACIÓN Y SEGURIDAD</h4>
                            <p style="font-size: 0.85em;">Conos flexibles de 90cm, cintas de prevención y paletas de control.</p>
                        </div>
                    </div>
                    <div class="category-item" data-category="equipos_brigadas" onclick="filterCatalogCategory('equipos_brigadas', this)">
                        <span class="number">05</span>
                        <div>
                            <h4 style="font-size: 1.05em;">EQUIPOS PARA BRIGADAS</h4>
                            <p style="font-size: 0.85em;">Megáfonos de 50W, estaciones lavaojos y equipos de evacuación.</p>
                        </div>
                    </div>
                </div>

                <div class="product-grid" id="productGrid">
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
    </div>

    <!-- ==================== PÁGINA 5: SERVICIOS ==================== -->
    <div id="page-servicios" class="page-view">
        <div class="page-header-banner">
            <div class="container">
                <h1>Nuestros Servicios</h1>
                <p>Soluciones integrales de asesoría, equipamiento y personalización en seguridad para tu empresa o institución</p>
            </div>
        </div>

        <section class="bg-white" style="padding-top: 15px;">
            <div class="container">
                <div class="grid-3">
                    {% for serv in services %}
                    <div class="card-box">
                        <div style="font-size: 2.5rem; margin-bottom: 12px;">{{ serv.icon }}</div>
                        <h4>{{ serv.title }}</h4>
                        <p style="color: var(--text-muted);">{{ serv.desc }}</p>
                        <button class="btn-analytics" style="margin-top: 18px; width:100%; text-align:center;" onclick="navigateToPage('contacto')">Solicitar Asesoría</button>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </section>
    </div>

    <!-- ==================== PÁGINA 6: CONTACTO ==================== -->
    <div id="page-contacto" class="page-view">
        <div class="page-header-banner">
            <div class="container">
                <h1>Contacto</h1>
                <p>Solicita asesoría personalizada, listas de precios y pedidos institucionales de inmediato</p>
            </div>
        </div>

        <section style="padding-top: 15px;">
            <div class="container">
                <div class="contact-section-wrapper">
                    <div>
                        <h3 style="color: var(--navy); margin-bottom: 18px; font-size: 1.3em;">Envíanos un Mensaje</h3>
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
                                <label for="cProduct">Producto o Servicio de Interés</label>
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
                                    <option value="Servicio de Bordado y Personalización">Servicio de Bordado y Personalización</option>
                                    <option value="Asesoría en Matriz de Riesgo">Asesoría en Matriz de Riesgo</option>
                                </select>
                            </div>
                            <div class="contact-form-group">
                                <label for="cMsg">Mensaje *</label>
                                <textarea id="cMsg" class="contact-form-input" rows="4" placeholder="Describe los productos, servicios o cantidades que necesitas cotizar..." required></textarea>
                            </div>
                            <button type="submit" class="btn-submit-contact">💬 Enviar Solicitud por WhatsApp</button>
                        </form>
                    </div>

                    <div style="background: var(--navy-dark); color: var(--white); padding: 32px 24px; border-radius: 16px; display: flex; flex-direction: column; justify-content: center;">
                        <h3 style="color: var(--orange); margin-bottom: 20px; font-size: 1.4em;">Información Directa</h3>
                        
                        <div style="margin-bottom: 24px; font-size: 1.05em; line-height: 2.1;">
                            <p><strong style="color: var(--orange);">📱 WHATSAPP:</strong> +57 (300) 000-0000</p>
                            <p><strong style="color: var(--orange);">✉️ CORREO:</strong> contacto@ydproteccion.com</p>
                            <p><strong style="color: var(--orange);">📸 INSTAGRAM:</strong> @ydproteccion</p>
                            <p><strong style="color: var(--orange);">📍 UBICACIÓN:</strong> Medellín, Antioquia, Colombia</p>
                        </div>

                        <div style="background: rgba(255,102,0,0.15); border: 1px solid var(--orange); padding: 18px; border-radius: 12px;">
                            <h4 style="color: var(--orange); margin-bottom: 6px; font-size: 1em;">⏰ HORARIOS DE ATENCIÓN</h4>
                            <p style="font-size: 0.92em; color: #E2E8F0;">Lunes a Viernes: 8:00 AM – 6:00 PM<br>Sábados: 8:00 AM – 1:00 PM</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- ==================== PÁGINA 7: VISTA ADMIN INTEGRADA ==================== -->
    <div id="page-admin" class="page-view">
        <div class="page-header-banner">
            <div class="container">
                <h1>Panel de Administración CMS</h1>
                <p>Gestiona productos, categorías, servicios y métricas del sitio web</p>
            </div>
        </div>

        <section class="bg-white" style="padding-top: 15px;">
            <div class="container">
                <!-- MODAL LOGIN ADMIN -->
                <div id="loginOverlay" style="background: var(--navy-dark); color: var(--white); padding: 35px; border-radius: 20px; max-width: 440px; margin: 0 auto 40px; text-align: center; border-top: 5px solid var(--orange);">
                    <div class="brand-badge" style="display: inline-block; margin-bottom: 12px;">YD</div>
                    <h3 style="color: #FFF; margin-bottom: 6px;">ACCESO ADMINISTRATIVO</h3>
                    <p style="color: #CBD5E1; font-size: 0.88rem; margin-bottom: 22px;">Ingresa tus credenciales para editar el contenido</p>

                    <form onsubmit="handleAdminLogin(event)">
                        <div style="margin-bottom: 14px; text-align: left;">
                            <label style="font-weight:700; font-size:0.82rem; color:var(--orange);">USUARIO</label>
                            <input type="text" id="admUser" class="contact-form-input" required placeholder="admin" value="admin">
                        </div>
                        <div style="margin-bottom: 20px; text-align: left;">
                            <label style="font-weight:700; font-size:0.82rem; color:var(--orange);">CONTRASEÑA</label>
                            <input type="password" id="admPass" class="contact-form-input" required placeholder="••••••••" value="yd2026">
                        </div>
                        <button type="submit" class="btn-submit-contact">🔑 Iniciar Sesión CMS</button>
                    </form>
                </div>

                <!-- CONTENIDO ADMIN (VISIBLE TRAS LOGIN) -->
                <div id="adminMainContent" style="display: none;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; margin-bottom: 25px;">
                        <div>
                            <h3 style="color: var(--navy); font-size: 1.5rem;">Catálogo de Productos</h3>
                            <p style="color: var(--text-muted); font-size: 0.9rem;">Agrega o elimina productos del catálogo</p>
                        </div>
                        <button class="btn-analytics" style="padding: 12px 22px;" onclick="openProductFormModal()">➕ Agregar Producto</button>
                    </div>

                    <div style="overflow-x: auto;">
                        <table class="admin-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Imagen</th>
                                    <th>Título</th>
                                    <th>Categoría</th>
                                    <th>Insignia</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody id="adminProductsTable">
                                {% for p in products %}
                                <tr id="row-{{ p.id }}">
                                    <td><strong>{{ p.id }}</strong></td>
                                    <td><img src="{{ p.image }}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 8px;" onerror="this.src='{{ p.fallback_image }}'"></td>
                                    <td><strong>{{ p.title }}</strong></td>
                                    <td><span class="badge-admin">{{ p.category_name }}</span></td>
                                    <td><span style="font-size:0.8rem; font-weight:bold; color:var(--orange);">{{ p.badge or '-' }}</span></td>
                                    <td>
                                        <button class="btn-detail" style="padding: 6px 10px; font-size: 0.78rem;" onclick="deleteProduct('{{ p.id }}')">🗑️ Eliminar</button>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- MODAL AGREGAR PRODUCTO -->
    <div class="modal-backdrop" id="productModal">
        <div class="modal-card">
            <button class="modal-close" onclick="closeProductModal()">&times;</button>
            <h3 id="pFormTitle" style="color: var(--navy); margin-bottom: 18px;">Agregar Producto al Catálogo</h3>
            
            <form id="productForm" onsubmit="saveProduct(event)">
                <input type="hidden" id="pId">
                <div class="contact-form-group">
                    <label>Título del Producto *</label>
                    <input type="text" id="pTitle" class="contact-form-input" required placeholder="Ej: Casco Dieléctrico Especial">
                </div>
                <div class="contact-form-group">
                    <label>Categoría *</label>
                    <select id="pCategory" class="contact-form-input" required>
                        <option value="proteccion_personal">Protección Personal</option>
                        <option value="emergencias_rescate">Emergencias y Rescate</option>
                        <option value="defensa_civil">Defensa Civil & Brigadas</option>
                        <option value="senalizacion_seguridad">Señalización y Seguridad</option>
                        <option value="equipos_brigadas">Equipos para Brigadas</option>
                        <option value="dotacion_personalizada">Dotación Personalizada</option>
                    </select>
                </div>
                <div class="contact-form-group">
                    <label>Ruta de la Imagen o URL *</label>
                    <input type="text" id="pImage" class="contact-form-input" required placeholder="/images/casco_industrial.jpg">
                </div>
                <div class="contact-form-group">
                    <label>Descripción Corta *</label>
                    <input type="text" id="pShortDesc" class="contact-form-input" required placeholder="Resumen del producto...">
                </div>
                <button type="submit" class="btn-submit-contact">💾 Guardar Producto</button>
            </form>
        </div>
    </div>

    <!-- MODAL PRODUCTO -->
    <div class="modal-backdrop" id="modalBackdrop">
        <div class="modal-card">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 22px;">
                <div style="height: 240px; border-radius: 14px; overflow: hidden; background: #000;">
                    <img id="mImg" src="" style="width:100%; height:100%; object-fit:cover;">
                </div>
                <div>
                    <span id="mCat" class="product-category-tag">CATEGORÍA</span>
                    <h3 id="mTitle" style="color: var(--navy); margin-bottom: 8px; font-size: 1.3rem;">Título del producto</h3>
                    <p id="mDesc" style="color: var(--text-muted); font-size: 0.92rem; margin-bottom: 16px; line-height: 1.5;">Descripción del producto</p>
                    
                    <h4 style="color: var(--orange); font-size: 0.88rem; margin-bottom: 8px;">ESPECIFICACIONES TÉCNICAS:</h4>
                    <ul id="mSpecs" class="product-specs"></ul>

                    <button id="mBtnWa" class="btn-wa" style="width: 100%; padding: 13px; font-size: 0.95rem; margin-top: 15px;">
                        Solicitar Cotización por WhatsApp
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <footer>
        <div class="container">
            <h2>HABLEMOS DE TU SEGURIDAD</h2>
            <p style="font-size: clamp(0.9rem, 2vw, 1.1rem);">Solicita cotización y asesoría personalizada de inmediato</p>
            
            <div class="footer-bottom">
                <p>YESIKA & DANIEL | YD PROTECCIÓN &copy; 2026 — Todos los Derechos Reservados</p>
            </div>
        </div>
    </footer>

    <!-- SCRIPT DE NAVEGACIÓN Y ACCIÓN DE REDIRECCIÓN 100% GARANTIZADA -->
    <script>
        const WHATSAPP_PHONE = '573000000000';
        const productsData = """ + json.dumps(EMBEDDED_PRODUCTS) + """;

        function navigateToPage(pageId, categoryFilter = null) {
            document.querySelectorAll('.page-view').forEach(view => {
                view.classList.remove('active-view');
            });
            document.querySelectorAll('.nav-link-btn').forEach(btn => {
                btn.classList.remove('active-page');
            });

            const targetPage = document.getElementById('page-' + pageId);
            const targetBtn = document.getElementById('nav-' + pageId);

            if (targetPage) {
                targetPage.classList.add('active-view');
            }
            if (targetBtn) {
                targetBtn.classList.add('active-page');
            }

            window.scrollTo({ top: 0, behavior: 'smooth' });

            if (categoryFilter) {
                filterCatalogCategory(categoryFilter);
            }
        }

        function filterCatalogCategory(cat, element = null) {
            if (element) {
                document.querySelectorAll('#categoriesGrid .category-item').forEach(item => {
                    item.classList.remove('active');
                });
                element.classList.add('active');
            }

            const productCards = document.querySelectorAll('#productGrid .product-card');
            productCards.forEach(card => {
                const c = card.getAttribute('data-category');
                card.style.display = (cat === 'todos' || c === cat) ? 'flex' : 'none';
            });
        }

        function handleAdminLogin(e) {
            e.preventDefault();
            const u = document.getElementById('admUser').value;
            const p = document.getElementById('admPass').value;
            if (u === 'admin' && p === 'yd2026') {
                document.getElementById('loginOverlay').style.display = 'none';
                document.getElementById('adminMainContent').style.display = 'block';
                sessionStorage.setItem('yd_admin_logged', 'true');
            } else {
                alert('Credenciales incorrectas');
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            if (sessionStorage.getItem('yd_admin_logged') === 'true') {
                const overlay = document.getElementById('loginOverlay');
                const content = document.getElementById('adminMainContent');
                if (overlay) overlay.style.display = 'none';
                if (content) content.style.display = 'block';
            }

            // Detectar si la URL termina en /admin
            if (window.location.pathname.includes('/admin')) {
                navigateToPage('admin');
            }

            const searchHomeInput = document.getElementById('searchHomeInput');
            const searchCatalogInput = document.getElementById('searchCatalogInput');

            function handleSearch(query) {
                navigateToPage('tienda');
                const productCards = document.querySelectorAll('#productGrid .product-card');
                productCards.forEach(card => {
                    const text = card.textContent.toLowerCase();
                    card.style.display = text.includes(query.toLowerCase().trim()) ? 'flex' : 'none';
                });
            }

            if (searchHomeInput) {
                searchHomeInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') handleSearch(e.target.value);
                });
            }
            if (searchCatalogInput) {
                searchCatalogInput.addEventListener('input', (e) => {
                    handleSearch(e.target.value);
                });
            }
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

        function openProductFormModal() {
            document.getElementById('productModal').classList.add('active');
        }

        function closeProductModal() {
            document.getElementById('productModal').classList.remove('active');
        }

        function saveProduct(e) {
            e.preventDefault();
            const title = document.getElementById('pTitle').value;
            const category = document.getElementById('pCategory').value;
            const image = document.getElementById('pImage').value;
            const shortDesc = document.getElementById('pShortDesc').value;

            alert('Producto "' + title + '" guardado exitosamente en el panel CMS.');
            closeProductModal();
        }

        function deleteProduct(id) {
            if (confirm('¿Estás seguro de eliminar el producto ' + id + '?')) {
                const row = document.getElementById('row-' + id);
                if (row) row.remove();
                alert('Producto ' + id + ' eliminado.');
            }
        }

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

METRICS_DATA = {"total_views": 0, "total_quotes": 0}

@app.get("/")
@app.get("/home")
@app.get("/quienes-somos")
@app.get("/categorias")
@app.get("/tienda")
@app.get("/servicios")
@app.get("/contacto")
@app.get("/admin")
@app.get("/api")
@app.get("/api/index")
@app.get("/api/index.py")
async def main_site_pages(request: Request):
    try:
        rendered = Template(INDEX_HTML).render(products=EMBEDDED_PRODUCTS, services=SERVICES_LIST)
        return HTMLResponse(content=rendered)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error renderizando sitio web</h1><p>{str(e)}</p>")

@app.get("/dashboard")
@app.get("/api/dashboard")
async def dashboard_page(request: Request):
    return await main_site_pages(request)

@app.get("/api/products")
async def get_products(category: Optional[str] = None, q: Optional[str] = None):
    products = EMBEDDED_PRODUCTS
    if category and category != "todos":
        products = [p for p in products if p.get("category") == category]
    if q:
        query_lower = q.lower().strip()
        products = [p for p in products if query_lower in p.get("title", "").lower() or query_lower in p.get("short_description", "").lower()]
    return JSONResponse(content={"status": "success", "count": len(products), "products": products})

@app.post("/api/admin/products")
async def create_product(product: Dict):
    EMBEDDED_PRODUCTS.insert(0, product)
    return JSONResponse(content={"status": "success", "message": "Producto creado", "product": product})

@app.put("/api/admin/products/{product_id}")
async def update_product(product_id: str, product: Dict):
    for i, p in enumerate(EMBEDDED_PRODUCTS):
        if p["id"] == product_id:
            EMBEDDED_PRODUCTS[i] = product
            return JSONResponse(content={"status": "success", "message": "Producto actualizado"})
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.delete("/api/admin/products/{product_id}")
async def delete_product(product_id: str):
    global EMBEDDED_PRODUCTS
    EMBEDDED_PRODUCTS = [p for p in EMBEDDED_PRODUCTS if p["id"] != product_id]
    return JSONResponse(content={"status": "success", "message": "Producto eliminado"})

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
    return await main_site_pages(request)

handler = app
