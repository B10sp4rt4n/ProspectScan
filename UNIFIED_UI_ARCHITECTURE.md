# Arquitectura UI Unificada - ProspectScan

## 🎯 Decisión de Diseño

**Antes:** Dos frontends en paralelo
- ❌ Streamlit (app_superficie.py, app_web.py)
- ⚛️ React (frontend/)

**Ahora:** UI unificada en React
- ✅ Una sola experiencia de usuario
- ✅ Navegación fluida entre módulos
- ✅ Diseño moderno y responsive

---

## 📐 Estructura del Frontend

```
frontend/
├── src/
│   ├── App.jsx                    # Router principal con navegación
│   ├── App.css                    # Estilos globales unificados
│   ├── components/
│   │   ├── ZoomInfoUpload.jsx     # 🔴 Capa 1: Ingesta
│   │   ├── ZoomInfoUpload.css
│   │   ├── CrucePipeline.jsx      # 🔴 Capas 2-4: Pipeline completo
│   │   ├── CrucePipeline.css
│   │   ├── DomainHeatmap.jsx      # 🔴 Visualización heatmap
│   │   ├── FilterBar.jsx
│   │   ├── HeatmapGrid.jsx
│   │   ├── DomainDetail.jsx
│   │   └── EnrichedAnalysis.jsx
│   └── main.jsx
├── package.json
└── vite.config.js
```

---

## 🚦 Flujo de Usuario

### 1️⃣ Ingesta (Ruta: `/ingesta`)
**Componente:** `ZoomInfoUpload.jsx`

**Funcionalidad:**
- Drag & drop para archivos Excel de ZoomInfo
- Validación de tipo de archivo (.xlsx, .xls)
- Upload a `/api/ingesta/upload`
- Muestra snapshot_id generado
- Lista dominios extraídos
- Referencia de columnas soportadas

**Estados:**
- `idle`: Zona de drop inicial
- `uploading`: Spinner de carga
- `success`: Snapshot creado con detalles
- `error`: Mensajes de error descriptivos

**Output:**
```json
{
  "snapshot_id": "zoominfo_20241231_abc123",
  "empresas_count": 5,
  "dominios": ["walmex.mx", "chedraui.com.mx", ...],
  "columnas_mapeadas": {...}
}
```

---

### 2️⃣ Pipeline de Cruce (Ruta: `/cruce`)
**Componente:** `CrucePipeline.jsx`

**Funcionalidad:**
- Botón "Ejecutar Cruce" para procesar snapshot
- Filtro por prioridad: crítica, alta, media, baja
- Ejecución de `/api/cruce/batch`
- Visualización de resultados en tarjetas

**Información por tarjeta:**
- 🎯 Score de oportunidad (0-100)
- 🚨 Prioridad (color-coded)
- 💰 Budget estimado
- ✅ Factores positivos (bullets)
- ❌ Factores negativos (bullets)
- 💬 Talking points para ventas
- 📋 Regulaciones aplicables

**Código de colores:**
- 🔴 Crítica: #dc3545 (rojo)
- 🟠 Alta: #fd7e14 (naranja)
- 🟡 Media: #ffc107 (amarillo)
- 🟢 Baja: #28a745 (verde)
- ⚫ Descartada: #6c757d (gris)

**Ejemplo resultado:**
```
┌─────────────────────────────────────┐
│ walmex.mx                           │
│ Score: 83/100 | Prioridad: MEDIA    │
│ Budget: $50,000 - $150,000          │
├─────────────────────────────────────┤
│ ✅ Factores Positivos:              │
│ • Alta presión regulatoria          │
│ • Gran capacidad de inversión       │
│                                     │
│ ❌ Factores Negativos:              │
│ • Postura reactiva requiere trabajo │
│                                     │
│ 💬 Talking Points:                  │
│ "Su crecimiento acelerado..."       │
└─────────────────────────────────────┘
```

---

### 3️⃣ Heatmap de Dominios (Ruta: `/heatmap`)
**Componente:** `DomainHeatmap.jsx`

**Funcionalidad:**
- Visualización de matriz de seguridad
- Filtros: proveedor, estado TLS, DNS security
- Grid interactivo con tooltips
- Panel lateral con análisis enriquecido

**Métricas visualizadas:**
- TLS Version (color de célula)
- DNS Security (DNSSEC, CAA)
- Proveedor de infraestructura
- Estado general de seguridad

---

## 🔗 Navegación Unificada

**Header persistente:**
```jsx
<nav className="app-nav">
  <div className="nav-brand">
    <h1>ProspectScan</h1>
    <p className="nav-subtitle">
      Contextual Decision Intelligence for Cybersecurity
    </p>
  </div>
  <div className="nav-links">
    <Link to="/ingesta" className="nav-link">Ingesta</Link>
    <Link to="/cruce" className="nav-link">Pipeline</Link>
    <Link to="/heatmap" className="nav-link">Heatmap</Link>
  </div>
</nav>
```

**Footer persistente:**
```jsx
<footer className="app-footer">
  <p>
    ProspectScan - Cybersecurity Intelligence Platform
    <a href="https://github.com/tu-repo">GitHub</a>
    <a href="/api/docs">API Docs</a>
  </p>
</footer>
```

---

## 🎨 Sistema de Diseño

### Paleta de colores:
- **Primary:** Gradiente morado (#667eea → #764ba2)
- **Background:** #f5f7fa
- **Cards:** White con sombras sutiles
- **Text:** #2c3e50 (principal), #6c757d (secundario)

### Tipografía:
- **Font family:** System fonts (San Francisco, Segoe UI, Roboto)
- **Sizes:** 
  - H1: 2rem (nav brand)
  - H2: 1.5rem (títulos de sección)
  - Body: 1rem
  - Small: 0.9rem (subtítulos)

### Animaciones:
- Transiciones suaves (0.3s ease)
- Hover effects en botones y links
- Spinner CSS puro (sin dependencias)
- Transform en tarjetas (-2px translateY)

---

## 🔌 Integración con API

### Endpoints utilizados:

| Endpoint | Método | Componente | Propósito |
|----------|--------|------------|-----------|
| `/api/ingesta/upload` | POST | ZoomInfoUpload | Subir Excel ZoomInfo |
| `/api/cruce/batch` | POST | CrucePipeline | Ejecutar pipeline completo |
| `/api/cruce/{dominio}` | GET | CrucePipeline | Obtener resultado individual |
| `/api/domains/analyze` | POST | DomainHeatmap | Análisis DNS/TLS |

### Gestión de estado:

**App.jsx mantiene:**
```jsx
const [currentSnapshot, setCurrentSnapshot] = useState(null);
```

**Flujo de datos:**
1. `ZoomInfoUpload` → crea snapshot → `setCurrentSnapshot(snapshot_id)`
2. `CrucePipeline` → recibe `currentSnapshot` → ejecuta cruce
3. Resultados persisten en backend (in-memory storage)

---

## 📦 Dependencias

### NPM packages:
```json
{
  "react": "^18.3.1",
  "react-dom": "^18.3.1",
  "react-router-dom": "^6.29.1",
  "react-dropzone": "^14.3.5"
}
```

### Dev dependencies:
```json
{
  "@vitejs/plugin-react": "^4.3.4",
  "vite": "^5.4.21"
}
```

---

## 🚀 Instrucciones de Despliegue

### Desarrollo local:

```bash
# Terminal 1: Backend
cd /workspaces/dns_profile
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd /workspaces/dns_profile/frontend
npm install
npm run dev
```

**URLs:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Producción:

```bash
# Build frontend
cd frontend
npm run build
# Output: dist/ folder

# Servir estáticos desde FastAPI
# Agregar a api.py:
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="frontend/dist", html=True))
```

---

## ✅ Testing del Flujo Completo

### Prueba manual:

1. **Abrir UI:** http://localhost:3000
2. **Ir a Ingesta:** Click en tab "Ingesta"
3. **Subir archivo:** Drag & drop `test_data/zoominfo_sample.xlsx`
4. **Verificar snapshot:** Debe mostrar 5 empresas, 5 dominios
5. **Ir a Pipeline:** Click en tab "Pipeline"
6. **Ejecutar cruce:** Click "Ejecutar Cruce"
7. **Filtrar resultados:** Seleccionar "media" en filtro de prioridad
8. **Ver detalles:** Expandir tarjeta de walmex.mx

**Resultado esperado:**
```
walmex.mx - Score 83 - MEDIA
Budget: $50,000 - $150,000
✅ 2 factores positivos
❌ 1 factor negativo
💬 Talking point generado
📋 Ley FinTech aplicable
```

---

## 🔄 Migración desde Streamlit

### Archivos deprecados:
- ❌ `app_superficie.py` (ahora vía API)
- ❌ `app_web.py` (ahora vía API)
- ❌ `app.py` (reemplazado por `api.py`)

### Funcionalidad migrada:

| Streamlit | React | Estado |
|-----------|-------|--------|
| `st.file_uploader()` | `ZoomInfoUpload.jsx` | ✅ Migrado |
| `st.dataframe()` | `CrucePipeline.jsx` tarjetas | ✅ Migrado |
| `st.metric()` | Badges color-coded | ✅ Migrado |
| Filtros sidebar | `FilterBar.jsx` | ✅ Migrado |

### Ventajas de React sobre Streamlit:

| Aspecto | Streamlit | React |
|---------|-----------|-------|
| **Performance** | Re-render completo | Virtual DOM optimizado |
| **UX** | Recarga página | SPA fluido |
| **Customización** | Limitada | Total control CSS/JS |
| **Producción** | Escalabilidad limitada | Production-ready |
| **Mobile** | Adaptación básica | Responsive nativo |

---

## 🎓 Capacitación del Equipo

### Para usuarios finales:
1. **Ingesta:** "Arrastra tu reporte ZoomInfo aquí"
2. **Pipeline:** "Click para ver prioridades de prospectos"
3. **Heatmap:** "Visualiza seguridad de dominios"

### Para desarrolladores:
- 📚 Ver código en `/frontend/src/components/`
- 📖 Leer `USAGE_GUIDE.md` para API
- 🔧 Modificar estilos en archivos `.css` correspondientes
- 🧪 Testear con `test_data/zoominfo_sample.xlsx`

---

## 📊 Métricas de Éxito

### KPIs UI:
- ⏱️ Tiempo de carga inicial: < 2s
- 📤 Tiempo de upload Excel: < 3s
- 🔄 Tiempo ejecución cruce (5 empresas): < 10s
- 📱 Mobile responsiveness: 100%

### KPIs UX:
- 👤 Claridad de navegación: Intuitiva
- 🎨 Consistencia visual: Unificada
- 🔔 Feedback de acciones: Inmediato
- ❌ Tasa de error: Minimizada con validaciones

---

## 🛠️ Próximos Pasos

### Capa 5: Módulo Focus (pendiente)
- [ ] Componente `ReviewQueue.jsx`
- [ ] CRUD para ReviewFocus
- [ ] Estados: Pendiente → En Revisión → Validado/Rechazado
- [ ] Asignación de reviewer
- [ ] Comentarios y notas

### Mejoras UI:
- [ ] Dark mode toggle
- [ ] Exportar resultados a PDF
- [ ] Compartir snapshot via link
- [ ] Historial de uploads
- [ ] Comparación entre snapshots

### DevOps:
- [ ] Dockerfile para frontend
- [ ] CI/CD con GitHub Actions
- [ ] Deploy en Vercel/Netlify (frontend)
- [ ] Deploy en Railway/Render (backend)

---

## 📞 Soporte

**Documentación:**
- [README.md](README.md) - Visión general
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Guía de API
- [PROMPT_MAESTRO.md](PROMPT_MAESTRO.md) - Arquitectura 5 capas
- [COMPETITIVE_ANALYSIS.md](COMPETITIVE_ANALYSIS.md) - Análisis de mercado

**Contacto:**
- GitHub Issues para bugs
- Pull Requests para features
- Slack #prospectscan para consultas

---

**Última actualización:** 31 de diciembre de 2024  
**Versión UI:** 2.0.0 (React unificado)  
**Estado:** ✅ Producción
