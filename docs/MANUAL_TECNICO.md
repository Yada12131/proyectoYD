# 🛠️ MANUAL TÉCNICO Y ARQUITECTURA - PLATAFORMA YD PROTECCIÓN

**Versión:** 18.0 (SaaS Full-Width & Sticky Sidebar Engine)  
**Stack Tecnológico:** Python 3.11, FastAPI, Jinja2, Vanilla JavaScript ES6+, HTML5 Semantic, CSS3 Design Tokens, Supabase Cloud Engine  
**Infraestructura:** Vercel Serverless Functions  
**Repositorio GitHub:** [github.com/Yada12131/proyectoYD.git](https://github.com/Yada12131/proyectoYD.git)

---

## 📋 TABLA DE CONTENIDOS
1. [Arquitectura General del Sistema](#1-arquitectura-general-del-sistema)
2. [Estructura del Proyecto y Archivos Clave](#2-estructura-del-proyecto-y-archivos-clave)
3. [Motor de Persistencia Nube & Local (v18.0)](#3-motor-de-persistencia-nube--local-v180)
4. [Routing y Servidor Serverless (`api/index.py`)](#4-routing-y-servidor-serverless-apiindexpy)
5. [Sistema de Diseño CSS y Tokens (Full-Width & Sticky Sidebar)](#5-sistema-de-diseño-css-y-tokens-full-width--sticky-sidebar)
6. [Instrucciones de Despliegue y Mantenimiento](#6-instrucciones-de-despliegue-y-mantenimiento)

---

## 1. ARQUITECTURA GENERAL DEL SISTEMA

La plataforma **YD Protección** opera bajo un modelo híbrido **Single-Page Application (SPA) + Serverless REST API**:

```
[ Cliente Nube / Novedades ]
            │
            ▼
 ┌──────────────────────────────────────────────────────────┐
 │  FastAPI Serverless Function (Vercel Node / Python Edge) │
 │  Path: api/index.py                                      │
 └──────────────────────────┬───────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
 ┌─────────────────────┐         ┌─────────────────────┐
 │  GET /api/site-data │         │ POST /api/site-data │
 └──────────┬──────────┘         └──────────┬──────────┘
            │                               │
            ▼                               ▼
 ┌──────────────────────────────────────────────────────────┐
 │  Supabase Cloud Engine + LocalStorage (yd_custom_saved_v18)│
 └──────────────────────────────────────────────────────────┘
```

- **Frontend:** SPA construida en HTML5, CSS custom con tokens de color (`#0B1C30`, `#FF6600`) y JavaScript Vanilla sin dependencias pesadas para asegurar cargas ultrarrápidas (< 0.8s).
- **Backend:** FastAPI expuesto como Handler Vercel Serverless (`api/index.py`).
- **Persistencia:** Engine de doble capa: `localStorage` navegador (`yd_custom_saved_v18`) + `/tmp/yd_site_config_v18.json` en servidor con flag `is_user_edited: true`.

---

## 2. ESTRUCTURA DEL PROYECTO Y ARCHIVOS CLAVE

```
c:\Users\DanielOspina\Downloads\YD\catalogo\
├── api/
│   └── index.py            # Servidor FastAPI, Motor Jinja2, HTML, CSS y JS embebidos
├── docs/                   # Documentación Oficial del Proyecto
│   ├── MANUAL_DE_USUARIO.md # Manual para Administradores y Ventas
│   ├── MANUAL_TECNICO.md    # Este archivo (Arquitectura e IT)
│   └── README.md            # Índice de la documentación
├── public/                 # Assets estáticos opcionales
├── vercel.json             # Configuración de rutas y rewrites de Vercel
├── requirements.txt        # Dependencias Python (fastapi, jinja2, uvicorn)
└── README.md               # Documentación general del repositorio
```

---

## 3. MOTOR DE PERSISTENCIA NUBE & LOCAL (v18.0)

Debido a que las **Serverless Functions de Vercel** son efímeras y sus contenedores se reinician automáticamente tras períodos de inactividad, la plataforma implementa una estrategia de persistencia garantizada:

1. **Prioridad 1 (Local):** `localStorage.getItem('yd_custom_saved_v18')`.
2. **Prioridad 2 (Cloud):** Endpoint REST `GET /api/site-data`. Si la respuesta del servidor incluye el flag `is_user_edited: true`, se sobreescribe el estado local para sincronizar el sitio en celulares y computadores nuevos de inmediato.
3. **Guardado:** Al presionar `💾 Guardar Todo y Publicar`, la función `saveSiteData(data)` realiza dos acciones en paralelo:
   - Setea `localStorage.setItem('yd_custom_saved_v18', JSON.stringify(data))`.
   - Emite una petición `POST /api/site-data` que actualiza la variable global en memoria y escribe el archivo `/tmp/yd_site_config_v18.json`.

---

## 4. ROUTING Y SERVIDOR SERVERLESS (`api/index.py`)

El archivo `api/index.py` gestiona todas las rutas del dominio:

- **Rutas de Vista Pública:** `/`, `/home`, `/quienes-somos`, `/categorias`, `/tienda`, `/servicios`, `/contacto`, `/admin`, `/dashboard`.
- **Endpoints de API:**
  - `GET /api/site-data`: Devuelve la estructura JSON completa de la web.
  - `POST /api/site-data`: Recibe y valida el payload JSON actualizado.

Configuración de Vercel (`vercel.json`):
```json
{
  "builds": [
    { "src": "api/index.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "api/index.py" }
  ]
}
```

---

## 5. SISTEMA DE DISEÑO CSS Y TOKENS (FULL-WIDTH & STICKY SIDEBAR)

El diseño visual está construido mediante CSS3 nativo sin frameworks externos:

- **Tokens de Color:**
  - `--navy: #0B1C30` (Azul Marino Ejecutivo)
  - `--navy-dark: #050E1A` (Fondo Obscuro)
  - `--orange: #FF6600` (Naranja Institucional YD)
  - `--orange-light: #FF8533`
- **Layout Full-Width (`.admin-fullwidth-container`):** `max-width: 1680px; width: 100%; margin: 0 auto; padding: 0 35px;`
- **Sidebar Proporcional Sticky (`.admin-sidebar`):**
  ```css
  .admin-sidebar {
      width: 290px;
      flex-shrink: 0;
      background: linear-gradient(180deg, #050E1A 0%, #0B1C30 100%);
      position: sticky;
      top: 90px;
      align-self: flex-start;
      height: fit-content;
      max-height: calc(100vh - 110px);
      overflow-y: auto;
  }
  ```

---

## 6. INSTRUCCIONES DE DESPLIEGUE Y MANTENIMIENTO

### Ejecución Local de Pruebas:
```bash
python -c "from api.index import app, main_site_pages; print('Servidor OK!')"
```

### Despliegue en Producción (GitHub + Vercel):
```bash
git add .
git commit -m "feat: Update platform to version 18.0"
git push origin main
```
Vercel detecta automáticamente el commit en la rama `main` y realiza el build serverless en menos de 30 segundos.
