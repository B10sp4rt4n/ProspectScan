# 🎯 ProspectScan

**Identifica oportunidades de seguridad en tus prospectos en segundos**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tu-app.streamlit.app)

## 🎯 Para qué sirve

**Para equipos de ventas B2B de ciberseguridad:**
- Analiza la postura de seguridad de prospectos antes de la llamada
- Identifica gaps específicos de correo y web
- Prioriza leads por potencial comercial
- Genera argumentos técnicos de venta

## 🚀 Productos incluidos

| Aplicación | Enfoque | Comando |
|------------|---------|---------|
| [app_superficie.py](app_superficie.py) | **ProspectScan Completo (Recomendado)** | `streamlit run app_superficie.py` |
| [app.py](app.py) | Solo correo (SPF/DMARC) | `streamlit run app.py` |
| [app_web.py](app_web.py) | Solo web (Headers/SSL) | `streamlit run app_web.py` |

## 📊 Qué analiza

### 🔐 Identidad Digital (Correo)
- **SPF**: OK / Débil / Ausente
- **DMARC**: Reject / Quarantine / None / Ausente  
- **Vendors de correo**: Microsoft 365, Google Workspace, etc.
- **Gateways de seguridad**: Proofpoint, Mimecast, Barracuda, etc.
- **Servicios de envío**: SendGrid, Mailgun, Amazon SES, etc.

### 🌐 Exposición Digital (Web)
- **HTTPS**: Forzado / Disponible / No disponible
- **Headers de seguridad**: HSTS, CSP, X-Frame-Options, etc.
- **CDN/WAF**: Cloudflare, Akamai, Imperva, etc.
- **Servidor**: Nginx, Apache, IIS, etc.

### 📈 Postura General
- **Básica**: Gaps evidentes → Alta prioridad comercial
- **Intermedia**: Algunos controles → Oportunidad moderada  
- **Avanzada**: Bien protegido → Baja prioridad

## 🔧 Instalación local

```bash
git clone https://github.com/B10sp4rt4n/prospectscan
cd prospectscan
pip install -r requirements.txt
streamlit run app_superficie.py
```

## 📁 Formato de entrada

CSV con columna de emails corporativos:

```csv
email,company,contact
juan.perez@empresa1.com,Empresa 1,Juan Pérez
maria.lopez@empresa2.com,Empresa 2,María López
```

## 📤 Formato de salida

### Resumen Ejecutivo
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

## ☁️ Deploy en Streamlit Cloud

### Pasos rápidos:
1. **Fork** este repositorio a tu cuenta de GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io) e inicia sesión
3. Click en **"New app"**
4. Selecciona tu repositorio fork
5. Configura:
   - **Main file path**: `app_superficie.py`
   - **Python version**: 3.11 (recomendado)
6. Click **"Deploy"**

### Configurar Secrets (opcional):
En tu app desplegada, ve a **Settings > Secrets** y añade:

```toml
# Para análisis con IA (opcional)
OPENAI_API_KEY = "sk-proj-xxx"

# Para cache persistente (opcional)  
NEON_CONNECTION_STRING = "postgresql://..."
```

> 💡 La app funciona completamente sin secrets. OpenAI mejora los insights y Neon acelera re-análisis.

### URL de tu app:
`https://[tu-usuario]-prospectscan-[sufijo].streamlit.app`