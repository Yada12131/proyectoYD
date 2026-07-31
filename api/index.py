import json
import os
from typing import Optional, Dict, List
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Template

app = FastAPI(
    title="YD Protección - Plataforma Web & CMS Ejecutivo 12.0",
    description="Plataforma Web Corporativa con Dashboard CMS de Nivel Ejecutivo, Métricas en Tiempo Real y Sincronización Supabase Cloud Engine",
    version="12.0.0"
)

# DATOS BASE PARAMETRIZADOS INICIALES TOTALES
INITIAL_SITE_DATA = {
  "company": {
    "brand_name": "YD PROTECCIÓN",
    "brand_subtitle": "EQUIPOS",
    "logo_image": "",
    "hero_tag": "Seguridad que salva vidas ★ Yesika & Daniel",
    "hero_subtitle": "Seguridad y Emergencia a tu Alcance",
    "hero_title": "EQUIPOS DE PROTECCIÓN Y PREVENCIÓN",
    "hero_desc": "Soluciones especializadas para Defensa Civil, Brigadas de Emergencia, Protección Industrial y Dotación Institucional.",
    "about_intro": "YD Protección es una empresa dedicada al suministro de equipos y soluciones integrales de seguridad industrial, elementos de protección personal (EPP), brigadas de emergencia y respuesta en socorrismo. Acompañamos a industrias e instituciones con productos 100% normativos y asesoría técnica especializada.",
    "mision": "Suministrar equipos de protección, emergencia y prevención de la más alta calidad y normatividad, brindando asesoría integral a empresas, brigadas e instituciones de socorro para preservar la vida y controlar riesgos operacionales.",
    "vision": "Ser reconocidos a nivel nacional como la empresa líder y aliada estratégica en soluciones de seguridad, prevención y atención de emergencias, destacándonos por la confiabilidad de nuestros productos, excelencia en el servicio y compromiso humano."
  },
  "preloader": {
    "bg_gradient": "linear-gradient(135deg, #000000 0%, #2D3748 50%, #1A202C 100%)",
    "title": "YD PROTECCIÓN",
    "subtitle": "Cargando plataforma de seguridad...",
    "duration_ms": 4500
  },
  "footer": {
    "title": "HABLEMOS DE TU SEGURIDAD",
    "subtitle": "Solicita cotización y asesoría personalizada de inmediato",
    "copyright": "YESIKA & DANIEL | YD PROTECCIÓN © 2026 — Todos los Derechos Reservados"
  },
  "nav_links": [
    { "id": "home", "label": "Home", "enabled": True, "is_button": False },
    { "id": "quienes-somos", "label": "Quiénes Somos", "enabled": True, "is_button": False },
    { "id": "categorias", "label": "Categorías", "enabled": True, "is_button": False },
    { "id": "tienda", "label": "Tienda", "enabled": True, "is_button": False },
    { "id": "servicios", "label": "Servicios", "enabled": True, "is_button": False },
    { "id": "contacto", "label": "Contacto", "enabled": True, "is_button": False },
    { "id": "admin", "label": "⚙️ Panel Admin CMS", "enabled": False, "is_button": True },
    { "id": "analytics", "label": "📊 Analítica", "enabled": False, "is_button": True, "url": "/dashboard" }
  ],
  "custom_sections": [
    {
      "id": "garantias",
      "nav_id": "garantias",
      "title": "Políticas de Garantía y Normatividad",
      "subtitle": "Respaldamos la calidad de todos nuestros equipos de protección con certificaciones nacionales e internacionales",
      "content": "Todos los elementos suministrados por YD Protección cuentan con ficha técnica oficial, certificación de fabricante y garantía directa por defectos de fabricación. Realizamos inspección previa de lotes para asegurar el cumplimiento estricto de las normas ANSI, CE, OSHA e ICONTEC."
    }
  ],
  "contact": {
    "whatsapp": "573000000000",
    "whatsapp_display": "+57 (300) 000-0000",
    "email": "contacto@ydproteccion.com",
    "instagram": "@ydproteccion",
    "location": "Medellín, Antioquia, Colombia",
    "schedule": "Lunes a Viernes: 8:00 AM – 6:00 PM | Sábados: 8:00 AM – 1:00 PM"
  },
  "categories_breakdown": [
    {
      "id": "cat-01",
      "num": "Categoría 01",
      "code": "proteccion_personal",
      "title": "Protección Personal (EPP)",
      "desc": "Elementos de protección individual para resguardar la salud e integridad física del trabajador.",
      "items": [
        "Protección de Cabeza: Cascos dieléctricos Tipo I y II Clase E (hasta 20.000V).",
        "Protección Visual & Facial: Gafas de policarbonato UV400 y caretas de esmerilar.",
        "Protección Auditiva: Tapones de silicona con cordón y protectores tipo copa.",
        "Protección Respiratoria: Respiradores de media cara y mascarillas N95 / FFP2.",
        "Protección Manual: Guantes tácticos anti-corte Nivel 5 y dieléctricos."
      ]
    },
    {
      "id": "cat-02",
      "num": "Categoría 02",
      "code": "emergencias_rescate",
      "title": "Emergencias y Rescate",
      "desc": "Equipamiento médico y operativo especializado para respuesta en contingencias y desastres.",
      "items": [
        "Primeros Auxilios: Botiquines reglamentarios Tipo A, B y C en lona tifón.",
        "Inmovilización: Camillas espinales rígidas HDPE e inmovilizadores cervicales.",
        "Iluminación Operativa: Linternas tácticas LED 2000 lúmenes IPX8.",
        "Rescate Vertical: Cuerdas estáticas 11mm, arneses y mosquetones 50kN."
      ]
    },
    {
      "id": "cat-03",
      "num": "Categoría 03",
      "code": "defensa_civil",
      "title": "Defensa Civil & Socorrismo",
      "desc": "Dotación institucional y prendaje oficial para integrantes de brigadas y organismos de atención.",
      "items": [
        "Indumentaria Operativa: Uniformes de trabajo y prendas en tela Ripstop.",
        "Visibilidad: Chalecos tácticos multibolsillos con cintas reflectivas 3M.",
        "Identificación: Parches bordados en velcro y rotulación corporativa en cascos.",
        "Equipamiento: Fundas para radio, mochilas socorrista y cinturones reinforced."
      ]
    },
    {
      "id": "cat-04",
      "num": "Categoría 04",
      "code": "senalizacion_seguridad",
      "title": "Señalización & Seguridad Vial",
      "desc": "Dispositivos físicos para delimitación, prevención y control de áreas de peligro.",
      "items": [
        "Canalización Vial: Conos de PVC virgen flexible de 90 cm indeformables.",
        "Control de Tránsito: Paletas manuales Pare / Siga reflectivas.",
        "Demarcación: Cintas de señalización 'Peligro No Pase' y 'Precaución'.",
        "Señalización Fotoluminiscente: Avisos de rutas de evacuación y extintores."
      ]
    },
    {
      "id": "cat-05",
      "num": "Categoría 05",
      "code": "equipos_brigadas",
      "title": "Equipos para Brigadas",
      "desc": "Soluciones integrales de comunicación y control de contingencias en empresas e industrias.",
      "items": [
        "Comunicación: Megáfonos profesionales de 50W con sirena (1000m alcance).",
        "Higiene Industrial: Estaciones lavaojos portátiles 32L (ANSI Z358.1).",
        "Protección Incendio: Extintores multipropósito ABC, CO2 y mangueras."
      ]
    },
    {
      "id": "cat-06",
      "num": "Categoría 06",
      "code": "dotacion_personalizada",
      "title": "Dotación Personalizada",
      "desc": "Servicio completo de bordado, estampado e identidad de marca institucional.",
      "items": [
        "Bordados Computarizados: Bordados en 3D para camisetas, gorras y chaquetas.",
        "Marcación de Cascos: Rotulación con vinilos reflectivos de alta adherencia.",
        "Uniformes Corporativos: Overalls industriales y jeans de trabajo en dril."
      ]
    }
  ],
  "services": [
    {
      "id": "serv-01",
      "icon": "🛡️",
      "title": "Suministro de EPP Certificados",
      "desc": "Provisión integral de Elementos de Protección Personal (Cascos, Gafas, Guantes, Calzado, Protección Auditiva y Respiratoria) bajo normas ANSI, CE e ISO."
    },
    {
      "id": "serv-02",
      "icon": "🚨",
      "title": "Equipamiento para Brigadas de Emergencia",
      "desc": "Armado de kits integrales de respuesta rápida: Botiquines Tipo A/B/C, camillas espinales, megáfonos, linternas tácticas y extintores."
    },
    {
      "id": "serv-03",
      "icon": "🦺",
      "title": "Personalización y Bordados Institucionales",
      "desc": "Confección y personalización de uniformes, chalecos tácticos, prendas reflectivas, parches en velcro y rotulación corporativa en cascos."
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
      "title": "Rescate Vertical & Trabajos en Alturas",
      "desc": "Venta y asesoramiento de arneses, cuerdas estáticas 11mm, mosquetones forjados y sistemas de anclaje para trabajos en alturas y socorrismo."
    }
  ],
  "products": [
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
        "Cierre: Ajuste de velcro reinforced",
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
}

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

/* PRELOADER SPLASH SCREEN CON FONDO TOTALMENTE OPACO DEGRADADO */
#pagePreloader {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: linear-gradient(135deg, #000000 0%, #2D3748 50%, #1A202C 100%);
    z-index: 999999;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1), visibility 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}
#pagePreloader.preloader-hidden {
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
}
.preloader-logo-ring {
    position: relative;
    width: 130px;
    height: 130px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
}
.preloader-ring-spin {
    position: absolute;
    width: 100%;
    height: 100%;
    border: 4px solid rgba(255, 102, 0, 0.2);
    border-top: 4px solid var(--orange);
    border-radius: 50%;
    animation: preloaderSpin 1.4s cubic-bezier(0.5, 0, 0.5, 1) infinite;
}
.preloader-badge-center {
    background: linear-gradient(135deg, var(--orange), var(--orange-light));
    color: #FFF;
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 2.4rem;
    padding: 14px 22px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(255,102,0,0.45);
    animation: preloaderPulse 2.2s ease-in-out infinite alternate;
}
.preloader-custom-logo-img {
    max-width: 100px;
    max-height: 100px;
    object-fit: contain;
    border-radius: 12px;
    filter: drop-shadow(0 6px 15px rgba(255,102,0,0.5));
    animation: preloaderPulse 2.2s ease-in-out infinite alternate;
}
@keyframes preloaderSpin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
@keyframes preloaderPulse {
    0% { transform: scale(0.95); }
    100% { transform: scale(1.05); }
}
.preloader-title {
    color: #FFFFFF;
    font-size: 1.5rem;
    font-weight: 900;
    letter-spacing: 2px;
    margin-bottom: 6px;
    text-transform: uppercase;
}
.preloader-title span { color: var(--orange); }
.preloader-subtext {
    color: #CBD5E1;
    font-size: 0.92rem;
    margin-bottom: 28px;
    letter-spacing: 0.5px;
}
.preloader-bar-bg {
    width: 260px;
    height: 6px;
    background: rgba(255,255,255,0.15);
    border-radius: 10px;
    overflow: hidden;
    position: relative;
}
.preloader-bar-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, var(--orange), var(--orange-light));
    border-radius: 10px;
    transition: width 0.08s linear;
    box-shadow: 0 0 12px var(--orange);
}

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
.top-bar-content { display: flex; justify-content: space-between; align-items: center; gap: 15px; }
.brand-logo-group { display: flex; align-items: center; gap: 10px; text-decoration: none; cursor: pointer; flex-shrink: 0; }
.brand-badge {
    background: linear-gradient(135deg, var(--orange), var(--orange-light));
    color: #FFF; font-family: 'Montserrat', sans-serif; font-weight: 900; font-size: 1.15rem;
    padding: 4px 10px; border-radius: 8px; box-shadow: 0 4px 12px rgba(255,102,0,0.3);
}
.brand-real-logo-img {
    height: 42px; width: auto; max-width: 140px; object-fit: contain; border-radius: 6px;
}
.brand-title { font-size: 1.25rem; font-weight: 900; letter-spacing: 0.5px; color: var(--white); }
.brand-title span { color: var(--orange); }

.nav-links { display: flex; gap: 16px; align-items: center; flex-wrap: wrap; }
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
    white-space: nowrap; flex-shrink: 0; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; border: none;
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

/* DESIGN SYSTEM EJECUTIVO CMS v12 */
.admin-hero-banner {
    background: linear-gradient(135deg, #050E1A 0%, #0B1C30 50%, #112844 100%);
    color: #FFF; padding: 40px 25px; border-radius: 20px; border-left: 6px solid var(--orange);
    box-shadow: 0 15px 35px rgba(0,0,0,0.25); margin-bottom: 30px; position: relative; overflow: hidden;
}
.admin-hero-banner::after {
    content: 'CMS 12.0'; position: absolute; right: -20px; bottom: -20px; font-size: 7rem;
    font-weight: 900; color: rgba(255,102,0,0.05); font-family: 'Montserrat', sans-serif; pointer-events: none;
}
.admin-metrics-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 35px;
}
.admin-metric-card {
    background: #FFFFFF; border-radius: 16px; padding: 22px 20px; box-shadow: var(--card-shadow);
    border: 1px solid rgba(0,0,0,0.06); border-top: 4px solid var(--orange); transition: all 0.3s ease; display: flex; align-items: center; gap: 16px;
}
.admin-metric-card:hover { transform: translateY(-4px); box-shadow: var(--hover-shadow); }
.admin-metric-icon {
    width: 52px; height: 52px; border-radius: 14px; background: rgba(255,102,0,0.12); color: var(--orange);
    display: flex; align-items: center; justify-content: center; font-size: 1.6rem; flex-shrink: 0;
}
.admin-metric-val { font-size: 1.8rem; font-weight: 900; color: var(--navy); line-height: 1; margin-bottom: 4px; font-family: 'Montserrat', sans-serif; }
.admin-metric-lbl { font-size: 0.8rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }

/* SWITCH TOGGLE ULTRA MODERNO */
.switch-container { display: flex; align-items: center; gap: 12px; }
.switch { position: relative; display: inline-block; width: 50px; height: 26px; flex-shrink: 0; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #CBD5E1; transition: .35s ease; border-radius: 34px; }
.slider:before { position: absolute; content: ""; height: 18px; width: 18px; left: 4px; bottom: 4px; background-color: white; transition: .35s ease; border-radius: 50%; box-shadow: 0 2px 6px rgba(0,0,0,0.3); }
input:checked + .slider { background-color: var(--orange); }
input:checked + .slider:before { transform: translateX(24px); }

/* TOAST FLOATING NOTIFICATIONS */
#toastContainer {
    position: fixed; top: 85px; right: 25px; z-index: 99999; display: flex; flex-direction: column; gap: 10px; pointer-events: none;
}
.toast-msg {
    background: #0B1C30; color: #FFF; border-left: 5px solid var(--orange); padding: 14px 22px; border-radius: 12px;
    font-weight: 700; font-size: 0.92rem; box-shadow: 0 10px 30px rgba(0,0,0,0.35); display: flex; align-items: center; gap: 10px;
    animation: toastIn 0.35s cubic-bezier(0.4, 0, 0.2, 1) forwards; pointer-events: all;
}
@keyframes toastIn {
    0% { opacity: 0; transform: translateX(60px); }
    100% { opacity: 1; transform: translateX(0); }
}

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

/* CONTÁCTENOS Y CMS */
.contact-section-wrapper { display: grid; grid-template-columns: 1fr 1fr; gap: 35px; background: var(--white); padding: 45px 35px; border-radius: 20px; box-shadow: var(--card-shadow); border: 1px solid rgba(0,0,0,0.06); }
.contact-form-group { margin-bottom: 18px; }
.contact-form-group label { display: block; font-weight: 700; margin-bottom: 6px; color: var(--navy); font-size: 0.9rem; }
.contact-form-input { width: 100%; padding: 13px 16px; border-radius: 8px; border: 1px solid #CBD5E1; font-size: 0.96rem; outline: none; transition: border-color 0.3s; }
.contact-form-input:focus { border-color: var(--orange); }
.btn-submit-contact { background: linear-gradient(135deg, var(--orange), var(--orange-light)); color: var(--white); border: none; padding: 15px 24px; border-radius: 8px; font-weight: 800; font-size: 1rem; cursor: pointer; width: 100%; box-shadow: 0 4px 15px rgba(255,102,0,0.3); transition: all 0.3s; }
.btn-submit-contact:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255,102,0,0.5); }

.admin-table { width: 100%; border-collapse: collapse; margin-top: 20px; background: var(--white); border-radius: 12px; overflow: hidden; box-shadow: var(--card-shadow); }
.admin-table th { background: var(--navy); color: var(--white); padding: 14px; text-align: left; font-size: 0.9rem; }
.admin-table td { padding: 14px; border-bottom: 1px solid #E2E8F0; font-size: 0.9rem; vertical-align: middle; }
.admin-table tr:hover { background: #F8FAFC; }
.badge-admin { padding: 4px 10px; border-radius: 50px; font-size: 0.75rem; font-weight: bold; background: rgba(255,102,0,0.12); color: var(--orange); }

.admin-tabs-bar { display: flex; gap: 10px; overflow-x: auto; margin-bottom: 25px; border-bottom: 2px solid #E2E8F0; padding-bottom: 10px; }
.admin-tab-btn { background: #E2E8F0; color: var(--navy); border: none; padding: 11px 20px; border-radius: 10px; font-weight: 800; font-size: 0.88rem; cursor: pointer; transition: all 0.3s; white-space: nowrap; }
.admin-tab-btn.active-tab { background: var(--orange); color: var(--white); box-shadow: 0 4px 14px rgba(255,102,0,0.35); }

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

# Template HTML con CMS Panel Ejecutivo Ultra Profesional 12.0
INDEX_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YD Protección | Plataforma Web Oficial</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800;900&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>""" + EMBEDDED_CSS + """</style>
</head>
<body>

    <!-- CONTENEDOR DE NOTIFICACIONES TOAST FLOATING -->
    <div id="toastContainer"></div>

    <!-- PRELOADER SPLASH SCREEN -->
    <div id="pagePreloader">
        <div class="preloader-logo-ring">
            <div class="preloader-ring-spin"></div>
            <div id="preloaderLogoContainer">
                <div class="preloader-badge-center">YD</div>
            </div>
        </div>
        <div class="preloader-title" id="preloaderTitle">PROTECCIÓN <span>EQUIPOS</span></div>
        <div class="preloader-subtext" id="preloaderSubtitle">Cargando plataforma de seguridad...</div>
        <div class="preloader-bar-bg">
            <div class="preloader-bar-fill" id="preloaderBar"></div>
        </div>
    </div>

    <!-- TOPBAR CON MENÚ Y BOTONES ADMINISTRABLES -->
    <header class="top-bar">
        <div class="container top-bar-content">
            <div class="brand-logo-group" onclick="navigateToPage('home')">
                <div id="navbarLogoContainer" style="display: flex; align-items: center; gap: 10px;">
                    <div class="brand-badge">YD</div>
                </div>
                <div class="brand-title"><span id="renderBrandTitle">PROTECCIÓN</span> <span id="renderBrandSub">EQUIPOS</span></div>
            </div>

            <!-- CONTENEDOR DE LINKS Y BOTONES DEL MENÚ ADMINISTRABLE -->
            <div style="display: flex; gap: 14px; align-items: center; flex-wrap: wrap; justify-content: flex-end; flex-grow: 1;">
                <nav class="nav-links" id="renderNavLinksContainer"></nav>
                <div id="renderActionButtonsContainer" style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;"></div>
            </div>
        </div>
    </header>

    <!-- ==================== PÁGINA 1: HOME ==================== -->
    <div id="page-home" class="page-view active-view">
        <section class="hero">
            <div class="container">
                <span class="hero-tag" id="renderHeroTag">Seguridad que salva vidas ★ Yesika & Daniel</span>
                <h2 id="renderHeroSub">Seguridad y Emergencia a tu Alcance</h2>
                <h3 id="renderHeroTitle">EQUIPOS DE PROTECCIÓN Y PREVENCIÓN</h3>
                <p id="renderHeroDesc">Soluciones especializadas para Defensa Civil, Brigadas de Emergencia, Protección Industrial y Dotación Institucional.</p>
                
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
                <p>Conoce nuestra historia, Misión, Visión y Valores en YD Protección.</p>
            </div>
        </div>

        <section class="bg-white" style="padding-top: 15px;">
            <div class="container">
                <p style="text-align: center; max-width: 880px; margin: 0 auto 45px; font-size: 1.12em; color: var(--text-dark); line-height: 1.75;" id="renderAboutIntro">
                    <strong>YD Protección</strong> es una empresa dedicada al suministro de equipos y soluciones integrales de seguridad industrial, elementos de protección personal (EPP), brigadas de emergencia y respuesta en socorrismo.
                </p>
                
                <div class="grid-2" style="margin-bottom: 45px;">
                    <div class="card-box">
                        <h4>🚀 Nuestra Misión</h4>
                        <p style="font-size: 1.02em; color: var(--text-dark);" id="renderMision">
                            Suministrar equipos de protección, emergencia y prevención de la más alta calidad y normatividad.
                        </p>
                    </div>
                    <div class="card-box navy-top">
                        <h4>👁️ Nuestra Visión</h4>
                        <p style="font-size: 1.02em; color: var(--text-dark);" id="renderVision">
                            Ser reconocidos a nivel nacional como la empresa líder y aliada estratégica en soluciones de seguridad.
                        </p>
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

                <div class="categories-grid" id="renderCategoriesPills" style="margin-bottom: 50px;"></div>

                <div style="border-top: 3px solid var(--orange); padding-top: 50px;">
                    <h2 class="section-title">Desglose Detallado por Categoría</h2>
                    <p class="section-subtitle">Conoce los insumos, elementos y certificaciones específicas que incluye cada línea de protección</p>
                    <div class="category-breakdown-grid" id="renderCategoriesBreakdown"></div>
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
                <div class="product-grid" id="productGrid"></div>
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
                <div class="grid-3" id="renderServicesGrid"></div>
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
                                <label for="cMsg">Mensaje *</label>
                                <textarea id="cMsg" class="contact-form-input" rows="4" placeholder="Describe los productos, servicios o cantidades que necesitas cotizar..." required></textarea>
                            </div>
                            <button type="submit" class="btn-submit-contact">💬 Enviar Solicitud por WhatsApp</button>
                        </form>
                    </div>

                    <div style="background: var(--navy-dark); color: var(--white); padding: 32px 24px; border-radius: 16px; display: flex; flex-direction: column; justify-content: center;">
                        <h3 style="color: var(--orange); margin-bottom: 20px; font-size: 1.4em;">Información Directa</h3>
                        
                        <div style="margin-bottom: 24px; font-size: 1.05em; line-height: 2.1;">
                            <p><strong style="color: var(--orange);">📱 WHATSAPP:</strong> <span id="renderContactWa">+57 (300) 000-0000</span></p>
                            <p><strong style="color: var(--orange);">✉️ CORREO:</strong> <span id="renderContactEmail">contacto@ydproteccion.com</span></p>
                            <p><strong style="color: var(--orange);">📸 INSTAGRAM:</strong> <span id="renderContactInsta">@ydproteccion</span></p>
                            <p><strong style="color: var(--orange);">📍 UBICACIÓN:</strong> <span id="renderContactLocation">Medellín, Antioquia, Colombia</span></p>
                        </div>

                        <div style="background: rgba(255,102,0,0.15); border: 1px solid var(--orange); padding: 18px; border-radius: 12px;">
                            <h4 style="color: var(--orange); margin-bottom: 6px; font-size: 1em;">⏰ HORARIOS DE ATENCIÓN</h4>
                            <p style="font-size: 0.92em; color: #E2E8F0;" id="renderContactSchedule">Lunes a Viernes: 8:00 AM – 6:00 PM</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- CONTENEDOR DINÁMICO DE SECCIONES PERSONALIZADAS CREADAS DESDE EL CMS -->
    <div id="dynamicCustomPagesContainer"></div>

    <!-- ==================== PÁGINA VISTA ADMIN CMS EJECUTIVO 12.0 ==================== -->
    <div id="page-admin" class="page-view">
        <div class="container" style="padding-top: 30px; padding-bottom: 60px;">
            
            <!-- ENCABEZADO HERO DEL CMS -->
            <div class="admin-hero-banner">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; position: relative; z-index: 2;">
                    <div>
                        <span style="background: rgba(255,102,0,0.2); border: 1px solid var(--orange); color: var(--orange); font-size: 0.78rem; font-weight: 900; padding: 4px 14px; border-radius: 50px; text-transform: uppercase;">PANEL DE CONTROL EJECUTIVO v12.0</span>
                        <h1 style="font-size: clamp(1.8rem, 4vw, 2.5rem); margin-top: 8px; color: #FFF;">ADMINISTRACIÓN TOTAL YD PROTECCIÓN</h1>
                        <p style="color: #CBD5E1; font-size: 0.95rem; margin-top: 4px;">Sincronización en tiempo real vía Supabase Cloud Sync Engine para Móviles, Tablets y PCs</p>
                    </div>
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="background: rgba(37,211,102,0.15); border: 1px solid #25D366; color: #25D366; padding: 8px 16px; border-radius: 50px; font-weight: 800; font-size: 0.85rem; display: flex; align-items: center; gap: 6px;">
                            <span>☁️ NUBE CONECTADA</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- MODAL LOGIN ADMIN -->
            <div id="loginOverlay" style="background: var(--navy-dark); color: var(--white); padding: 40px 30px; border-radius: 20px; max-width: 440px; margin: 0 auto 40px; text-align: center; border-top: 6px solid var(--orange); box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
                <div class="brand-badge" style="display: inline-block; margin-bottom: 14px; font-size: 1.4rem; padding: 6px 14px;">YD</div>
                <h3 style="color: #FFF; margin-bottom: 6px; letter-spacing: 0.5px;">ACCESO ADMINISTRATIVO CMS</h3>
                <p style="color: #CBD5E1; font-size: 0.88rem; margin-bottom: 25px;">Ingresa credenciales para parametrizar la plataforma</p>

                <form onsubmit="handleAdminLogin(event)">
                    <div style="margin-bottom: 16px; text-align: left;">
                        <label style="font-weight:800; font-size:0.82rem; color:var(--orange);">USUARIO ADMINISTRADOR</label>
                        <input type="text" id="admUser" class="contact-form-input" required placeholder="admin" value="admin" style="margin-top: 6px;">
                    </div>
                    <div style="margin-bottom: 22px; text-align: left;">
                        <label style="font-weight:800; font-size:0.82rem; color:var(--orange);">CONTRASEÑA SECLAVE</label>
                        <input type="password" id="admPass" class="contact-form-input" required placeholder="••••••••" value="yd2026" style="margin-top: 6px;">
                    </div>
                    <button type="submit" class="btn-submit-contact" style="padding: 16px; font-size: 1.05rem;">🔑 Entrar al Dashboard CMS</button>
                </form>
            </div>

            <!-- CONTENIDO PRINCIPAL DEL CMS TRAS INICIAR SESIÓN -->
            <div id="adminMainContent" style="display: none;">
                
                <!-- METRICAS EJECUTIVAS EN TIEMPO REAL -->
                <div class="admin-metrics-grid">
                    <div class="admin-metric-card">
                        <div class="admin-metric-icon">📦</div>
                        <div>
                            <div class="admin-metric-val" id="metricProductsCount">0</div>
                            <div class="admin-metric-lbl">Productos en Catálogo</div>
                        </div>
                    </div>
                    <div class="admin-metric-card">
                        <div class="admin-metric-icon">🏷️</div>
                        <div>
                            <div class="admin-metric-val" id="metricCategoriesCount">0</div>
                            <div class="admin-metric-lbl">Categorías Activas</div>
                        </div>
                    </div>
                    <div class="admin-metric-card">
                        <div class="admin-metric-icon">🌐</div>
                        <div>
                            <div class="admin-metric-val" id="metricNavsCount">0</div>
                            <div class="admin-metric-lbl">Links & Botones Web</div>
                        </div>
                    </div>
                    <div class="admin-metric-card" style="border-top-color: #25D366;">
                        <div class="admin-metric-icon" style="background: rgba(37,211,102,0.12); color: #25D366;">☁️</div>
                        <div>
                            <div class="admin-metric-val" style="color: #166534; font-size: 1.4rem;">ONLINE</div>
                            <div class="admin-metric-lbl">Supabase Cloud Sync</div>
                        </div>
                    </div>
                </div>

                <!-- BARRA DE PESTAÑAS EJECUTIVAS -->
                <div class="admin-tabs-bar">
                    <button class="admin-tab-btn active-tab" onclick="switchAdminTab('nav_menu', this)">🍔 Menú & Botones</button>
                    <button class="admin-tab-btn" onclick="switchAdminTab('logo_preloader', this)">🖼️ Logo & Preloader</button>
                    <button class="admin-tab-btn" onclick="switchAdminTab('categories_manage', this)">🏷️ Categorías (CRUD)</button>
                    <button class="admin-tab-btn" onclick="switchAdminTab('products', this)">📦 Catálogo Productos</button>
                    <button class="admin-tab-btn" onclick="switchAdminTab('company', this)">🏢 Empresa & Hero</button>
                    <button class="admin-tab-btn" onclick="switchAdminTab('contact', this)">📞 Canales Contacto</button>
                    <button class="admin-tab-btn" onclick="switchAdminTab('services', this)">🛠️ Servicios</button>
                    <button class="admin-tab-btn" onclick="switchAdminTab('footer_manage', this)">🦶 Pie de Página</button>
                </div>

                <!-- TAB MENÚ DE NAVEGACIÓN Y BOTONES CON SWITCHES ANIMADOS -->
                <div id="tab-nav_menu" class="admin-tab-content">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; margin-bottom: 22px;">
                        <div>
                            <h3 style="color: var(--navy); font-size: 1.3rem;">Administración del Menú Superior y Botones de Acción</h3>
                            <p style="color: var(--text-muted); font-size: 0.9rem;">Usa los switches interactivos para activar u ocultar de inmediato cualquier botón en celulares y laptops</p>
                        </div>
                        <button class="btn-analytics" onclick="openNewSectionModal()">➕ Crear Nueva Sección Personalizada</button>
                    </div>
                    
                    <form onsubmit="saveNavLinksParams(event)">
                        <div class="grid-2" id="adminNavLinksList"></div>
                        <button type="submit" class="btn-submit-contact" style="margin-top: 25px; padding: 16px; font-size: 1.05rem;">💾 Guardar Menú y Sincronizar en Nube</button>
                    </form>
                </div>

                <!-- TAB LOGO REAL Y PRELOADER -->
                <div id="tab-logo_preloader" class="admin-tab-content" style="display: none;">
                    <h3 style="color: var(--navy); margin-bottom: 18px; font-size: 1.3rem;">Logotipo Institucional y Configuración de Carga</h3>
                    <form onsubmit="saveLogoAndPreloader(event)">
                        <div style="background: #F8FAFC; padding: 25px; border-radius: 16px; margin-bottom: 24px; border: 1px solid #E2E8F0; border-left: 6px solid var(--orange);">
                            <h4 style="color: var(--navy); margin-bottom: 12px; font-size: 1.1rem;">📁 CARGAR LOGO REAL DESDE LA PC</h4>
                            <input type="file" id="logoFileInput" accept="image/*" class="contact-form-input" style="background: #FFF;" onchange="handleLogoFileSelect(event)">
                            <div id="logoPreviewContainer" style="margin-top: 18px; display: none; align-items: center; gap: 18px;">
                                <span style="font-weight: bold; font-size: 0.9rem; color: var(--navy);">Vista Previa Oficial:</span>
                                <img id="logoPreviewImg" src="" style="height: 65px; max-width: 200px; object-fit: contain; background: #0B1C30; padding: 8px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                                <button type="button" class="btn-detail" style="padding: 8px 16px; font-size: 0.82rem; background: #FEE2E2; color: #DC2626;" onclick="clearCustomLogo()">Remover Logo</button>
                            </div>
                        </div>

                        <div style="background: #F8FAFC; padding: 25px; border-radius: 16px; margin-bottom: 24px; border: 1px solid #E2E8F0; border-left: 6px solid var(--navy);">
                            <h4 style="color: var(--navy); margin-bottom: 12px; font-size: 1.1rem;">🎨 PRELOADER DE BIENVENIDA (PANTALLA DE CARGA)</h4>
                            <div class="contact-form-group">
                                <label>Tiempo de Retraso / Duración del Preloader (Segundos de espera)</label>
                                <select id="cfgPreloaderDuration" class="contact-form-input">
                                    <option value="4500">4.5 Segundos (Recomendado - Carga Completa)</option>
                                    <option value="6000">6.0 Segundos (Presentación Extendida)</option>
                                    <option value="3000">3.0 Segundos (Duración Media)</option>
                                    <option value="2000">2.0 Segundos (Rápido)</option>
                                </select>
                            </div>
                            <div class="contact-form-group">
                                <label>Fondo de la Pantalla de Carga (Degradado Opaco Blanco, Gris y Negro)</label>
                                <select id="cfgPreloaderGradient" class="contact-form-input">
                                    <option value="linear-gradient(135deg, #000000 0%, #2D3748 50%, #1A202C 100%)">Degradado Oscuro Elegante (Negro, Gris Oscuro y Grafito)</option>
                                    <option value="linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 50%, #475569 100%)">Degradado Claro Ejecutivo (Blanco, Gris Platino y Acero)</option>
                                    <option value="linear-gradient(135deg, #050E1A 0%, #112844 50%, #FF6600 100%)">Degradado Institucional (Azul Marino y Naranja YD)</option>
                                </select>
                            </div>
                            <div class="contact-form-group">
                                <label>Título en Pantalla de Carga</label>
                                <input type="text" id="cfgPreloaderTitle" class="contact-form-input" required>
                            </div>
                            <div class="contact-form-group">
                                <label>Subtítulo en Pantalla de Carga</label>
                                <input type="text" id="cfgPreloaderSub" class="contact-form-input" required>
                            </div>
                        </div>
                        <button type="submit" class="btn-submit-contact" style="padding: 16px; font-size: 1.05rem;">💾 Guardar Logo y Preloader en Nube</button>
                    </form>
                </div>

                <!-- TAB CATEGORÍAS CRUD -->
                <div id="tab-categories_manage" class="admin-tab-content" style="display: none;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 22px;">
                        <h3 style="color: var(--navy); font-size: 1.3rem;">Gestión de Categorías y Líneas de Protección</h3>
                        <button class="btn-analytics" onclick="openCategoryFormModal()">➕ Agregar Nueva Categoría</button>
                    </div>
                    <div style="overflow-x: auto; border-radius: 14px; box-shadow: var(--card-shadow);">
                        <table class="admin-table" style="margin-top:0;">
                            <thead>
                                <tr>
                                    <th>Número</th>
                                    <th>Título Categoría</th>
                                    <th>Código</th>
                                    <th>Descripción</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody id="adminCategoriesTable"></tbody>
                        </table>
                    </div>
                </div>

                <!-- TAB FOOTER -->
                <div id="tab-footer_manage" class="admin-tab-content" style="display: none;">
                    <h3 style="color: var(--navy); margin-bottom: 18px; font-size: 1.3rem;">Pie de Página (Footer)</h3>
                    <form onsubmit="saveFooterParams(event)">
                        <div class="contact-form-group">
                            <label>Título del Footer</label>
                            <input type="text" id="cfgFooterTitle" class="contact-form-input" required>
                        </div>
                        <div class="contact-form-group">
                            <label>Subtítulo del Footer</label>
                            <input type="text" id="cfgFooterSubtitle" class="contact-form-input" required>
                        </div>
                        <div class="contact-form-group">
                            <label>Texto de Copyright y Derechos Reservados</label>
                            <input type="text" id="cfgFooterCopyright" class="contact-form-input" required>
                        </div>
                        <button type="submit" class="btn-submit-contact" style="padding: 16px; font-size: 1.05rem;">💾 Guardar Pie de Página en Nube</button>
                    </form>
                </div>

                <!-- TAB PRODUCTOS CRUD -->
                <div id="tab-products" class="admin-tab-content" style="display: none;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; margin-bottom: 22px;">
                        <h3 style="color: var(--navy); font-size: 1.3rem;">Catálogo General de Productos</h3>
                        <button class="btn-analytics" onclick="openProductFormModal()">➕ Agregar Nuevo Producto</button>
                    </div>
                    <div style="overflow-x: auto; border-radius: 14px; box-shadow: var(--card-shadow);">
                        <table class="admin-table" style="margin-top:0;">
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
                            <tbody id="adminProductsTable"></tbody>
                        </table>
                    </div>
                </div>

                <!-- TAB EMPRESA -->
                <div id="tab-company" class="admin-tab-content" style="display: none;">
                    <h3 style="color: var(--navy); margin-bottom: 18px; font-size: 1.3rem;">Información Institucional & Secciones Principales</h3>
                    <form onsubmit="saveCompanyParams(event)">
                        <div class="contact-form-group">
                            <label>Título del Hero Principal</label>
                            <input type="text" id="cfgHeroTitle" class="contact-form-input" required>
                        </div>
                        <div class="contact-form-group">
                            <label>Subtítulo del Hero</label>
                            <input type="text" id="cfgHeroTag" class="contact-form-input" required>
                        </div>
                        <div class="contact-form-group">
                            <label>Descripción del Hero Principal</label>
                            <textarea id="cfgHeroDesc" class="contact-form-input" rows="2" required></textarea>
                        </div>
                        <div class="contact-form-group">
                            <label>Texto "Quiénes Somos"</label>
                            <textarea id="cfgAboutIntro" class="contact-form-input" rows="3" required></textarea>
                        </div>
                        <div class="contact-form-group">
                            <label>Nuestra Misión</label>
                            <textarea id="cfgMision" class="contact-form-input" rows="3" required></textarea>
                        </div>
                        <div class="contact-form-group">
                            <label>Nuestra Visión</label>
                            <textarea id="cfgVision" class="contact-form-input" rows="3" required></textarea>
                        </div>
                        <button type="submit" class="btn-submit-contact" style="padding: 16px; font-size: 1.05rem;">💾 Guardar Cambios Institucionales en Nube</button>
                    </form>
                </div>

                <!-- TAB CONTACTO -->
                <div id="tab-contact" class="admin-tab-content" style="display: none;">
                    <h3 style="color: var(--navy); margin-bottom: 18px; font-size: 1.3rem;">Canales de Contacto y Atención</h3>
                    <form onsubmit="saveContactParams(event)">
                        <div class="contact-form-group">
                            <label>Número de WhatsApp para Cotizaciones (Ej: 573000000000)</label>
                            <input type="text" id="cfgWa" class="contact-form-input" required>
                        </div>
                        <div class="contact-form-group">
                            <label>Texto Visible del WhatsApp (Ej: +57 (300) 000-0000)</label>
                            <input type="text" id="cfgWaDisplay" class="contact-form-input" required>
                        </div>
                        <div class="contact-form-group">
                            <label>Correo Electrónico</label>
                            <input type="email" id="cfgEmail" class="contact-form-input" required>
                        </div>
                        <div class="contact-form-group">
                            <label>Instagram</label>
                            <input type="text" id="cfgInsta" class="contact-form-input" required>
                        </div>
                        <div class="contact-form-group">
                            <label>Ubicación / Ciudad</label>
                            <input type="text" id="cfgLocation" class="contact-form-input" required>
                        </div>
                        <div class="contact-form-group">
                            <label>Horarios de Atención</label>
                            <input type="text" id="cfgSchedule" class="contact-form-input" required>
                        </div>
                        <button type="submit" class="btn-submit-contact" style="padding: 16px; font-size: 1.05rem;">💾 Guardar Datos de Contacto en Nube</button>
                    </form>
                </div>

                <!-- TAB SERVICIOS -->
                <div id="tab-services" class="admin-tab-content" style="display: none;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
                        <h3 style="color: var(--navy); font-size: 1.3rem;">Servicios Corporativos</h3>
                        <button class="btn-analytics" onclick="addNewServicePrompt()">➕ Agregar Servicio</button>
                    </div>
                    <div class="grid-2" id="adminServicesList"></div>
                </div>

            </div>
        </div>
    </div>

    <!-- MODAL CREAR NUEVA SECCIÓN PERSONALIZADA -->
    <div class="modal-backdrop" id="newSectionModal">
        <div class="modal-card">
            <button class="modal-close" onclick="closeNewSectionModal()">&times;</button>
            <h3 style="color: var(--navy); margin-bottom: 18px;">Crear Nueva Sección en la Web</h3>
            
            <form onsubmit="saveNewSection(event)">
                <div class="contact-form-group">
                    <label>Nombre para el Menú Superior *</label>
                    <input type="text" id="secNavLabel" class="contact-form-input" required placeholder="Ej: Garantías / Promociones">
                </div>
                <div class="contact-form-group">
                    <label>Título del Banner de la Sección *</label>
                    <input type="text" id="secTitle" class="contact-form-input" required placeholder="Ej: Políticas de Garantía y Normatividad">
                </div>
                <div class="contact-form-group">
                    <label>Subtítulo *</label>
                    <input type="text" id="secSubtitle" class="contact-form-input" required placeholder="Resumen o lema de la sección...">
                </div>
                <div class="contact-form-group">
                    <label>Contenido Principal / Descripción *</label>
                    <textarea id="secContent" class="contact-form-input" rows="4" required placeholder="Detalla la información completa de esta nueva sección..."></textarea>
                </div>
                <button type="submit" class="btn-submit-contact">🚀 Crear Sección y Añadir al Menú</button>
            </form>
        </div>
    </div>

    <!-- MODAL AGREGAR / EDITAR CATEGORÍA -->
    <div class="modal-backdrop" id="categoryModal">
        <div class="modal-card">
            <button class="modal-close" onclick="closeCategoryModal()">&times;</button>
            <h3 id="catFormTitle" style="color: var(--navy); margin-bottom: 18px;">Agregar / Editar Categoría</h3>
            
            <form id="categoryForm" onsubmit="saveCategory(event)">
                <input type="hidden" id="catId">
                <div class="contact-form-group">
                    <label>Número Visible (Ej: Categoría 01) *</label>
                    <input type="text" id="catNum" class="contact-form-input" required placeholder="Categoría 07">
                </div>
                <div class="contact-form-group">
                    <label>Título de la Categoría *</label>
                    <input type="text" id="catTitle" class="contact-form-input" required placeholder="Ej: Calzado de Seguridad Industrial">
                </div>
                <div class="contact-form-group">
                    <label>Código Identificador *</label>
                    <input type="text" id="catCode" class="contact-form-input" required placeholder="ej: calzado_seguridad">
                </div>
                <div class="contact-form-group">
                    <label>Descripción Resumida *</label>
                    <textarea id="catDesc" class="contact-form-input" rows="2" required placeholder="Descripción de la línea de productos..."></textarea>
                </div>
                <div class="contact-form-group">
                    <label>Ítems Desglose (Separados por punto y coma ';') *</label>
                    <textarea id="catItems" class="contact-form-input" rows="3" required placeholder="Botas dieléctricas; Calzado anti-deslizante; Punteras de policarbonato"></textarea>
                </div>
                <button type="submit" class="btn-submit-contact">💾 Guardar Categoría</button>
            </form>
        </div>
    </div>

    <!-- MODAL PRODUCTO -->
    <div class="modal-backdrop" id="productModal">
        <div class="modal-card">
            <button class="modal-close" onclick="closeProductModal()">&times;</button>
            <h3 id="pFormTitle" style="color: var(--navy); margin-bottom: 18px;">Agregar / Editar Producto</h3>
            
            <form id="productForm" onsubmit="saveProduct(event)">
                <input type="hidden" id="pId">
                <div class="contact-form-group">
                    <label>Título del Producto *</label>
                    <input type="text" id="pTitle" class="contact-form-input" required placeholder="Ej: Casco Dieléctrico Especial">
                </div>
                <div class="contact-form-group">
                    <label>Categoría *</label>
                    <select id="pCategory" class="contact-form-input" required></select>
                </div>
                <div class="contact-form-group">
                    <label>Insignia / Badge (Opcional)</label>
                    <input type="text" id="pBadge" class="contact-form-input" placeholder="Ej: MÁS VENDIDO / NORMATIVO">
                </div>
                <div class="contact-form-group">
                    <label>Ruta de la Imagen o URL *</label>
                    <input type="text" id="pImage" class="contact-form-input" required placeholder="/images/casco_industrial.jpg">
                </div>
                <div class="contact-form-group">
                    <label>Descripción Corta *</label>
                    <input type="text" id="pShortDesc" class="contact-form-input" required placeholder="Resumen del producto...">
                </div>
                <div class="contact-form-group">
                    <label>Descripción Completa *</label>
                    <textarea id="pDesc" class="contact-form-input" rows="3" required placeholder="Usos y características técnicas..."></textarea>
                </div>
                <button type="submit" class="btn-submit-contact">💾 Guardar Producto</button>
            </form>
        </div>
    </div>

    <!-- MODAL VISTA FICHA -->
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

    <!-- FOOTER ADMINISTRABLE -->
    <footer>
        <div class="container">
            <h2 id="renderFooterTitle">HABLEMOS DE TU SEGURIDAD</h2>
            <p style="font-size: clamp(0.9rem, 2vw, 1.1rem);" id="renderFooterSubtitle">Solicita cotización y asesoría personalizada de inmediato</p>
            
            <div class="footer-bottom">
                <p id="renderFooterCopyright">YESIKA & DANIEL | YD PROTECCIÓN &copy; 2026 — Todos los Derechos Reservados</p>
            </div>
        </div>
    </footer>

    <!-- ENGINE DE SINCRONIZACIÓN Y CMS INTERACTIVO EJECUTIVO (v12) -->
    <script>
        const INITIAL_DATA = """ + json.dumps(INITIAL_SITE_DATA) + """;
        let tempLoadedLogoBase64 = "";

        // NOTIFICACIONES FLOATING TOAST ELEGANTES
        function showToast(message, type = 'success') {
            const container = document.getElementById('toastContainer');
            if (!container) return;
            const toast = document.createElement('div');
            toast.className = 'toast-msg';
            toast.innerHTML = `<span>${type === 'success' ? '✅' : 'ℹ️'}</span> ${message}`;
            container.appendChild(toast);
            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(60px)';
                toast.style.transition = 'all 0.4s ease';
                setTimeout(() => toast.remove(), 400);
            }, 3500);
        }

        // PURGA AUTOMÁTICA DE VERSIONES ANTIGUAS DE CACHE LOCAL EN DISPOSITIVOS MÓVILES
        ['yd_site_config_v5','yd_site_config_v6','yd_site_config_v7','yd_site_config_v8','yd_site_config_v9','yd_site_config_v10'].forEach(k => {
            try { localStorage.removeItem(k); } catch(e) {}
        });

        async function fetchSupabaseSiteData() {
            try {
                const res = await fetch('/api/site-data?t=' + Date.now());
                if (res.ok) {
                    const data = await res.json();
                    if (data && data.nav_links) return data;
                }
            } catch(e) {}

            return null;
        }

        function getLocalSiteData() {
            const saved = localStorage.getItem('yd_site_config_v12');
            if (saved) {
                try {
                    const parsed = JSON.parse(saved);
                    if (parsed && parsed.nav_links) return parsed;
                } catch(e) {}
            }
            return INITIAL_DATA;
        }

        async function getSiteData() {
            const cloudData = await fetchSupabaseSiteData();
            if (cloudData && cloudData.nav_links) {
                localStorage.setItem('yd_site_config_v12', JSON.stringify(cloudData));
                return cloudData;
            }
            return getLocalSiteData();
        }

        async function saveSiteData(data) {
            localStorage.setItem('yd_site_config_v12', JSON.stringify(data));
            renderSite(data);

            try {
                await fetch('/api/site-data', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            } catch(e) {}
        }

        function updateAdminMetrics(data) {
            const products = data.products || INITIAL_DATA.products;
            const categories = data.categories_breakdown || INITIAL_DATA.categories_breakdown;
            const navs = data.nav_links || INITIAL_DATA.nav_links;

            document.getElementById('metricProductsCount').textContent = products.length;
            document.getElementById('metricCategoriesCount').textContent = categories.length;
            document.getElementById('metricNavsCount').textContent = navs.filter(n => n.enabled === true || n.enabled === "true").length;
        }

        function renderSite(data) {
            const comp = data.company || INITIAL_DATA.company;
            const prel = data.preloader || INITIAL_SITE_DATA.preloader;
            const foot = data.footer || INITIAL_SITE_DATA.footer;
            const navs = data.nav_links || INITIAL_SITE_DATA.nav_links;
            const customSecs = data.custom_sections || INITIAL_SITE_DATA.custom_sections;

            // Actualizar métricas ejecutivas
            updateAdminMetrics(data);

            // Renderizar Preloader
            const preloaderEl = document.getElementById('pagePreloader');
            if (preloaderEl) preloaderEl.style.background = prel.bg_gradient || "linear-gradient(135deg, #000000 0%, #2D3748 50%, #1A202C 100%)";
            document.getElementById('preloaderTitle').textContent = prel.title || "YD PROTECCIÓN";
            document.getElementById('preloaderSubtitle').textContent = prel.subtitle || "Cargando plataforma de seguridad...";

            // Renderizar Logo Real
            const pLogoBox = document.getElementById('preloaderLogoContainer');
            const navLogoBox = document.getElementById('navbarLogoContainer');

            if (comp.logo_image && comp.logo_image.trim() !== "") {
                if (pLogoBox) pLogoBox.innerHTML = `<img src="${comp.logo_image}" class="preloader-custom-logo-img">`;
                if (navLogoBox) navLogoBox.innerHTML = `<img src="${comp.logo_image}" class="brand-real-logo-img">`;
            } else {
                if (pLogoBox) pLogoBox.innerHTML = `<div class="preloader-badge-center">YD</div>`;
                if (navLogoBox) navLogoBox.innerHTML = `<div class="brand-badge">YD</div>`;
            }

            // Renderizar Menú de Navegación y Botones Accionables con FILTRADO ABSOLUTO (enabled === true)
            const navContainer = document.getElementById('renderNavLinksContainer');
            const actionsContainer = document.getElementById('renderActionButtonsContainer');

            let navHtml = '';
            let actionHtml = '';

            navs.forEach(n => {
                const isEnabled = (n.enabled === true || n.enabled === "true");
                if (isEnabled) {
                    if (n.is_button) {
                        if (n.id === 'admin') {
                            actionHtml += `<button class="btn-analytics" style="background: linear-gradient(135deg, var(--navy), #112844);" onclick="navigateToPage('admin')">${n.label}</button>`;
                        } else if (n.id === 'analytics') {
                            actionHtml += `<a href="${n.url || '/dashboard'}" class="btn-analytics">${n.label}</a>`;
                        } else {
                            actionHtml += `<button class="btn-analytics" onclick="navigateToPage('${n.id}')">${n.label}</button>`;
                        }
                    } else {
                        navHtml += `<button class="nav-link-btn" id="nav-${n.id}" onclick="navigateToPage('${n.id}')">${n.label}</button>`;
                    }
                }
            });

            if (navContainer) navContainer.innerHTML = navHtml;
            if (actionsContainer) actionsContainer.innerHTML = actionHtml;

            // Renderizar Secciones Personalizadas Creadas
            const customPagesBox = document.getElementById('dynamicCustomPagesContainer');
            if (customPagesBox) {
                customPagesBox.innerHTML = customSecs.map(sec => `
                    <div id="page-${sec.id}" class="page-view">
                        <div class="page-header-banner">
                            <div class="container">
                                <h1>${sec.title}</h1>
                                <p>${sec.subtitle}</p>
                            </div>
                        </div>
                        <section class="bg-white" style="padding-top: 15px;">
                            <div class="container">
                                <div class="card-box" style="max-width: 900px; margin: 0 auto; padding: 40px;">
                                    <p style="font-size: 1.1rem; line-height: 1.8; color: var(--text-dark);">${sec.content}</p>
                                </div>
                            </div>
                        </section>
                    </div>
                `).join('');
            }

            // Renderizar Footer Administrable
            document.getElementById('renderFooterTitle').textContent = foot.title || "HABLEMOS DE TU SEGURIDAD";
            document.getElementById('renderFooterSubtitle').textContent = foot.subtitle || "Solicita cotización personalizada";
            document.getElementById('renderFooterCopyright').textContent = foot.copyright || "YD PROTECCIÓN © 2026";

            // Renderizar Empresa / Hero
            document.getElementById('renderHeroTag').textContent = comp.hero_tag;
            document.getElementById('renderHeroSub').textContent = comp.hero_subtitle;
            document.getElementById('renderHeroTitle').textContent = comp.hero_title;
            document.getElementById('renderHeroDesc').textContent = comp.hero_desc;
            document.getElementById('renderAboutIntro').innerHTML = '<strong>' + comp.brand_name + '</strong> ' + comp.about_intro;
            document.getElementById('renderMision').textContent = comp.mision;
            document.getElementById('renderVision').textContent = comp.vision;

            const cnt = data.contact || INITIAL_DATA.contact;
            document.getElementById('renderContactWa').textContent = cnt.whatsapp_display;
            document.getElementById('renderContactEmail').textContent = cnt.email;
            document.getElementById('renderContactInsta').textContent = cnt.instagram;
            document.getElementById('renderContactLocation').textContent = cnt.location;
            document.getElementById('renderContactSchedule').textContent = cnt.schedule;

            // Renderizar Categorías Pills y Breakdown Administrables
            const categories = data.categories_breakdown || INITIAL_DATA.categories_breakdown;
            const cPills = document.getElementById('renderCategoriesPills');
            if (cPills) {
                cPills.innerHTML = `
                    <div class="category-item active" onclick="navigateToPage('tienda', 'todos')">
                        <span class="number">00</span>
                        <div><h4 style="font-size: 1.1em;">TODOS LOS PRODUCTOS</h4><p style="font-size: 0.88em;">Catálogo general completo.</p></div>
                    </div>
                ` + categories.map((c, i) => `
                    <div class="category-item" onclick="navigateToPage('tienda', '${c.code}')">
                        <span class="number">${String(i + 1).padStart(2, '0')}</span>
                        <div><h4 style="font-size: 1.1em;">${c.title}</h4><p style="font-size: 0.88em;">${c.desc}</p></div>
                    </div>
                `).join('');
            }

            const cGrid = document.getElementById('renderCategoriesBreakdown');
            if (cGrid) {
                cGrid.innerHTML = categories.map(c => `
                    <div class="category-breakdown-card">
                        <span class="breakdown-num">${c.num}</span>
                        <h3 class="breakdown-title">${c.title}</h3>
                        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 12px;">${c.desc}</p>
                        <ul class="breakdown-list">
                            ${c.items.map(it => `<li>${it}</li>`).join('')}
                        </ul>
                        <button class="btn-detail" style="width: 100%; margin-top: 10px;" onclick="navigateToPage('tienda', '${c.code}')">Ver Productos en Tienda</button>
                    </div>
                `).join('');
            }

            // Renderizar Productos
            const products = data.products || INITIAL_DATA.products;
            const pGrid = document.getElementById('productGrid');
            pGrid.innerHTML = products.map(p => `
                <article class="product-card" data-id="${p.id}" data-category="${p.category}">
                    <div class="product-image-box">
                        <img src="${p.image}" alt="${p.title}" loading="lazy" onerror="this.src='${p.fallback_image || ''}'">
                        ${p.badge ? `<span class="product-badge">${p.badge}</span>` : ''}
                    </div>
                    <div class="product-info">
                        <span class="product-category-tag">${p.category_name}</span>
                        <h4>${p.title}</h4>
                        <p>${p.short_description}</p>
                        <div class="btn-group">
                            <button class="btn-detail" onclick="openModal('${p.id}')">Ver Detalles</button>
                            <button class="btn-wa" onclick="sendWhatsAppQuote('${p.id}', '${p.title.replace(/'/g, "")}', '${p.category}')">Cotizar</button>
                        </div>
                    </div>
                </article>
            `).join('');

            // Renderizar Servicios
            const services = data.services || INITIAL_DATA.services;
            const sGrid = document.getElementById('renderServicesGrid');
            sGrid.innerHTML = services.map(s => `
                <div class="card-box">
                    <div style="font-size: 2.5rem; margin-bottom: 12px;">${s.icon}</div>
                    <h4>${s.title}</h4>
                    <p style="color: var(--text-muted);">${s.desc}</p>
                    <button class="btn-analytics" style="margin-top: 18px; width:100%; text-align:center;" onclick="navigateToPage('contacto')">Solicitar Asesoría</button>
                </div>
            `).join('');

            loadAdminForms(data);
        }

        function loadAdminForms(data) {
            const comp = data.company || INITIAL_DATA.company;
            const prel = data.preloader || INITIAL_SITE_DATA.preloader;
            const foot = data.footer || INITIAL_SITE_DATA.footer;
            const navs = data.nav_links || INITIAL_SITE_DATA.nav_links;

            // Formulario Preloader / Logo
            document.getElementById('cfgPreloaderDuration').value = prel.duration_ms || "4500";
            document.getElementById('cfgPreloaderGradient').value = prel.bg_gradient || "linear-gradient(135deg, #000000 0%, #2D3748 50%, #1A202C 100%)";
            document.getElementById('cfgPreloaderTitle').value = prel.title || "YD PROTECCIÓN";
            document.getElementById('cfgPreloaderSub').value = prel.subtitle || "Cargando plataforma de seguridad...";

            if (comp.logo_image && comp.logo_image.trim() !== "") {
                document.getElementById('logoPreviewImg').src = comp.logo_image;
                document.getElementById('logoPreviewContainer').style.display = 'flex';
                tempLoadedLogoBase64 = comp.logo_image;
            }

            // Formulario Menú Links CON SWITCHES ANIMADOS v12
            const navAdminGrid = document.getElementById('adminNavLinksList');
            if (navAdminGrid) {
                navAdminGrid.innerHTML = navs.map(n => {
                    const isEnabled = (n.enabled === true || n.enabled === "true");
                    return `
                        <div class="card-box" style="padding: 24px; border-top: 5px solid ${n.is_button ? 'var(--orange)' : 'var(--navy)'};">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                                <span class="badge-admin" style="font-size: 0.8rem;">${n.is_button ? 'BOTÓN DE ACCIÓN' : 'LINK DEL MENÚ'} (ID: ${n.id})</span>
                                
                                <div class="switch-container">
                                    <label class="switch">
                                        <input type="checkbox" class="nav-enable-toggle" data-id="${n.id}" ${isEnabled ? 'checked' : ''} onchange="updateSwitchLabel(this, '${n.id}')">
                                        <span class="slider"></span>
                                    </label>
                                    <span id="switch-lbl-${n.id}" style="font-weight: 800; font-size: 0.85rem; color: ${isEnabled ? 'var(--orange)' : 'var(--text-muted)'};">
                                        ${isEnabled ? '🟢 PUBLICADO' : '🔴 OCULTO'}
                                    </span>
                                </div>
                            </div>

                            <label style="font-size:0.84rem; font-weight:bold; color:var(--navy);">Texto Visible en el Sitio Web:</label>
                            <input type="text" class="contact-form-input nav-label-input" data-id="${n.id}" value="${n.label}" style="margin-top: 6px;">
                            
                            ${n.is_custom ? `
                                <button type="button" class="btn-detail" style="margin-top: 14px; width: 100%; background: #FEE2E2; color: #DC2626;" onclick="deleteCustomSection('${n.id}')">🗑️ Eliminar Sección Personalizada</button>
                            ` : ''}
                        </div>
                    `;
                }).join('');
            }

            // Formulario Footer
            document.getElementById('cfgFooterTitle').value = foot.title || "HABLEMOS DE TU SEGURIDAD";
            document.getElementById('cfgFooterSubtitle').value = foot.subtitle || "Solicita cotización personalizada";
            document.getElementById('cfgFooterCopyright').value = foot.copyright || "YD PROTECCIÓN © 2026";

            // Formulario Categorías CRUD Admin Table
            const categories = data.categories_breakdown || INITIAL_DATA.categories_breakdown;
            const catTable = document.getElementById('adminCategoriesTable');
            if (catTable) {
                catTable.innerHTML = categories.map(c => `
                    <tr id="catrow-${c.id}">
                        <td><strong>${c.num}</strong></td>
                        <td><strong>${c.title}</strong></td>
                        <td><span class="badge-admin">${c.code}</span></td>
                        <td style="font-size:0.82rem; color: var(--text-muted);">${c.desc}</td>
                        <td>
                            <button class="btn-detail" style="padding: 6px 10px; font-size: 0.78rem;" onclick="editCategory('${c.id}')">✏️ Editar</button>
                            <button class="btn-detail" style="padding: 6px 10px; font-size: 0.78rem; background: #FEE2E2; color: #DC2626;" onclick="deleteCategory('${c.id}')">🗑️ Eliminar</button>
                        </td>
                    </tr>
                `).join('');
            }

            // Opciones de categorías en modal de Producto
            const pCategorySelect = document.getElementById('pCategory');
            if (pCategorySelect) {
                pCategorySelect.innerHTML = categories.map(c => `<option value="${c.code}">${c.title}</option>`).join('');
            }

            // Formulario Empresa
            document.getElementById('cfgHeroTitle').value = comp.hero_title;
            document.getElementById('cfgHeroTag').value = comp.hero_tag;
            document.getElementById('cfgHeroDesc').value = comp.hero_desc;
            document.getElementById('cfgAboutIntro').value = comp.about_intro;
            document.getElementById('cfgMision').value = comp.mision;
            document.getElementById('cfgVision').value = comp.vision;

            // Formulario Contacto
            const cnt = data.contact || INITIAL_DATA.contact;
            document.getElementById('cfgWa').value = cnt.whatsapp;
            document.getElementById('cfgWaDisplay').value = cnt.whatsapp_display;
            document.getElementById('cfgEmail').value = cnt.email;
            document.getElementById('cfgInsta').value = cnt.instagram;
            document.getElementById('cfgLocation').value = cnt.location;
            document.getElementById('cfgSchedule').value = cnt.schedule;

            // Formulario Productos
            const products = data.products || INITIAL_DATA.products;
            const pTable = document.getElementById('adminProductsTable');
            if (pTable) {
                pTable.innerHTML = products.map(p => `
                    <tr id="row-${p.id}">
                        <td><strong>${p.id}</strong></td>
                        <td><img src="${p.image}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 8px;" onerror="this.src='${p.fallback_image || ''}'"></td>
                        <td><strong>${p.title}</strong></td>
                        <td><span class="badge-admin">${p.category_name}</span></td>
                        <td><span style="font-size:0.8rem; font-weight:bold; color:var(--orange);">${p.badge || '-'}</span></td>
                        <td>
                            <button class="btn-detail" style="padding: 6px 10px; font-size: 0.78rem;" onclick="editProduct('${p.id}')">✏️ Editar</button>
                            <button class="btn-detail" style="padding: 6px 10px; font-size: 0.78rem; background: #FEE2E2; color: #DC2626;" onclick="deleteProduct('${p.id}')">🗑️ Eliminar</button>
                        </td>
                    </tr>
                `).join('');
            }

            // Formulario Servicios
            const services = data.services || INITIAL_DATA.services;
            const sAdminGrid = document.getElementById('adminServicesList');
            if (sAdminGrid) {
                sAdminGrid.innerHTML = services.map(s => `
                    <div class="card-box">
                        <div style="font-size: 2rem;">${s.icon}</div>
                        <h4>${s.title}</h4>
                        <p style="color: var(--text-muted); font-size: 0.9rem;">${s.desc}</p>
                        <button class="btn-detail" style="margin-top: 12px; background: #FEE2E2; color: #DC2626;" onclick="deleteService('${s.id}')">Eliminar Servicio</button>
                    </div>
                `).join('');
            }
        }

        function updateSwitchLabel(chk, id) {
            const lbl = document.getElementById('switch-lbl-' + id);
            if (lbl) {
                lbl.textContent = chk.checked ? '🟢 PUBLICADO' : '🔴 OCULTO';
                lbl.style.color = chk.checked ? 'var(--orange)' : 'var(--text-muted)';
            }
        }

        // GUARDAR MENÚ DE NAVEGACIÓN Y ESTADO DE ACTIVACIÓN/DESACTIVACIÓN
        async function saveNavLinksParams(e) {
            e.preventDefault();
            const data = await getSiteData();
            
            const inputs = document.querySelectorAll('.nav-label-input');
            const toggles = document.querySelectorAll('.nav-enable-toggle');

            toggles.forEach(chk => {
                const id = chk.getAttribute('data-id');
                const linkObj = data.nav_links.find(n => n.id === id);
                if (linkObj) linkObj.enabled = Boolean(chk.checked);
            });

            inputs.forEach(input => {
                const id = input.getAttribute('data-id');
                const linkObj = data.nav_links.find(n => n.id === id);
                if (linkObj) linkObj.label = input.value;
            });

            await saveSiteData(data);
            showToast('Menú y botones guardados en la Nube Supabase exitosamente.');
        }

        // CREAR NUEVA SECCIÓN PERSONALIZADA
        function openNewSectionModal() {
            document.getElementById('newSectionModal').classList.add('active');
        }
        function closeNewSectionModal() {
            document.getElementById('newSectionModal').classList.remove('active');
        }

        async function saveNewSection(e) {
            e.preventDefault();
            const data = await getSiteData();
            
            const label = document.getElementById('secNavLabel').value;
            const title = document.getElementById('secTitle').value;
            const subtitle = document.getElementById('secSubtitle').value;
            const content = document.getElementById('secContent').value;
            const secId = 'seccion-' + String(Date.now()).slice(-4);

            data.nav_links.splice(data.nav_links.length - 2, 0, {
                id: secId,
                label: label,
                enabled: true,
                is_button: false,
                is_custom: true
            });

            if (!data.custom_sections) data.custom_sections = [];
            data.custom_sections.push({
                id: secId,
                title: title,
                subtitle: subtitle,
                content: content
            });

            await saveSiteData(data);
            closeNewSectionModal();
            showToast('¡Nueva sección "' + label + '" creada con éxito!');
        }

        async function deleteCustomSection(id) {
            if (confirm('¿Deseas eliminar esta sección personalizada?')) {
                const data = await getSiteData();
                data.nav_links = data.nav_links.filter(x => x.id !== id);
                if (data.custom_sections) data.custom_sections = data.custom_sections.filter(x => x.id !== id);
                await saveSiteData(data);
                showToast('Sección eliminada.');
            }
        }

        // GUARDAR FOOTER
        async function saveFooterParams(e) {
            e.preventDefault();
            const data = await getSiteData();
            data.footer.title = document.getElementById('cfgFooterTitle').value;
            data.footer.subtitle = document.getElementById('cfgFooterSubtitle').value;
            data.footer.copyright = document.getElementById('cfgFooterCopyright').value;
            await saveSiteData(data);
            showToast('Pie de página guardado en la Nube Supabase.');
        }

        // ACCIONES DE CATEGORÍAS (CRUD)
        function openCategoryFormModal() {
            document.getElementById('catFormTitle').textContent = 'Agregar Nueva Categoría';
            document.getElementById('catId').value = '';
            document.getElementById('categoryForm').reset();
            document.getElementById('categoryModal').classList.add('active');
        }

        function closeCategoryModal() {
            document.getElementById('categoryModal').classList.remove('active');
        }

        async function editCategory(id) {
            const data = await getSiteData();
            const c = data.categories_breakdown.find(x => x.id === id);
            if (!c) return;

            document.getElementById('catFormTitle').textContent = 'Editar Categoría ID: ' + id;
            document.getElementById('catId').value = c.id;
            document.getElementById('catNum').value = c.num;
            document.getElementById('catTitle').value = c.title;
            document.getElementById('catCode').value = c.code;
            document.getElementById('catDesc').value = c.desc;
            document.getElementById('catItems').value = (c.items || []).join('; ');

            document.getElementById('categoryModal').classList.add('active');
        }

        async function saveCategory(e) {
            e.preventDefault();
            const data = await getSiteData();
            const cid = document.getElementById('catId').value || ('cat-' + String(Date.now()).slice(-4));
            const rawItems = document.getElementById('catItems').value;
            const itemsArray = rawItems.split(';').map(s => s.trim()).filter(s => s.length > 0);

            const cObj = {
                id: cid,
                num: document.getElementById('catNum').value,
                title: document.getElementById('catTitle').value,
                code: document.getElementById('catCode').value,
                desc: document.getElementById('catDesc').value,
                items: itemsArray
            };

            const idx = data.categories_breakdown.findIndex(x => x.id === cid);
            if (idx >= 0) {
                data.categories_breakdown[idx] = cObj;
            } else {
                data.categories_breakdown.push(cObj);
            }

            await saveSiteData(data);
            closeCategoryModal();
            showToast('Categoría guardada en la Nube Supabase.');
        }

        async function deleteCategory(id) {
            if (confirm('¿Deseas eliminar la categoría ' + id + '?')) {
                const data = await getSiteData();
                data.categories_breakdown = data.categories_breakdown.filter(x => x.id !== id);
                await saveSiteData(data);
                showToast('Categoría eliminada.');
            }
        }

        // CONTROL DEL PRELOADER ANIMADO
        document.addEventListener('DOMContentLoaded', async () => {
            const currentData = await getSiteData();
            renderSite(currentData);

            const duration = (currentData.preloader && currentData.preloader.duration_ms) ? currentData.preloader.duration_ms : 4500;
            const stepInterval = Math.floor(duration / 35);
            let progress = 0;
            
            const bar = document.getElementById('preloaderBar');
            const preloader = document.getElementById('pagePreloader');
            
            const interval = setInterval(() => {
                progress += Math.floor(Math.random() * 4) + 2;
                if (progress >= 100) {
                    progress = 100;
                    if (bar) bar.style.width = '100%';
                    clearInterval(interval);
                    setTimeout(() => {
                        if (preloader) preloader.classList.add('preloader-hidden');
                    }, 500);
                } else {
                    if (bar) bar.style.width = progress + '%';
                }
            }, stepInterval);

            if (sessionStorage.getItem('yd_admin_logged') === 'true') {
                const overlay = document.getElementById('loginOverlay');
                const content = document.getElementById('adminMainContent');
                if (overlay) overlay.style.display = 'none';
                if (content) content.style.display = 'block';
            }

            if (window.location.pathname.includes('/admin')) {
                navigateToPage('admin');
            }
        });

        function handleLogoFileSelect(e) {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(evt) {
                tempLoadedLogoBase64 = evt.target.result;
                document.getElementById('logoPreviewImg').src = tempLoadedLogoBase64;
                document.getElementById('logoPreviewContainer').style.display = 'flex';
            };
            reader.readAsDataURL(file);
        }

        function clearCustomLogo() {
            tempLoadedLogoBase64 = "";
            document.getElementById('logoFileInput').value = "";
            document.getElementById('logoPreviewContainer').style.display = 'none';
        }

        async function saveLogoAndPreloader(e) {
            e.preventDefault();
            const data = await getSiteData();
            data.company.logo_image = tempLoadedLogoBase64;
            data.preloader.bg_gradient = document.getElementById('cfgPreloaderGradient').value;
            data.preloader.title = document.getElementById('cfgPreloaderTitle').value;
            data.preloader.subtitle = document.getElementById('cfgPreloaderSub').value;
            data.preloader.duration_ms = parseInt(document.getElementById('cfgPreloaderDuration').value) || 4500;

            await saveSiteData(data);
            showToast('Logo y Preloader guardados en la Nube Supabase.');
        }

        async function saveCompanyParams(e) {
            e.preventDefault();
            const data = await getSiteData();
            data.company.hero_title = document.getElementById('cfgHeroTitle').value;
            data.company.hero_tag = document.getElementById('cfgHeroTag').value;
            data.company.hero_desc = document.getElementById('cfgHeroDesc').value;
            data.company.about_intro = document.getElementById('cfgAboutIntro').value;
            data.company.mision = document.getElementById('cfgMision').value;
            data.company.vision = document.getElementById('cfgVision').value;
            await saveSiteData(data);
            showToast('Información Institucional guardada en la Nube.');
        }

        async function saveContactParams(e) {
            e.preventDefault();
            const data = await getSiteData();
            data.contact.whatsapp = document.getElementById('cfgWa').value;
            data.contact.whatsapp_display = document.getElementById('cfgWaDisplay').value;
            data.contact.email = document.getElementById('cfgEmail').value;
            data.contact.instagram = document.getElementById('cfgInsta').value;
            data.contact.location = document.getElementById('cfgLocation').value;
            data.contact.schedule = document.getElementById('cfgSchedule').value;
            await saveSiteData(data);
            showToast('Datos de Contacto guardados en la Nube.');
        }

        async function editProduct(id) {
            const data = await getSiteData();
            const p = data.products.find(x => x.id === id);
            if (!p) return;

            document.getElementById('pFormTitle').textContent = 'Editar Producto ID: ' + id;
            document.getElementById('pId').value = p.id;
            document.getElementById('pTitle').value = p.title;
            document.getElementById('pCategory').value = p.category;
            document.getElementById('pBadge').value = p.badge || '';
            document.getElementById('pImage').value = p.image;
            document.getElementById('pShortDesc').value = p.short_description;
            document.getElementById('pDesc').value = p.description || p.short_description;
            document.getElementById('productModal').classList.add('active');
        }

        async function saveProduct(e) {
            e.preventDefault();
            const data = await getSiteData();
            const pid = document.getElementById('pId').value || ('prod-' + String(Date.now()).slice(-4));
            const catSelect = document.getElementById('pCategory');
            const catName = catSelect.options[catSelect.selectedIndex].text;

            const pObj = {
                id: pid,
                title: document.getElementById('pTitle').value,
                category: catSelect.value,
                category_name: catName,
                badge: document.getElementById('pBadge').value,
                image: document.getElementById('pImage').value,
                short_description: document.getElementById('pShortDesc').value,
                description: document.getElementById('pDesc').value,
                specs: ["Calidad Garantizada"]
            };

            const idx = data.products.findIndex(x => x.id === pid);
            if (idx >= 0) {
                data.products[idx] = pObj;
            } else {
                data.products.unshift(pObj);
            }

            await saveSiteData(data);
            closeProductModal();
            showToast('Producto guardado en la Nube Supabase.');
        }

        async function deleteProduct(id) {
            if (confirm('¿Deseas eliminar el producto ' + id + '?')) {
                const data = await getSiteData();
                data.products = data.products.filter(x => x.id !== id);
                await saveSiteData(data);
                showToast('Producto eliminado.');
            }
        }

        async function addNewServicePrompt() {
            const title = prompt('Título del nuevo servicio:');
            if (!title) return;
            const desc = prompt('Descripción del servicio:');
            if (!desc) return;

            const data = await getSiteData();
            data.services.push({
                id: 'serv-' + Date.now(),
                icon: '⚡',
                title: title,
                desc: desc
            });
            await saveSiteData(data);
            showToast('Servicio agregado con éxito.');
        }

        async function deleteService(id) {
            if (confirm('¿Deseas eliminar este servicio?')) {
                const data = await getSiteData();
                data.services = data.services.filter(x => x.id !== id);
                await saveSiteData(data);
                showToast('Servicio eliminado.');
            }
        }

        function navigateToPage(pageId, categoryFilter = null) {
            document.querySelectorAll('.page-view').forEach(view => view.classList.remove('active-view'));
            document.querySelectorAll('.nav-link-btn').forEach(btn => btn.classList.remove('active-page'));

            const targetPage = document.getElementById('page-' + pageId);
            const targetBtn = document.getElementById('nav-' + pageId);

            if (targetPage) targetPage.classList.add('active-view');
            if (targetBtn) targetBtn.classList.add('active-page');

            window.scrollTo({ top: 0, behavior: 'smooth' });
            if (categoryFilter) filterCatalogCategory(categoryFilter);
        }

        function filterCatalogCategory(cat, element = null) {
            if (element) {
                document.querySelectorAll('#categoriesGrid .category-item').forEach(item => item.classList.remove('active'));
                element.classList.add('active');
            }
            const productCards = document.querySelectorAll('#productGrid .product-card');
            productCards.forEach(card => {
                const c = card.getAttribute('data-category');
                card.style.display = (cat === 'todos' || c === cat) ? 'flex' : 'none';
            });
        }

        function switchAdminTab(tabName, btnEl) {
            document.querySelectorAll('.admin-tab-content').forEach(el => el.style.display = 'none');
            document.querySelectorAll('.admin-tab-btn').forEach(el => el.classList.remove('active-tab'));
            
            const target = document.getElementById('tab-' + tabName);
            if (target) target.style.display = 'block';
            if (btnEl) btnEl.classList.add('active-tab');
        }

        function handleAdminLogin(e) {
            e.preventDefault();
            const u = document.getElementById('admUser').value;
            const p = document.getElementById('admPass').value;
            if (u === 'admin' && p === 'yd2026') {
                document.getElementById('loginOverlay').style.display = 'none';
                document.getElementById('adminMainContent').style.display = 'block';
                sessionStorage.setItem('yd_admin_logged', 'true');
                showToast('🔑 Sesión CMS iniciada con éxito.');
            } else {
                alert('Credenciales incorrectas');
            }
        }

        async function openModal(id) {
            const data = await getSiteData();
            const p = data.products.find(x => x.id === id);
            if (!p) return;

            document.getElementById('mImg').src = p.image;
            document.getElementById('mCat').textContent = p.category_name;
            document.getElementById('mTitle').textContent = p.title;
            document.getElementById('mDesc').textContent = p.description || p.short_description;
            
            const specsList = document.getElementById('mSpecs');
            specsList.innerHTML = (p.specs || ["Calidad Garantizada"]).map(s => `<li>${s}</li>`).join('');

            document.getElementById('mBtnWa').onclick = () => sendWhatsAppQuote(p.id, p.title, p.category);
            document.getElementById('modalBackdrop').classList.add('active');
        }

        function closeModal() { document.getElementById('modalBackdrop').classList.remove('active'); }
        function openProductFormModal() { document.getElementById('pFormTitle').textContent = 'Agregar Nuevo Producto'; document.getElementById('pId').value = ''; document.getElementById('productForm').reset(); document.getElementById('productModal').classList.add('active'); }
        function closeProductModal() { document.getElementById('productModal').classList.remove('active'); }

        async function handleContactSubmit(e) {
            e.preventDefault();
            const data = await getSiteData();
            const waNum = data.contact.whatsapp || '573000000000';
            const name = document.getElementById('cName').value;
            const phone = document.getElementById('cPhone').value;
            const email = document.getElementById('cEmail').value;
            const msg = document.getElementById('cMsg').value;

            const text = `Hola *YD Protección*, mi nombre es *${name}*.\n\n` +
                         `📱 *Teléfono:* ${phone}\n` +
                         `✉️ *Correo:* ${email}\n` +
                         `💬 *Mensaje:* ${msg}`;

            window.open(`https://wa.me/${waNum}?text=${encodeURIComponent(text)}`, '_blank');
        }

        async function sendWhatsAppQuote(productId, title, category) {
            const data = await getSiteData();
            const waNum = data.contact.whatsapp || '573000000000';
            const msg = `Hola *YD Protección*, solicito cotización de:\n\n📌 *Producto:* ${title}\n🆔 *Código:* ${productId}\n\nPor favor me comparten precio y disponibilidad. ¡Gracias!`;
            window.open(`https://wa.me/${waNum}?text=${encodeURIComponent(msg)}`, '_blank');
        }
    </script>
</body>
</html>"""

DATA_FILE_PATH = "/tmp/yd_site_config_v12.json"

def load_server_data() -> dict:
    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return dict(INITIAL_SITE_DATA)

def save_server_data(data: dict):
    try:
        with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

SAVED_CLOUD_SITE_DATA = load_server_data()

@app.get("/api/site-data")
async def get_site_data_api():
    """Retorna los datos del sitio guardados en el servidor / Supabase para todos los dispositivos"""
    return JSONResponse(content=SAVED_CLOUD_SITE_DATA)

@app.post("/api/site-data")
async def save_site_data_api(request: Request):
    """Guarda las actualizaciones enviadas desde el CMS para que se reflejen al instante en Celulares y Laptops"""
    global SAVED_CLOUD_SITE_DATA
    try:
        data = await request.json()
        if isinstance(data, dict) and "nav_links" in data:
            SAVED_CLOUD_SITE_DATA = data
            save_server_data(data)
            return JSONResponse(content={"status": "success", "message": "Datos guardados en servidor"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return JSONResponse(content={"status": "error"})

@app.get("/")
@app.get("/home")
@app.get("/quienes-somos")
@app.get("/categorias")
@app.get("/tienda")
@app.get("/servicios")
@app.get("/contacto")
@app.get("/admin")
@app.get("/dashboard")
@app.get("/api")
@app.get("/api/index")
@app.get("/api/index.py")
async def main_site_pages(request: Request):
    try:
        rendered = Template(INDEX_HTML).render()
        return HTMLResponse(content=rendered)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error renderizando sitio web</h1><p>{str(e)}</p>")

@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, full_path: str):
    if full_path.startswith("api/"):
        return JSONResponse(status_code=404, content={"detail": "Not Found"})
    return await main_site_pages(request)

handler = app
