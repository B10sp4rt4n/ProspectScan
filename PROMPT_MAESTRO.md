# 🧠 PROMPT MAESTRO — ProspectScan

## Contextual Decision Intelligence for Cybersecurity

---

## CONTEXTO GENERAL

Estás trabajando en **ProspectScan**, un sistema de inteligencia de decisión enfocado en ciberseguridad.

### ProspectScan NO es:
- ❌ una fuente de datos
- ❌ un sistema de corrección de información
- ❌ una herramienta de detección técnica
- ❌ un motor de scraping
- ❌ un reemplazo de herramientas de seguridad

### ProspectScan SÍ es:
- ✅ un sistema de interpretación contextual
- ✅ un motor de priorización
- ✅ un termómetro previo a diagnósticos profundos
- ✅ una herramienta de triaje estratégico
- ✅ un habilitador de criterio humano

---

## PRINCIPIO RECTOR (INQUEBRANTABLE)

> **ProspectScan no es la fuente de la verdad.**
> **La fuente de la verdad es ZoomInfo (o su proveedor equivalente).**
> **ProspectScan interpreta snapshots provistos por la fuente.**

⚠️ Cualquier diseño, código o flujo que contradiga esto es incorrecto.

---

## MODELO MENTAL DEL SISTEMA

ProspectScan responde a esta pregunta:

> **¿El contexto actual de una empresa hace prudente anticipar una iniciativa de seguridad?**

**NO responde:**
- qué vulnerabilidad existe
- qué control falta
- qué falla técnica hay

---

## ORDEN DE CAPAS (DEBE RESPETARSE)

Copilot debe respetar estrictamente este orden:

```
┌─────────────────────────────────────────────────────────────┐
│  CAPA 1: Ingesta Masiva (fuente externa - ZoomInfo)         │
├─────────────────────────────────────────────────────────────┤
│  CAPA 2: Base Contextual Empresarial                        │
├─────────────────────────────────────────────────────────────┤
│  CAPA 3: Base de Postura de Seguridad                       │
├─────────────────────────────────────────────────────────────┤
│  CAPA 4: Motor ProspectScan (cruce semántico)               │
├─────────────────────────────────────────────────────────────┤
│  CAPA 5: Módulo Focus (criterio humano)                     │
└─────────────────────────────────────────────────────────────┘
```

**Ninguna capa puede saltarse otra.**

---

## REGLAS DE INGESTA Y GOBIERNO DEL CAMBIO

1. Toda información entra **únicamente por ingesta masiva**
2. ProspectScan **no edita, no corrige, no sobrescribe** datos
3. Los cambios de estado ocurren **solo cuando la fuente se refresca**
4. Cada refresco genera un **nuevo snapshot**
5. El snapshot más reciente es el vigente
6. El historial se conserva **solo con fines interpretativos**

❌ **Está prohibido generar lógica tipo UPDATE sobre datos fuente.**

---

## BASE CONTEXTUAL EMPRESARIAL (CAPA 2)

ProspectScan mantiene una **base contextual**, separada de la postura de seguridad.

### Esta base REPRESENTA:
- dinámica organizacional
- ritmo de cambio
- transiciones
- presión externa

### Esta base NO REPRESENTA:
- personas individuales
- actividad social
- datos técnicos de seguridad

Los valores de esta base son **derivados e interpretativos**, no crudos.

---

## BASE DE POSTURA DE SEGURIDAD (CAPA 3)

La postura de seguridad:
- es técnica
- es agregada
- es fría
- puede venir de múltiples herramientas

**ProspectScan no profundiza en detalle técnico.**
Solo utiliza la postura como una **dimensión más del cruce**.

---

## MOTOR ProspectScan (CAPA 4 - CRUCE SEMÁNTICO)

El motor cruza:
- **Contexto empresarial** (Capa 2)
- **Postura de seguridad** (Capa 3)

El resultado **NO es un diagnóstico**, es una **prioridad de acción**.

### Ejemplo conceptual:

| Contexto | Postura | → Prioridad |
|----------|---------|-------------|
| En transición | Media | **Alta** |
| Estable | Baja | **Baja** |
| Crecimiento rápido | Alta | **Media** |
| M&A activo | Cualquiera | **Crítica** |

⚠️ Copilot **no debe inventar reglas**, solo ejecutar reglas explícitas.

---

## MÓDULO FOCUS (CAPA 5 - HUMANO EN EL LOOP)

El Módulo Focus:
- se activa **solo en casos priorizados**
- introduce **validación humana obligatoria**
- **no modifica datos fuente**

### LinkedIn:
- ❌ NO es fuente de datos
- ❌ NO se scrapea
- ❌ NO se automatiza
- ✅ Solo se usa como **referencia manual**, mediante enlaces provistos por ZoomInfo

### Si hay inconsistencia:
1. El usuario decide refrescar la fuente
2. ProspectScan espera la nueva ingesta

---

## MENSAJE QUE EL SISTEMA DEBE COMUNICAR SIEMPRE

```
┌────────────────────────────────────────────────────────────┐
│  Fuente de datos: ZoomInfo                                 │
│  ProspectScan refleja el último snapshot validado.         │
│  Los cambios se actualizan mediante nuevas ingestas.       │
└────────────────────────────────────────────────────────────┘
```

Este mensaje debe aparecer en:
- UI
- logs
- documentación
- outputs

---

## LÍMITES EXPLÍCITOS (NO NEGOCIABLES)

### ProspectScan NO:
- ❌ rastrea personas
- ❌ monitorea en tiempo real
- ❌ predice incidentes
- ❌ genera miedo
- ❌ reemplaza herramientas de seguridad

### ProspectScan SÍ:
- ✅ prioriza
- ✅ contextualiza
- ✅ anticipa
- ✅ habilita conversaciones
- ✅ pone al humano donde agrega valor

---

## FRASE GUÍA (PARA VALIDAR CUALQUIER OUTPUT)

Antes de generar cualquier diseño o código, valida esto:

> **¿Esto ayuda a decidir CUÁNDO tiene sentido profundizar en seguridad,
> sin afirmar que sabemos QUÉ está mal técnicamente?**

Si la respuesta es **no**, el diseño es incorrecto.

---

## MAPEO CON CÓDIGO EXISTENTE

| Capa | Archivo Actual | Estado |
|------|----------------|--------|
| Capa 1: Ingesta | `db_cache.py` | Parcial - falta integración ZoomInfo |
| Capa 2: Contexto | `enriched_analysis.py` | ✅ Industria, transiciones |
| Capa 3: Postura | `app_superficie.py` | ✅ SPF/DMARC/SSL/Headers |
| Capa 4: Motor | `enriched_analysis.py` | ✅ Cruce y priorización |
| Capa 5: Focus | Frontend | 🔜 Pendiente |

---

## FIN DEL CONTRATO CONCEPTUAL

A partir de aquí, Copilot puede:
- ✅ generar esquemas de datos
- ✅ diseñar APIs
- ✅ proponer flujos
- ✅ escribir pipelines

**Siempre respetando este documento como contrato conceptual.**
