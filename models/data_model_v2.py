"""
ProspectScan - Modelo de Datos v2.0
Contextual Decision Intelligence for Cybersecurity

Arquitectura de 5 capas según PROMPT_MAESTRO.md
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# ============================================================================
# CAPA 1: INGESTA MASIVA (Fuente Externa)
# ============================================================================

class FuenteDatos(Enum):
    """Fuentes de datos válidas - ZoomInfo es la fuente de verdad"""
    ZOOMINFO = "zoominfo"
    MANUAL = "manual"  # Solo para testing/demo


@dataclass
class Snapshot:
    """
    Unidad atómica de ingesta. Inmutable una vez creado.
    ProspectScan NO edita snapshots, solo los interpreta.
    """
    snapshot_id: str
    fuente: FuenteDatos
    timestamp_ingesta: datetime
    version: int  # Incrementa con cada refresco
    datos_crudos: Dict[str, Any]  # Payload de ZoomInfo sin modificar
    checksum: str  # Para validar integridad
    
    # Metadatos de ingesta
    registros_totales: int
    registros_nuevos: int
    registros_actualizados: int


@dataclass
class EmpresaFuente:
    """
    Datos crudos de empresa desde ZoomInfo.
    ProspectScan NO modifica estos campos.
    """
    # Identificadores (de ZoomInfo)
    zoominfo_id: str
    dominio: str
    
    # Datos empresariales (solo lectura)
    nombre_empresa: str
    industria: str
    sub_industria: Optional[str]
    empleados_rango: str  # "1-10", "11-50", etc.
    ingresos_rango: Optional[str]  # "$1M-$10M", etc.
    pais: str
    estado_region: Optional[str]
    
    # Señales de ZoomInfo (interpretativas)
    crecimiento_empleados_12m: Optional[float]  # % cambio
    funding_reciente: Optional[bool]
    tech_stack_conocido: List[str]
    
    # Metadatos de snapshot
    snapshot_id: str
    timestamp_fuente: datetime


# ============================================================================
# CAPA 2: BASE CONTEXTUAL EMPRESARIAL (Derivada)
# ============================================================================

class EstadoOrganizacional(Enum):
    """Estados derivados del contexto empresarial"""
    ESTABLE = "estable"
    EN_CRECIMIENTO = "en_crecimiento"
    EN_TRANSICION = "en_transicion"
    EN_CONTRACCION = "en_contraccion"
    MA_ACTIVO = "ma_activo"  # M&A
    DESCONOCIDO = "desconocido"


class PresionExterna(Enum):
    """Nivel de presión externa interpretada"""
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


@dataclass
class ContextoEmpresarial:
    """
    Interpretación contextual derivada de datos fuente.
    NO contiene datos técnicos de seguridad.
    NO rastrea personas individuales.
    """
    dominio: str
    
    # Derivados de EmpresaFuente
    estado_organizacional: EstadoOrganizacional
    ritmo_cambio: str  # "lento", "moderado", "acelerado"
    presion_externa: PresionExterna
    
    # Indicadores de oportunidad (no técnicos)
    señales_inversion: List[str]  # "funding", "expansion", "hiring"
    madurez_digital: str  # "emergente", "en_desarrollo", "madura"
    
    # Industria y regulación
    industria_detectada: str
    regulaciones_aplicables: List[str]  # "GDPR", "PCI-DSS", etc.
    
    # Metadatos
    snapshot_origen: str
    timestamp_derivacion: datetime
    confianza_derivacion: float  # 0.0 - 1.0


# ============================================================================
# CAPA 3: BASE DE POSTURA DE SEGURIDAD (Técnica, Agregada)
# ============================================================================

class NivelPostura(Enum):
    """Niveles agregados de postura - NO diagnóstico técnico"""
    BASICA = "basica"
    INTERMEDIA = "intermedia"
    AVANZADA = "avanzada"


@dataclass
class PosturaSeguridad:
    """
    Postura de seguridad agregada.
    Es técnica, fría, sin contexto de negocio.
    ProspectScan NO profundiza en detalle técnico.
    """
    dominio: str
    
    # Posturas agregadas (sin detalle técnico)
    postura_identidad: NivelPostura  # Email security
    postura_exposicion: NivelPostura  # Web security
    postura_general: NivelPostura  # Combinada
    
    # Score numérico (0-100, solo para ordenamiento)
    score_agregado: int
    
    # Tech stack detectado (para cruce, no diagnóstico)
    vendors_email: List[str]
    vendors_seguridad: List[str]
    cdn_waf: Optional[str]
    
    # Indicadores booleanos simples
    tiene_spf: bool
    tiene_dmarc: bool
    tiene_https: bool
    tiene_hsts: bool
    
    # Metadatos
    timestamp_analisis: datetime
    fuente_analisis: str  # "dns_scan", "header_check", etc.


# ============================================================================
# CAPA 4: MOTOR PROSPECTSCAN (Cruce Semántico)
# ============================================================================

class PrioridadAccion(Enum):
    """Resultado del cruce - NO es diagnóstico, es priorización"""
    CRITICA = "critica"  # Actuar inmediatamente
    ALTA = "alta"  # Priorizar esta semana
    MEDIA = "media"  # Revisar en 2 semanas
    BAJA = "baja"  # Monitorear
    DESCARTADA = "descartada"  # No es momento


@dataclass
class ResultadoCruce:
    """
    Output del Motor ProspectScan.
    Responde: ¿Es prudente anticipar una iniciativa de seguridad?
    NO responde: ¿Qué vulnerabilidad existe?
    """
    dominio: str
    
    # Inputs del cruce
    contexto: ContextoEmpresarial
    postura: PosturaSeguridad
    
    # Output principal
    prioridad: PrioridadAccion
    score_oportunidad: int  # 0-100
    
    # Razones del cruce (para humano)
    factores_positivos: List[str]
    factores_negativos: List[str]
    
    # Señales de timing
    momento_oportuno: bool
    razon_momento: str
    
    # Budget estimado (rango, no exacto)
    budget_estimado_min: int
    budget_estimado_max: int
    
    # Talking points generados
    talking_points: List[str]
    
    # Metadatos
    timestamp_cruce: datetime
    version_reglas: str


# ============================================================================
# CAPA 5: MÓDULO FOCUS (Humano en el Loop)
# ============================================================================

class EstadoFocus(Enum):
    """Estados del review humano"""
    PENDIENTE = "pendiente"  # Esperando revisión
    EN_REVISION = "en_revision"
    VALIDADO = "validado"  # Humano confirmó
    RECHAZADO = "rechazado"  # Humano descartó
    REQUIERE_REFRESCO = "requiere_refresco"  # Inconsistencia detectada


@dataclass
class ReviewFocus:
    """
    Validación humana sobre ResultadoCruce.
    NO modifica datos fuente.
    """
    dominio: str
    resultado_cruce_id: str
    
    # Estado del review
    estado: EstadoFocus
    reviewer_id: str
    
    # Notas del humano
    notas: Optional[str]
    ajuste_prioridad: Optional[PrioridadAccion]  # Override humano
    
    # Links de referencia (NO scrapeados)
    linkedin_company_url: Optional[str]  # Solo referencia, de ZoomInfo
    
    # Si hay inconsistencia
    solicita_refresco: bool
    razon_refresco: Optional[str]
    
    # Timestamps
    timestamp_asignacion: datetime
    timestamp_completado: Optional[datetime]


# ============================================================================
# REGLAS DE CRUCE (Motor ProspectScan)
# ============================================================================

REGLAS_CRUCE = {
    # (EstadoOrganizacional, NivelPostura) -> PrioridadAccion
    
    # Transición = siempre oportunidad
    (EstadoOrganizacional.EN_TRANSICION, NivelPostura.BASICA): PrioridadAccion.CRITICA,
    (EstadoOrganizacional.EN_TRANSICION, NivelPostura.INTERMEDIA): PrioridadAccion.ALTA,
    (EstadoOrganizacional.EN_TRANSICION, NivelPostura.AVANZADA): PrioridadAccion.MEDIA,
    
    # M&A = máxima prioridad
    (EstadoOrganizacional.MA_ACTIVO, NivelPostura.BASICA): PrioridadAccion.CRITICA,
    (EstadoOrganizacional.MA_ACTIVO, NivelPostura.INTERMEDIA): PrioridadAccion.CRITICA,
    (EstadoOrganizacional.MA_ACTIVO, NivelPostura.AVANZADA): PrioridadAccion.ALTA,
    
    # Crecimiento = oportunidad moderada
    (EstadoOrganizacional.EN_CRECIMIENTO, NivelPostura.BASICA): PrioridadAccion.ALTA,
    (EstadoOrganizacional.EN_CRECIMIENTO, NivelPostura.INTERMEDIA): PrioridadAccion.MEDIA,
    (EstadoOrganizacional.EN_CRECIMIENTO, NivelPostura.AVANZADA): PrioridadAccion.BAJA,
    
    # Estable = depende de postura
    (EstadoOrganizacional.ESTABLE, NivelPostura.BASICA): PrioridadAccion.MEDIA,
    (EstadoOrganizacional.ESTABLE, NivelPostura.INTERMEDIA): PrioridadAccion.BAJA,
    (EstadoOrganizacional.ESTABLE, NivelPostura.AVANZADA): PrioridadAccion.DESCARTADA,
    
    # Contracción = bajo potencial
    (EstadoOrganizacional.EN_CONTRACCION, NivelPostura.BASICA): PrioridadAccion.BAJA,
    (EstadoOrganizacional.EN_CONTRACCION, NivelPostura.INTERMEDIA): PrioridadAccion.DESCARTADA,
    (EstadoOrganizacional.EN_CONTRACCION, NivelPostura.AVANZADA): PrioridadAccion.DESCARTADA,
}


def ejecutar_cruce(contexto: ContextoEmpresarial, postura: PosturaSeguridad) -> PrioridadAccion:
    """
    Motor de cruce semántico.
    Solo ejecuta reglas explícitas, NO inventa.
    """
    key = (contexto.estado_organizacional, postura.postura_general)
    return REGLAS_CRUCE.get(key, PrioridadAccion.MEDIA)


# ============================================================================
# MENSAJE OBLIGATORIO EN TODOS LOS OUTPUTS
# ============================================================================

DISCLAIMER_PROSPECTSCAN = """
┌────────────────────────────────────────────────────────────┐
│  Fuente de datos: ZoomInfo                                 │
│  ProspectScan refleja el último snapshot validado.         │
│  Los cambios se actualizan mediante nuevas ingestas.       │
└────────────────────────────────────────────────────────────┘
"""
