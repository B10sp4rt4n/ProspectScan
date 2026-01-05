# 🎯 ProspectScan

**Contextual Decision Intelligence for Cybersecurity Sales**

Plataforma de inteligencia para identificar y priorizar oportunidades de venta en ciberseguridad basada en análisis contextual de empresas.

[![React](https://img.shields.io/badge/React-18.3-blue)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-yellow)](https://www.python.org/)

## 🎯 Para qué sirve

**Para equipos de ventas B2B de ciberseguridad:**
- 📊 Analiza reportes de ZoomInfo con información empresarial
- 🔍 Evalúa postura de seguridad técnica (DNS, HTTPS, headers)
- 🎯 Prioriza prospectos con algoritmo de cruce contextual
- 💬 Genera talking points automáticos para ventas
- 💰 Estima budget potencial por industria y tamaño
- 📈 Visualiza oportunidades en heatmap interactivo

## 🏗️ Arquitectura (5 Capas)

```
📥 Capa 1: Ingesta          → ZoomInfo Excel upload
📋 Capa 2: Contexto         → Estado organizacional + Presión externa
🔐 Capa 3: Postura          → DNS/TLS/Headers analysis
🎯 Capa 4: ProspectScan     → Cruce semántico (Contexto × Postura)
👁️ Capa 5: Focus (WIP)     → Human review queue
```

Ver [PROMPT_MAESTRO.md](PROMPT_MAESTRO.md) para arquitectura completa.

## 🚀 Quick Start

### Opción 1: UI Completa (React)

```bash
# Terminal 1: Backend
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

**URLs:**
- 🎨 Frontend: http://localhost:3000
- 🔌 Backend API: http://localhost:8000
- 📖 API Docs: http://localhost:8000/docs

### Opción 2: API directa (curl)

```bash
# 1. Upload ZoomInfo Excel
curl -X POST http://localhost:8000/api/ingesta/upload \
  -F "file=@test_data/zoominfo_sample.xlsx"

# 2. Ejecutar cruce semántico
curl -X POST http://localhost:8000/api/cruce/batch \
  -H "Content-Type: application/json" \
  -d '{"snapshot_id": "zoominfo_20241231_abc123"}'
```

Ver [USAGE_GUIDE.md](USAGE_GUIDE.md) para ejemplos completos.

## 📊 Módulos de la Plataforma

### 1️⃣ Ingesta de Datos
**Fuente:** Reportes ZoomInfo en Excel

**Columnas soportadas:**
- Company Name / Company / Organization
- Website / Domain / Company Website
- Industry / Industry Category
- Employees / Company Size / Employee Count
- Revenue / Annual Revenue / Company Revenue
- Technologies / Tech Stack / Technology

**Proceso:**
1. Upload de archivo Excel via drag & drop
2. Mapeo automático de columnas con variaciones
3. Generación de snapshot inmutable (SHA256 checksum)
4. Extracción de dominios para análisis técnico

### 2️⃣ Contexto Empresarial
**Derivación automática basada en ZoomInfo:**

**Estado Organizacional:**
- `estable`: Revenue plano, crecimiento < 10%
- `crecimiento_acelerado`: Growth > 20%
- `cambio_estructural`: Mergers, adquisiciones, restructuring

**Presión Externa:**
- `alta`: Finanzas, salud, regulado
- `media`: Retail, manufactura
- `baja`: Servicios generales

### 3️⃣ Postura de Seguridad
**Análisis técnico automatizado:**

| Dimensión | Indicadores | Valores |
|-----------|-------------|---------|
| **Email** | SPF, DMARC | ok, debil, ausente |
| **Web** | HTTPS, HSTS, Headers | forzado, disponible, no_disponible |
| **Vendors** | Proveedores detectados | Microsoft 365, Cloudflare, etc. |

**Clasificación:**
- `basica`: Gaps críticos (SPF ausente, no HTTPS)
- `reactiva`: Controles básicos presentes
- `proactiva`: DMARC reject, HSTS habilitado
- `avanzada`: Full security headers, CDN/WAF

### 4️⃣ Motor ProspectScan
**Algoritmo de priorización (REGLAS_CRUCE):**

```python
Prioridad = f(Contexto Empresarial, Postura Seguridad)

Matriz 4x4:
                básica  reactiva  proactiva  avanzada
estable         ALTA    MEDIA     BAJA       DESCARTADA
crec_acelerado  CRÍTICA ALTA      MEDIA      BAJA
cambio_struct   CRÍTICA ALTA      MEDIA      DESCARTADA
```

**Output por prospecto:**
- 🎯 Score de oportunidad (0-100)
- 🚨 Prioridad (crítica/alta/media/baja/descartada)
- 💰 Budget estimado por industria
- 💬 Talking points automáticos
- 📋 Regulaciones aplicables

**Ejemplo real (walmex.mx):**
```json
{
  "dominio": "walmex.mx",
  "score": 83,
  "prioridad": "MEDIA",
  "budget_estimado": "$50,000 - $150,000",
  "factores_positivos": [
    "Alta presión regulatoria (industria regulada)",
    "Gran capacidad de inversión (>$1B revenue)"
  ],
  "factores_negativos": [
    "Postura reactiva requiere convencimiento de valor"
  ],
  "momento_oportuno": "Su crecimiento acelerado...",
  "regulaciones": ["Ley Federal de Protección de Datos", "Ley FinTech"]
}
```

### 5️⃣ Visualización Heatmap
**Grid interactivo de dominios:**

**Dimensiones visualizadas:**
- TLS Version (color-coding)
- Proveedores de infraestructura
- Headers de seguridad
- Estado DNSSEC

**Filtros:**
- Por proveedor (Cloudflare, AWS, etc.)
- Por estado TLS (1.2, 1.3, insecure)
- Por features de seguridad

## 🔧 Instalación Completa

```bash
# 1. Clonar repositorio
git clone https://github.com/B10sp4rt4n/prospectscan
cd prospectscan

# 2. Backend dependencies
pip install -r requirements.txt

# 3. Frontend dependencies
cd frontend
npm install
cd ..

# 4. Configurar variables de entorno (opcional)
cp .env.example .env
# Editar DATABASE_URL si usas PostgreSQL
```

## 📁 Estructura del Proyecto

```
prospectscan/
├── api.py                          # FastAPI main app
├── ingesta/
│   └── zoominfo_adapter.py         # Capa 1: Excel parser
├── motor/
│   └── cruce_semantico.py          # Capa 4: Scoring engine
├── models/
│   └── data_model_v2.py            # Dataclasses para todas las capas
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Router principal
│   │   ├── components/
│   │   │   ├── ZoomInfoUpload.jsx  # Ingesta UI
│   │   │   ├── CrucePipeline.jsx   # Pipeline UI
│   │   │   └── DomainHeatmap.jsx   # Heatmap UI
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── test_data/
│   └── zoominfo_sample.xlsx        # Datos de prueba (5 empresas)
├── PROMPT_MAESTRO.md               # Arquitectura 5 capas
├── USAGE_GUIDE.md                  # Guía de API completa
├── UNIFIED_UI_ARCHITECTURE.md      # Documentación UI
└── README.md                       # Este archivo
```

## 📤 Testing con Datos de Ejemplo

### Dataset incluido (test_data/zoominfo_sample.xlsx):

| Empresa | Dominio | Industria | Empleados | Revenue |
|---------|---------|-----------|-----------|---------|
| Walmart México | walmex.mx | Retail | 50,000+ | $1B+ |
| Chedraui | chedraui.com.mx | Retail | 10,000+ | $500M+ |
| Banorte | banorte.com | Financial | 5,000+ | $1B+ |
| BBVA México | bbva.mx | Financial | 10,000+ | $1B+ |
| Liverpool | liverpool.com.mx | Retail | 20,000+ | $500M+ |

### Resultados esperados:

```
✅ walmex.mx          - Score 83 - MEDIA      - $50K-$150K
✅ chedraui.com.mx    - Score 68 - BAJA       - $50K-$150K
✅ banorte.com        - Score 68 - BAJA       - $100K-$250K
❌ bbva.mx            - DESCARTADA (postura avanzada)
❌ liverpool.com.mx   - DESCARTADA (postura avanzada)
```

## 📖 Documentación Adicional

| Documento | Descripción |
|-----------|-------------|
| [PROMPT_MAESTRO.md](PROMPT_MAESTRO.md) | Contrato conceptual de 5 capas |
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | API endpoints con ejemplos curl |
| [UNIFIED_UI_ARCHITECTURE.md](UNIFIED_UI_ARCHITECTURE.md) | Arquitectura frontend React |
| [COMPETITIVE_ANALYSIS.md](COMPETITIVE_ANALYSIS.md) | Análisis vs competidores |

## 🌐 Endpoints API

### Ingesta
- `POST /api/ingesta/upload` - Upload ZoomInfo Excel

### Cruce Semántico
- `POST /api/cruce/batch` - Ejecutar pipeline completo
- `POST /api/cruce/analizar` - Análisis ad-hoc de dominio
- `GET /api/cruce/{dominio}` - Obtener resultado individual

### Análisis Técnico (Heatmap)
- `POST /api/domains/analyze` - Análisis DNS/TLS batch
- `GET /api/domains/{domain}` - Detalle de dominio individual

Ver `/api/docs` para Swagger UI interactivo.

## 🎓 Casos de Uso

### Caso 1: Preparación de llamada de ventas
```bash
# 1. Sales rep recibe lista de 50 prospectos en ZoomInfo
# 2. Upload Excel → obtiene priorización automática
# 3. Filtra por CRÍTICA/ALTA → reduce a 15 prospectos
# 4. Lee talking points generados para cada uno
# 5. Ordena llamadas por score descendente
```

### Caso 2: Análisis de vertical
```bash
# 1. Export ZoomInfo de industria "Financial Services"
# 2. Upload → analiza 200 bancos y fintechs
# 3. Visualiza en heatmap proveedores dominantes
# 4. Identifica clusters con posturas básicas/reactivas
# 5. Genera campaña segmentada por prioridad
```

### Caso 3: Follow-up informado
```bash
# 1. Prospecto dice "ya tenemos controles"
# 2. Busca dominio en pipeline → ve postura "reactiva"
# 3. Lee factores negativos específicos
# 4. Contraargumenta con gaps detectados
# 5. Cierra con regulación aplicable
```

## 🚀 Roadmap

### ✅ Completado
- [x] Arquitectura 5 capas (4/5 implementadas)
- [x] Ingesta ZoomInfo con mapeo flexible
- [x] Motor de cruce semántico con REGLAS_CRUCE
- [x] API RESTful con FastAPI
- [x] UI unificada en React con navegación
- [x] Heatmap de visualización
- [x] Testing con datos reales mexicanos

### 🔄 En progreso
- [ ] Capa 5: Módulo Focus (human review)
- [ ] Persistencia en PostgreSQL (actualmente in-memory)
- [ ] Autenticación y multi-tenancy

### 📋 Planeado
- [ ] Exportar resultados a PDF
- [ ] Integración con CRM (Salesforce, HubSpot)
- [ ] Alertas de cambios en postura de prospectos
- [ ] ML para refinar scoring con feedback de ventas
- [ ] Expansión a LATAM (regulaciones por país)

## 🤝 Contribuciones

```bash
# 1. Fork el repositorio
# 2. Crea branch de feature
git checkout -b feature/nueva-funcionalidad

# 3. Commit cambios
git commit -m "feat: descripción de cambio"

# 4. Push y abre PR
git push origin feature/nueva-funcionalidad
```

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## 📞 Soporte

- 🐛 **Bugs:** [GitHub Issues](https://github.com/B10sp4rt4n/prospectscan/issues)
- 💡 **Features:** [GitHub Discussions](https://github.com/B10sp4rt4n/prospectscan/discussions)
- 📧 **Contacto:** [tu-email@example.com](mailto:tu-email@example.com)

---

**ProspectScan** - Contextual Decision Intelligence for Cybersecurity Sales  
Hecho con ❤️ para equipos de ventas B2B

| Dominio | Postura Identidad | Postura Exposición | Vendor Correo | Seguridad Correo | CDN/WAF | Superficie Digital |
|---------|-------------------|--------------------|--------------|-----------------|---------|--------------------|
| empresa1.com | Básica | Intermedia | Microsoft 365 | Sin gateway | Sin protección | Básica |

### Anexo Técnico
Incluye todos los registros DNS y headers HTTP detectados para análisis técnico.

## 🎯 Casos de uso comercial

**Para vendedores de:**
- Proofpoint, Mimecast → Identifica empresas sin gateway de correo
- Cloudflare, Imperva → Encuentra sitios sin WAF/CDN  
- CrowdStrike, Threatdown → Usa DMARC débil como indicador de riesgo
- Consultoras → Genera reportes ejecutivos de postura

**Flujo típico:**
1. Exporta lista de prospectos de LinkedIn/ZoomInfo/CRM
2. Sube CSV al diagnóstico  
3. Filtra por "Postura Básica" = oportunidades calientes
4. Contacta con gaps específicos identificados

## 🏗️ Arquitectura técnica

- **Frontend**: Streamlit (Python)
- **Datos**: DNS público (MX, TXT), HTTP headers
- **Sin dependencias**: No requiere APIs de pago
- **Sin acceso**: Análisis pasivo, no intrusivo
- **Escalable**: Análisis paralelo con ThreadPoolExecutor

## 📝 Licencia

MIT License - Libre para uso comercial

## 🤝 Contribuciones

PRs bienvenidos. Para cambios mayores, abre un issue primero.

---

**⚡ Deploy en Streamlit Cloud:**
1. Fork este repo
2. Conecta tu cuenta de Streamlit Cloud
3. Selecciona `app_superficie.py` como main file
4. ¡Listo! Tu app estará en `https://tu-usuario-prospectscan-app-superficie-main.streamlit.app`