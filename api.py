"""
API REST para ProspectScan - Security Heatmap
Expone funcionalidades de app_superficie.py como endpoints JSON
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any
import pandas as pd
from datetime import datetime

# Importar funciones del backend existente
from app_superficie import (
    analizar_dominio,
    analizar_dominios,
    validar_email,
    extraer_dominio,
    resultado_a_tecnico,
    Postura,
    EstadoSPF,
    EstadoDMARC,
    EstadoHTTPS,
    EstadoHeader,
    CACHE_AVAILABLE
)

# Importar análisis enriquecido
from enriched_analysis import generate_enriched_analysis

if CACHE_AVAILABLE:
    from db_cache import query_all_cached, get_cache_stats, _get_connection

# ============================================================================
# CONFIGURACIÓN FASTAPI
# ============================================================================

app = FastAPI(
    title="ProspectScan API",
    description="API para análisis de seguridad de dominios empresariales",
    version="1.0.0"
)

# CORS para permitir requests desde el frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# MODELOS PYDANTIC
# ============================================================================

class DomainAnalysisRequest(BaseModel):
    domain: str
    
    @field_validator('domain')
    @classmethod
    def validate_domain(cls, v):
        if not v or len(v) < 3:
            raise ValueError("Dominio inválido")
        return v.lower().strip()


class BulkAnalysisRequest(BaseModel):
    domains: List[str]
    
    @field_validator('domains')
    @classmethod
    def validate_domains(cls, v):
        if not v or len(v) == 0:
            raise ValueError("Lista de dominios vacía")
        if len(v) > 100:
            raise ValueError("Máximo 100 dominios por request")
        return [d.lower().strip() for d in v]


class EmailListRequest(BaseModel):
    emails: List[str]
    
    @field_validator('emails')
    @classmethod
    def validate_emails(cls, v):
        if not v or len(v) == 0:
            raise ValueError("Lista de emails vacía")
        if len(v) > 100:
            raise ValueError("Máximo 100 emails por request")
        return v


class DomainResponse(BaseModel):
    domain: str
    score: int
    identity_level: str
    exposure_level: str
    general_level: str
    provider: str
    spf_status: str
    dmarc_status: str
    https_status: str
    cdn_waf: Optional[str]
    security_vendors: List[str]
    recommendations: List[str]
    analyzed_at: str


# ============================================================================
# FUNCIONES HELPER
# ============================================================================

def calcular_score(postura_identidad: str, postura_exposicion: str, 
                   estado_spf: str, estado_dmarc: str) -> int:
    """
    Calcula un score 0-100 basado en las posturas y estados.
    Lógica simplificada - en producción usar ML.
    """
    score = 50  # Base
    
    # Postura Identidad (40 puntos)
    if postura_identidad == "Avanzada":
        score += 20
    elif postura_identidad == "Intermedia":
        score += 10
    else:
        score -= 10
    
    # Postura Exposición (40 puntos)
    if postura_exposicion == "Avanzada":
        score += 20
    elif postura_exposicion == "Intermedia":
        score += 10
    else:
        score -= 10
    
    # SPF (10 puntos)
    if estado_spf == "OK":
        score += 5
    elif estado_spf == "Débil":
        score += 2
    else:
        score -= 5
    
    # DMARC (10 puntos)
    if estado_dmarc == "Reject":
        score += 5
    elif estado_dmarc == "Quarantine":
        score += 3
    elif estado_dmarc == "None":
        score += 1
    else:
        score -= 5
    
    return max(0, min(100, score))


def convertir_resultado_a_api(resultado) -> Dict[str, Any]:
    """Convierte ResultadoSuperficie a formato API del Heatmap"""
    
    # Calcular score
    score = calcular_score(
        resultado.identidad.postura.value,
        resultado.exposicion.postura.value,
        resultado.identidad.estado_spf.value,
        resultado.identidad.estado_dmarc.value
    )
    
    # Mapear niveles
    identity_level = resultado.identidad.postura.value
    exposure_level = resultado.exposicion.postura.value
    general_level = resultado.postura_general.value
    
    # Provider
    provider = resultado.identidad.vendor_correo or "Otro"
    
    return {
        "domain": resultado.dominio,
        "score": score,
        "identity_level": identity_level,
        "exposure_level": exposure_level,
        "general_level": general_level,
        "provider": provider,
        "spf_status": resultado.identidad.estado_spf.value,
        "dmarc_status": resultado.identidad.estado_dmarc.value,
        "https_status": resultado.exposicion.https.value,
        "cdn_waf": resultado.exposicion.cdn_waf,
        "security_vendors": resultado.identidad.vendors_seguridad,
        "recommendations": resultado.recomendaciones,
        "analyzed_at": datetime.utcnow().isoformat()
    }


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """Health check"""
    return {
        "status": "ok",
        "service": "ProspectScan API",
        "version": "1.0.0",
        "cache_available": CACHE_AVAILABLE
    }


@app.get("/api/health")
def health():
    """Health check detallado"""
    health_info = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "cache_available": CACHE_AVAILABLE
    }
    
    if CACHE_AVAILABLE:
        try:
            stats = get_cache_stats()
            health_info["cache_stats"] = stats
        except:
            health_info["cache_stats"] = "unavailable"
    
    return health_info


@app.get("/api/domains", response_model=List[DomainResponse])
def get_all_domains():
    """
    Obtiene todos los dominios analizados desde cache.
    Si no hay cache, retorna lista vacía.
    """
    if not CACHE_AVAILABLE:
        return []
    
    try:
        df = query_all_cached()
        
        if df is None or df.empty:
            return []
        
        # Convertir DataFrame a lista de respuestas
        dominios = []
        for _, row in df.iterrows():
            # Parsear los datos del cache
            dominio_data = {
                "domain": row.get("dominio", ""),
                "score": calcular_score(
                    row.get("postura_identidad", "Básica"),
                    row.get("postura_exposicion", "Básica"),
                    row.get("spf_estado", "Ausente"),
                    row.get("dmarc_estado", "Ausente")
                ),
                "identity_level": row.get("postura_identidad", "Básica"),
                "exposure_level": row.get("postura_exposicion", "Básica"),
                "general_level": row.get("postura_general", "Básica"),
                "provider": row.get("correo_proveedor", "Otro") or "Otro",
                "spf_status": row.get("spf_estado", "Ausente"),
                "dmarc_status": row.get("dmarc_estado", "Ausente"),
                "https_status": row.get("https_estado", "No disponible"),
                "cdn_waf": row.get("cdn_waf"),
                "security_vendors": row.get("correo_gateway", "").split(", ") if row.get("correo_gateway") else [],
                "recommendations": [],  # No guardadas en cache
                "analyzed_at": row.get("updated_at", datetime.utcnow().isoformat())
            }
            dominios.append(dominio_data)
        
        return dominios
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener dominios: {str(e)}")


@app.post("/api/analyze/domain", response_model=DomainResponse)
def analyze_single_domain(request: DomainAnalysisRequest):
    """
    Analiza un dominio individual y retorna resultados detallados.
    """
    try:
        resultado = analizar_dominio(request.domain)
        return convertir_resultado_a_api(resultado)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar dominio: {str(e)}")


@app.post("/api/analyze/bulk", response_model=List[DomainResponse])
def analyze_bulk_domains(request: BulkAnalysisRequest):
    """
    Analiza múltiples dominios en paralelo.
    Máximo 100 dominios por request.
    """
    try:
        df = analizar_dominios(request.domains)
        
        # Convertir DataFrame a lista de respuestas
        resultados = []
        for _, row in df.iterrows():
            # Reconstruir resultado desde DataFrame
            resultado_data = {
                "domain": row["Dominio"],
                "score": calcular_score(
                    row["Postura Identidad"],
                    row["Postura Exposición"],
                    row["Estado SPF"],
                    row["Estado DMARC"]
                ),
                "identity_level": row["Postura Identidad"],
                "exposure_level": row["Postura Exposición"],
                "general_level": row["Superficie Digital"],
                "provider": row["Vendor Correo"],
                "spf_status": row["Estado SPF"],
                "dmarc_status": row["Estado DMARC"],
                "https_status": row["HTTPS"],
                "cdn_waf": row["CDN/WAF"] if row["CDN/WAF"] != "No detectado" else None,
                "security_vendors": row["Vendors Seguridad"].split(", ") if row["Vendors Seguridad"] != "Ninguno" else [],
                "recommendations": [],
                "analyzed_at": datetime.utcnow().isoformat()
            }
            resultados.append(resultado_data)
        
        return resultados
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar dominios: {str(e)}")


@app.post("/api/analyze/emails", response_model=List[DomainResponse])
def analyze_from_emails(request: EmailListRequest):
    """
    Extrae dominios de emails y los analiza.
    Filtra dominios personales automáticamente.
    """
    try:
        # Extraer dominios únicos de los emails
        dominios = set()
        for email in request.emails:
            if validar_email(email):
                dominio = extraer_dominio(email)
                if dominio:
                    dominios.add(dominio)
        
        if not dominios:
            raise HTTPException(status_code=400, detail="No se encontraron dominios válidos en los emails")
        
        # Analizar dominios
        df = analizar_dominios(list(dominios))
        
        # Convertir a respuesta
        resultados = []
        for _, row in df.iterrows():
            resultado_data = {
                "domain": row["Dominio"],
                "score": calcular_score(
                    row["Postura Identidad"],
                    row["Postura Exposición"],
                    row["Estado SPF"],
                    row["Estado DMARC"]
                ),
                "identity_level": row["Postura Identidad"],
                "exposure_level": row["Postura Exposición"],
                "general_level": row["Superficie Digital"],
                "provider": row["Vendor Correo"],
                "spf_status": row["Estado SPF"],
                "dmarc_status": row["Estado DMARC"],
                "https_status": row["HTTPS"],
                "cdn_waf": row["CDN/WAF"] if row["CDN/WAF"] != "No detectado" else None,
                "security_vendors": row["Vendors Seguridad"].split(", ") if row["Vendors Seguridad"] != "Ninguno" else [],
                "recommendations": [],
                "analyzed_at": datetime.utcnow().isoformat()
            }
            resultados.append(resultado_data)
        
        return resultados
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar emails: {str(e)}")


@app.get("/api/stats")
def get_statistics():
    """
    Obtiene estadísticas agregadas de todos los dominios analizados.
    """
    if not CACHE_AVAILABLE:
        return {
            "total_domains": 0,
            "cache_available": False
        }
    
    try:
        stats = get_cache_stats()
        return {
            "cache_available": True,
            **stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")


@app.post("/api/analyze/enriched")
def analyze_domain_enriched(request: DomainAnalysisRequest):
    """
    Analiza un dominio y retorna análisis enriquecido con insights comerciales.
    Incluye:
    - Detección de industria
    - Tech stack completo
    - Budget signals
    - Talking points para ventas
    - Estimación de deal size
    - Urgencia de acción
    """
    try:
        # Análisis técnico base
        resultado = analizar_dominio(request.domain)
        
        # Calcular score
        score = calcular_score(
            resultado.identidad.postura.value,
            resultado.exposicion.postura.value,
            resultado.identidad.estado_spf.value,
            resultado.identidad.estado_dmarc.value
        )
        
        # Generar análisis enriquecido
        enriched = generate_enriched_analysis(resultado, score)
        
        # Convertir a dict para JSON response
        return {
            "domain": enriched.domain,
            "industry": enriched.industry,
            "score": enriched.score,
            "posture": enriched.posture,
            "insights": [
                {
                    "category": i.category,
                    "title": i.title,
                    "status": i.status,
                    "technical_detail": i.technical_detail,
                    "business_impact": i.business_impact,
                    "cost_estimate": i.cost_estimate,
                    "recommendation": i.recommendation,
                    "urgency": i.urgency
                }
                for i in enriched.insights
            ],
            "commercial_intel": {
                "budget_signals": enriched.commercial_intel.budget_signals,
                "tech_stack": enriched.commercial_intel.tech_stack,
                "decision_makers": enriched.commercial_intel.decision_makers,
                "pain_points": enriched.commercial_intel.pain_points,
                "estimated_budget": enriched.commercial_intel.estimated_budget,
                "competitive_advantage": enriched.commercial_intel.competitive_advantage
            },
            "executive_summary": enriched.executive_summary,
            "technical_summary": enriched.technical_summary,
            "sales_talking_points": enriched.sales_talking_points,
            "estimated_deal_size": enriched.estimated_deal_size,
            "urgency_level": enriched.urgency_level,
            "analyzed_at": enriched.analyzed_at
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar análisis enriquecido: {str(e)}")


@app.delete("/api/cache/clear")
def clear_cache():
    """
    Limpia completamente el caché de dominios.
    Útil para forzar re-análisis con detección actualizada.
    """
    if not CACHE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Cache no disponible")
    
    try:
        conn = _get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cur = conn.cursor()
        cur.execute("TRUNCATE TABLE dominios_cache;")
        conn.commit()
        
        # Obtener conteo antes de cerrar
        cur.execute("SELECT COUNT(*) FROM dominios_cache;")
        count = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return {
            "status": "success",
            "message": "Caché limpiado completamente",
            "domains_remaining": count,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al limpiar caché: {str(e)}")


# ============================================================================
# ARRANQUE
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
