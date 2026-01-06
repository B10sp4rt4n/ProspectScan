# ProspectScan - OpenAI Integration

Integración completa con OpenAI para post-procesamiento de análisis estructurales.

## 🎯 Funcionalidades Implementadas

### 1. **Reformulación por Audiencia**
Adapta el análisis técnico para diferentes públicos:
- **Ejecutivo (C-Level)**: Riesgos de negocio, impacto financiero, estrategia
- **Técnico (CISO/IT)**: Controles específicos, gaps técnicos, implementación
- **Comercial (Sales/BDR)**: Oportunidades de venta, pain points, timing

### 2. **Clasificación de Urgencia**
Determina automáticamente:
- Nivel de urgencia (crítica/alta/media/baja)
- Timeframe recomendado para contacto
- Ángulo principal de conversación
- Razón basada en hallazgos

### 3. **Generación de Emails**
Crea emails de prospección personalizados:
- Asunto impactante
- Referencia a hallazgos específicos
- Propuesta de valor clara
- Call-to-action efectivo

### 4. **Procesamiento Batch**
- Procesa hasta 10 dominios por batch (configurable)
- Progress tracking en tiempo real
- Exportación de resultados en CSV
- Vista comparativa original vs OpenAI

## ⚙️ Configuración

### Opción 1: Streamlit Secrets (Recomendado)

```bash
# Crear archivo de secrets
mkdir -p .streamlit
cp secrets.toml.example .streamlit/secrets.toml

# Editar con tu API key
nano .streamlit/secrets.toml
```

Contenido de `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-proj-XXXXXXXXX"
```

### Opción 2: Variables de Entorno

```bash
export OPENAI_API_KEY="sk-proj-XXXXXXXXX"
```

### Opción 3: Input Manual en UI

- No requiere configuración previa
- Ingresa la API key directamente en Streamlit
- Solo válido para la sesión actual

## 📦 Instalación

```bash
# Instalar dependencia OpenAI
pip install openai

# Verificar instalación
python -c "from analisis_estructural import OPENAI_AVAILABLE; print('OK' if OPENAI_AVAILABLE else 'ERROR')"
```

## 🚀 Uso

### Desde Streamlit (UI)

1. Ve al tab **"Análisis Estructural"**
2. Genera análisis normales primero
3. Configura OpenAI API Key (si no está en secrets)
4. Selecciona acción:
   - Resumen Ejecutivo
   - Resumen Técnico
   - Resumen Comercial
   - Clasificar Urgencia
   - Generar Email
5. Haz clic en **"🚀 Procesar con OpenAI"**

### Desde Python (API)

```python
from analisis_estructural import (
    reformular_con_openai,
    clasificar_urgencia_con_openai,
    generar_email_prospeccion_con_openai,
    procesar_batch_con_openai
)

# Reformular para ejecutivo
resumen = reformular_con_openai(
    analisis="[análisis original]",
    audiencia="ejecutivo",
    api_key="sk-proj-xxx",
    modelo="gpt-4"
)

# Clasificar urgencia
clasificacion = clasificar_urgencia_con_openai(
    analisis="[análisis original]",
    api_key="sk-proj-xxx"
)

# Generar email
email = generar_email_prospeccion_con_openai(
    analisis="[análisis original]",
    api_key="sk-proj-xxx"
)

# Procesar múltiples
resultados = procesar_batch_con_openai(
    resultados=[...],
    accion="reformular_ejecutivo",
    api_key="sk-proj-xxx"
)
```

## 💡 Prompts Internos

Los prompts están optimizados para:

### System Prompt Base
```
Eres un analista de ciberseguridad experto.
Reformula el análisis proporcionado SOLO con información disponible.
NUNCA inventes datos, métricas o información que no esté en el original.
Si algo no está disponible, no lo menciones.
```

### Temperatura
- **0.2**: Para clasificación (más determinístico)
- **0.3**: Para reformulación (balance precisión/fluidez)
- **0.4**: Para generación de emails (más creativo)

## 📊 Modelos Disponibles

| Modelo | Velocidad | Costo | Calidad | Recomendado para |
|--------|-----------|-------|---------|------------------|
| `gpt-4` | Lento | Alto | Excelente | Análisis críticos |
| `gpt-4-turbo` | Medio | Medio | Excelente | Uso general |
| `gpt-3.5-turbo` | Rápido | Bajo | Bueno | Pruebas, batch grandes |

## 💰 Costos Aproximados

Con GPT-4 (precios aprox, verificar en OpenAI):
- **Input**: ~$0.03 / 1K tokens
- **Output**: ~$0.06 / 1K tokens

Promedio por análisis:
- Análisis original: ~1000 tokens input
- Respuesta: ~500 tokens output
- **Costo**: ~$0.06 por análisis

Batch de 10 dominios: **~$0.60**

## 🔒 Seguridad

### Mejores Prácticas

1. **Nunca commitees API keys**:
   ```bash
   # .gitignore ya incluye:
   .streamlit/secrets.toml
   .env
   ```

2. **Usa secrets en producción**:
   - Streamlit Cloud: Settings > Secrets
   - Docker: Variables de entorno
   - GitHub Actions: Repository Secrets

3. **Limita permisos de API Key**:
   - Solo permisos de "Chat Completions"
   - Configura limits de gasto en OpenAI

4. **Monitorea uso**:
   - Dashboard de OpenAI: usage tracking
   - Logs de costos por sesión

## 🛠️ Troubleshooting

### Error: "Module OpenAI not available"
```bash
pip install openai
```

### Error: "API Key not configured"
Verifica en orden:
1. `.streamlit/secrets.toml` existe y tiene `OPENAI_API_KEY`
2. Variable de entorno: `echo $OPENAI_API_KEY`
3. Input manual en UI

### Error: "Rate limit exceeded"
- Espera unos segundos
- Reduce batch size
- Upgrade tu plan en OpenAI

### Error: "Insufficient quota"
- Verifica créditos en tu cuenta OpenAI
- Añade método de pago si es necesario

## 📈 Roadmap

Futuras mejoras planificadas:

- [ ] Soporte para Azure OpenAI
- [ ] Caché de respuestas OpenAI
- [ ] Streaming de respuestas largas
- [ ] Modo comparison (A/B testing de prompts)
- [ ] Fine-tuning personalizado
- [ ] Métricas de calidad de respuestas
- [ ] Integración con Copilot Studio

## 📝 Ejemplos de Uso

### Caso 1: Pipeline de Prospección Automatizado

```python
# 1. Generar análisis estructurales
resultados = procesar_csv("prospectscan_20260106.csv")

# 2. Clasificar por urgencia
clasificados = procesar_batch_con_openai(
    resultados,
    accion="clasificar",
    api_key=api_key
)

# 3. Filtrar críticos/altos
urgentes = [r for r in clasificados 
            if r['openai_output']['urgencia'] in ['critica', 'alta']]

# 4. Generar emails para urgentes
emails = procesar_batch_con_openai(
    urgentes,
    accion="email",
    api_key=api_key
)

# 5. Exportar para BDRs
df_emails = pd.DataFrame(emails)
df_emails.to_csv("emails_prospecting.csv")
```

### Caso 2: Reportes Ejecutivos Batch

```python
# Generar resúmenes ejecutivos de todos los dominios críticos
df = pd.read_csv("pipeline_criticos.csv")
resultados = procesar_dataframe(df)

resumenes = procesar_batch_con_openai(
    resultados,
    accion="reformular_ejecutivo",
    api_key=api_key,
    modelo="gpt-4"
)

# Exportar para presentación a C-Level
exportar_markdown(resumenes, "resumen_ejecutivo_Q1.md")
```

## 🤝 Integración con Otros Sistemas

### Zapier/Make.com
```python
# Endpoint webhook que recibe dominio
@app.post("/analizar_y_clasificar")
def analizar_webhook(dominio: str):
    analisis = generar_analisis_estructural({"dominio": dominio, ...})
    clasificacion = clasificar_urgencia_con_openai(analisis)
    
    # Enviar a CRM si es crítico
    if clasificacion['urgencia'] == 'critica':
        crm.create_lead(dominio, clasificacion)
    
    return clasificacion
```

### Slack Bot
```python
# Comando /prospectscan dominio.com
@slack_app.command("/prospectscan")
def prospectscan_command(ack, command):
    dominio = command['text']
    analisis = generar_analisis_estructural_rapido(dominio)
    resumen = reformular_con_openai(analisis, "comercial")
    
    ack(f"📊 Análisis de {dominio}:\n{resumen}")
```

## ⚖️ Consideraciones Legales

### AUP Compliance
- ✅ Solo analiza superficie pública
- ✅ No inventa información
- ✅ OpenAI procesa solo datos observables
- ✅ No almacena análisis en servidores de OpenAI

### GDPR
- Los análisis no contienen PII
- Datos de dominios corporativos (públicos)
- Opcional: anonimizar nombres de empresa

### OpenAI Terms
- Cumple con OpenAI Usage Policies
- No usa para entrenar modelos (opt-out disponible)
- Monitorea uso según términos

## 📞 Soporte

Para problemas específicos de OpenAI:
- [OpenAI Platform Status](https://status.openai.com/)
- [OpenAI Help Center](https://help.openai.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

Para ProspectScan:
- Ver logs: `tail -f /tmp/streamlit.log`
- Debug mode: Activar en Streamlit
- Issues: GitHub repository
