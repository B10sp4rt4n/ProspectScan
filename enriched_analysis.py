"""
Generador de Análisis Enriquecido para ProspectScan
Convierte datos técnicos en insights comerciales accionables
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import re

from app_superficie import (
    ResultadoSuperficie,
    Postura,
    EstadoSPF,
    EstadoDMARC,
    EstadoHTTPS,
    obtener_mx,
    obtener_spf,
    obtener_dmarc
)

# ============================================================================
# CATÁLOGOS DE INTELIGENCIA COMERCIAL
# ============================================================================

VENDOR_COSTS = {
    "Hornetsecurity": {"min": 15, "max": 25, "unit": "€/usuario/año"},
    "Proofpoint": {"min": 25, "max": 45, "unit": "$/usuario/año"},
    "Mimecast": {"min": 30, "max": 50, "unit": "$/usuario/año"},
    "Microsoft 365": {"min": 12, "max": 20, "unit": "$/usuario/año"},
    "Google Workspace": {"min": 6, "max": 18, "unit": "$/usuario/año"},
    "Cloudflare": {"min": 200, "max": 5000, "unit": "$/mes"},
    "Akamai": {"min": 5000, "max": 50000, "unit": "$/mes"},
}

INDUSTRY_MAPPING = {
    r'retail|tienda|super|shop|store|chedraui|soriana|liverpool': 'Retail',
    r'bank|banco|financial|hsbc|bbva|santander': 'Financiero',
    r'hotel|resort|tourism|viaje|travel': 'Hospitalidad',
    r'tech|software|cloud|saas': 'Tecnología',
    r'health|hospital|clinic|salud': 'Salud',
    r'edu|school|university|universidad': 'Educación',
    r'gov|gobierno|gob\.': 'Gobierno',
}

ISSUE_SEVERITY = {
    "ssl_invalid": {
        "severity": "CRITICAL",
        "revenue_impact": {"min": 200000, "max": 500000, "unit": "USD/mes"},
        "fix_time": "24-48h",
        "cost": {"min": 0, "max": 500, "unit": "USD/año"}
    },
    "no_waf": {
        "severity": "HIGH",
        "revenue_impact": {"min": 50000, "max": 200000, "unit": "USD/año"},
        "fix_time": "1-2 semanas",
        "cost": {"min": 2400, "max": 60000, "unit": "USD/año"}
    },
    "weak_dmarc": {
        "severity": "MEDIUM",
        "revenue_impact": {"min": 10000, "max": 50000, "unit": "USD/año"},
        "fix_time": "2-4 días",
        "cost": {"min": 0, "max": 0, "unit": "USD"}
    }
}


@dataclass
class EnrichedInsight:
    """Insight enriquecido con contexto comercial"""
    category: str  # "ssl", "email", "infrastructure", "compliance"
    title: str
    status: str  # "critical", "warning", "ok"
    technical_detail: str
    business_impact: str
    cost_estimate: Optional[Dict]
    recommendation: str
    urgency: str  # "immediate", "high", "medium", "low"


@dataclass
class CommercialIntelligence:
    """Inteligencia comercial del prospecto"""
    budget_signals: List[str]
    tech_stack: List[str]
    decision_makers: List[str]
    pain_points: List[str]
    estimated_budget: Dict[str, Any]
    competitive_advantage: List[str]


@dataclass
class EnrichedAnalysis:
    """Análisis completo enriquecido"""
    domain: str
    industry: str
    score: int
    posture: str
    insights: List[EnrichedInsight]
    commercial_intel: CommercialIntelligence
    executive_summary: str
    technical_summary: str
    sales_talking_points: List[str]
    estimated_deal_size: Dict[str, Any]
    urgency_level: str
    analyzed_at: str


# ============================================================================
# DETECCIÓN DE INDUSTRIA
# ============================================================================

def detect_industry(domain: str, mx_records: List[str], spf: str) -> str:
    """Detecta la industria basándose en el dominio y configuración"""
    domain_lower = domain.lower()
    
    for pattern, industry in INDUSTRY_MAPPING.items():
        if re.search(pattern, domain_lower):
            return industry
    
    # Heurísticas adicionales
    if "edu" in domain_lower or ".edu." in domain_lower:
        return "Educación"
    
    if ".gob." in domain_lower or ".gov" in domain_lower:
        return "Gobierno"
    
    return "Corporativo"


# ============================================================================
# DETECCIÓN DE TECH STACK
# ============================================================================

def detect_tech_stack(resultado: ResultadoSuperficie) -> List[str]:
    """Detecta el stack tecnológico completo"""
    stack = []
    
    # Email providers
    if resultado.identidad.vendor_correo:
        stack.append(f"Email: {resultado.identidad.vendor_correo}")
    
    # Security gateways
    for vendor in resultado.identidad.vendors_seguridad:
        stack.append(f"Email Security: {vendor}")
    
    # Sending services
    for vendor in resultado.identidad.vendors_envio:
        stack.append(f"Email Sending: {vendor}")
    
    # CDN/WAF
    if resultado.exposicion.cdn_waf:
        stack.append(f"CDN/WAF: {resultado.exposicion.cdn_waf}")
    
    # Web server
    if resultado.exposicion.servidor:
        stack.append(f"Server: {resultado.exposicion.servidor}")
    
    # Detectar cloud provider por MX o servidor
    mx_records = obtener_mx(resultado.dominio)
    mx_text = " ".join(mx_records).lower()
    
    if "amazonaws" in mx_text or "aws" in resultado.exposicion.servidor.lower() if resultado.exposicion.servidor else False:
        stack.append("Cloud: AWS")
    elif "google" in mx_text:
        stack.append("Cloud: Google Cloud")
    elif "azure" in mx_text or "microsoft" in mx_text:
        stack.append("Cloud: Azure")
    
    return stack


# ============================================================================
# ANÁLISIS DE BUDGET SIGNALS
# ============================================================================

def analyze_budget_signals(resultado: ResultadoSuperficie, tech_stack: List[str]) -> Dict:
    """Analiza señales de presupuesto"""
    signals = []
    estimated_annual = {"min": 0, "max": 0}
    
    # Security gateway = presupuesto alto
    for vendor in resultado.identidad.vendors_seguridad:
        if vendor in VENDOR_COSTS:
            cost = VENDOR_COSTS[vendor]
            signals.append(f"{vendor}: {cost['min']}-{cost['max']} {cost['unit']}")
            # Estimar para 500-1000 usuarios promedio
            estimated_annual["min"] += cost["min"] * 500
            estimated_annual["max"] += cost["max"] * 1000
    
    # Email provider
    if resultado.identidad.vendor_correo in VENDOR_COSTS:
        cost = VENDOR_COSTS[resultado.identidad.vendor_correo]
        signals.append(f"{resultado.identidad.vendor_correo}: {cost['min']}-{cost['max']} {cost['unit']}")
        estimated_annual["min"] += cost["min"] * 500
        estimated_annual["max"] += cost["max"] * 1000
    
    # CDN/WAF
    if resultado.exposicion.cdn_waf and resultado.exposicion.cdn_waf in VENDOR_COSTS:
        cost = VENDOR_COSTS[resultado.exposicion.cdn_waf]
        signals.append(f"{resultado.exposicion.cdn_waf}: {cost['min']}-{cost['max']} {cost['unit']}")
        estimated_annual["min"] += cost["min"] * 12
        estimated_annual["max"] += cost["max"] * 12
    
    return {
        "signals": signals,
        "estimated_annual": estimated_annual,
        "budget_conscious": len(signals) > 0
    }


# ============================================================================
# GENERACIÓN DE INSIGHTS ENRIQUECIDOS
# ============================================================================

def generate_ssl_insight(resultado: ResultadoSuperficie, industry: str) -> Optional[EnrichedInsight]:
    """Genera insight sobre SSL"""
    if resultado.exposicion.https != EstadoHTTPS.FORZADO:
        issue = ISSUE_SEVERITY["ssl_invalid"]
        
        # Impacto varía por industria
        impact_multiplier = {
            "Retail": 1.5,
            "Financiero": 2.0,
            "Tecnología": 1.2,
            "Salud": 1.8
        }.get(industry, 1.0)
        
        min_loss = int(issue["revenue_impact"]["min"] * impact_multiplier)
        max_loss = int(issue["revenue_impact"]["max"] * impact_multiplier)
        
        return EnrichedInsight(
            category="ssl",
            title="Certificado SSL Inválido o Ausente",
            status="critical",
            technical_detail=f"HTTPS: {resultado.exposicion.https.value}. Los navegadores mostrarán advertencias de seguridad.",
            business_impact=f"Pérdida estimada: ${min_loss:,}-${max_loss:,} USD/mes en conversión. Penalización SEO activa. Riesgo de compliance.",
            cost_estimate={
                "fix_cost": f"${issue['cost']['min']}-${issue['cost']['max']} {issue['cost']['unit']}",
                "potential_loss": f"${min_loss:,}-${max_loss:,} USD/mes"
            },
            recommendation="Implementar Let's Encrypt (gratuito) o AWS Certificate Manager si usa AWS. Tiempo de fix: 2-4 horas.",
            urgency="immediate"
        )
    
    return None


def generate_waf_insight(resultado: ResultadoSuperficie, industry: str) -> Optional[EnrichedInsight]:
    """Genera insight sobre WAF/CDN"""
    if not resultado.exposicion.cdn_waf:
        issue = ISSUE_SEVERITY["no_waf"]
        
        return EnrichedInsight(
            category="infrastructure",
            title="Sin WAF/CDN de Protección",
            status="warning",
            technical_detail="No se detectaron headers de Cloudflare, Akamai, Fastly u otros proveedores de protección.",
            business_impact=f"Vulnerable a ataques DDoS, sin optimización de latencia, costos elevados de bandwidth. Pérdida potencial: ${issue['revenue_impact']['min']:,}-${issue['revenue_impact']['max']:,}/año.",
            cost_estimate={
                "solution_cost": "Cloudflare Pro: $200/mes, Enterprise: $5K/mes",
                "roi_time": "3-6 meses (recuperado en ahorro de bandwidth + uptime)"
            },
            recommendation=f"Implementar Cloudflare para empresas de {industry}. Reducción de 40-60% en costos de infraestructura.",
            urgency="high"
        )
    
    return None


def generate_email_insight(resultado: ResultadoSuperficie) -> Optional[EnrichedInsight]:
    """Genera insight sobre configuración de email"""
    if resultado.identidad.vendors_seguridad:
        # Tiene seguridad = budget signal positivo
        vendor = resultado.identidad.vendors_seguridad[0]
        cost_info = VENDOR_COSTS.get(vendor, {})
        
        return EnrichedInsight(
            category="email",
            title="Seguridad de Email: Excelente",
            status="ok",
            technical_detail=f"Gateway de seguridad: {vendor}. SPF: {resultado.identidad.estado_spf.value}. DMARC: {resultado.identidad.estado_dmarc.value}.",
            business_impact=f"Inversión activa en ciberseguridad (~${cost_info.get('min', 20)}-{cost_info.get('max', 40)}/usuario/año). Cliente B2B calificado.",
            cost_estimate={
                "current_spend": f"~$50K-$100K/año estimado",
                "expansion_opportunity": "Extender seguridad a infraestructura web"
            },
            recommendation=f"Usar como talking point: 'Su inversión en {vendor} es excelente. ¿Han considerado el mismo nivel de protección para su web?'",
            urgency="medium"
        )
    elif resultado.identidad.estado_dmarc in [EstadoDMARC.AUSENTE, EstadoDMARC.NONE]:
        return EnrichedInsight(
            category="email",
            title="DMARC Ausente o Débil",
            status="warning",
            technical_detail=f"DMARC: {resultado.identidad.estado_dmarc.value}. El dominio es vulnerable a phishing y spoofing.",
            business_impact="Riesgo de suplantación de identidad, phishing a clientes, daño reputacional. Costo promedio de incidente: $50K-$200K.",
            cost_estimate={
                "fix_cost": "$0 (configuración gratuita)",
                "avoided_cost": "$50K-$200K por incidente prevenido"
            },
            recommendation="Implementar DMARC con política 'quarantine' inicialmente, luego 'reject'. Monitoreo con herramientas gratuitas como DMARC Analyzer.",
            urgency="high"
        )
    
    return None


# ============================================================================
# GENERACIÓN DE EXECUTIVE SUMMARY
# ============================================================================

def generate_executive_summary(resultado: ResultadoSuperficie, insights: List[EnrichedInsight], industry: str, score: int) -> str:
    """Genera resumen ejecutivo"""
    critical_count = sum(1 for i in insights if i.status == "critical")
    warning_count = sum(1 for i in insights if i.status == "warning")
    
    posture_emoji = {
        "Avanzada": "🟢",
        "Intermedia": "🟡",
        "Básica": "🔴"
    }.get(resultado.postura_general.value, "⚪")
    
    summary = f"""
**Dominio:** {resultado.dominio}
**Industria:** {industry}
**Score:** {score}/100 {posture_emoji} {resultado.postura_general.value}

**Hallazgos:**
- Críticos: {critical_count}
- Advertencias: {warning_count}
- Configuraciones correctas: {len([i for i in insights if i.status == 'ok'])}

**Urgencia:** {"🔴 ALTA - Acción inmediata requerida" if critical_count > 0 else "🟡 MEDIA - Planificar mejoras" if warning_count > 0 else "🟢 BAJA - Mantenimiento preventivo"}
"""
    
    return summary.strip()


# ============================================================================
# SALES TALKING POINTS
# ============================================================================

def generate_sales_talking_points(resultado: ResultadoSuperficie, insights: List[EnrichedInsight], commercial_intel: CommercialIntelligence) -> List[str]:
    """Genera puntos de conversación para ventas"""
    points = []
    
    # Punto 1: Contradicción entre inversiones
    if commercial_intel.budget_signals and any(i.status == "critical" for i in insights):
        points.append(
            f"Detectamos inversión en seguridad ({', '.join(commercial_intel.budget_signals[:2])}), "
            f"pero identificamos vulnerabilidades críticas en su infraestructura web. "
            f"Esta contradicción pone en riesgo su inversión actual."
        )
    
    # Punto 2: Impacto financiero cuantificado
    critical_insights = [i for i in insights if i.status == "critical"]
    if critical_insights:
        insight = critical_insights[0]
        if insight.cost_estimate and "potential_loss" in insight.cost_estimate:
            points.append(
                f"{insight.title}: {insight.cost_estimate['potential_loss']} de pérdida potencial. "
                f"Solución: {insight.cost_estimate.get('fix_cost', 'Variable')}. "
                f"ROI inmediato."
            )
    
    # Punto 3: Comparación con competencia
    if resultado.postura_general.value == "Básica":
        points.append(
            f"Su postura de seguridad actual es Básica. Competidores líderes en {commercial_intel.tech_stack[0] if commercial_intel.tech_stack else 'su industria'} "
            f"mantienen postura Avanzada. Esta brecha puede afectar contratos empresariales."
        )
    
    # Punto 4: Quick wins
    free_fixes = [i for i in insights if i.cost_estimate and "0" in str(i.cost_estimate.get("fix_cost", ""))]
    if free_fixes:
        points.append(
            f"Identificamos {len(free_fixes)} mejoras de costo cero con ROI inmediato. "
            f"Podemos implementarlas en {free_fixes[0].recommendation.split('Tiempo de fix:')[-1].strip() if 'Tiempo de fix:' in free_fixes[0].recommendation else '48 horas'}."
        )
    
    return points[:4]  # Top 4 talking points


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def generate_enriched_analysis(resultado: ResultadoSuperficie, score: int) -> EnrichedAnalysis:
    """Genera análisis completamente enriquecido"""
    
    # Detectar industria
    mx_records = obtener_mx(resultado.dominio)
    spf = obtener_spf(resultado.dominio)
    industry = detect_industry(resultado.dominio, mx_records, spf)
    
    # Detectar tech stack
    tech_stack = detect_tech_stack(resultado)
    
    # Generar insights
    insights = []
    
    # SSL
    ssl_insight = generate_ssl_insight(resultado, industry)
    if ssl_insight:
        insights.append(ssl_insight)
    
    # WAF/CDN
    waf_insight = generate_waf_insight(resultado, industry)
    if waf_insight:
        insights.append(waf_insight)
    
    # Email
    email_insight = generate_email_insight(resultado)
    if email_insight:
        insights.append(email_insight)
    
    # Analizar budget signals
    budget_analysis = analyze_budget_signals(resultado, tech_stack)
    
    # Commercial intelligence
    commercial_intel = CommercialIntelligence(
        budget_signals=budget_analysis["signals"],
        tech_stack=tech_stack,
        decision_makers=["CTO", "CISO", f"Director de {industry}"] if industry != "Corporativo" else ["CTO", "CISO"],
        pain_points=[i.title for i in insights if i.status in ["critical", "warning"]],
        estimated_budget=budget_analysis["estimated_annual"],
        competitive_advantage=[
            "Análisis técnico automatizado",
            "Inteligencia comercial integrada",
            "ROI cuantificado por problema"
        ]
    )
    
    # Executive summary
    executive_summary = generate_executive_summary(resultado, insights, industry, score)
    
    # Sales talking points
    sales_points = generate_sales_talking_points(resultado, insights, commercial_intel)
    
    # Estimated deal size
    critical_fixes = len([i for i in insights if i.status == "critical"])
    warning_fixes = len([i for i in insights if i.status == "warning"])
    
    deal_size = {
        "setup": f"${5000 + (critical_fixes * 3000) + (warning_fixes * 1500):,} USD",
        "monthly": f"${1000 + (critical_fixes * 500) + (warning_fixes * 200):,} USD",
        "annual": f"${12000 + (critical_fixes * 6000) + (warning_fixes * 2400):,} USD",
        "confidence": "high" if critical_fixes > 0 else "medium"
    }
    
    # Urgency level
    urgency = "immediate" if critical_fixes > 0 else "high" if warning_fixes > 1 else "medium"
    
    return EnrichedAnalysis(
        domain=resultado.dominio,
        industry=industry,
        score=score,
        posture=resultado.postura_general.value,
        insights=insights,
        commercial_intel=commercial_intel,
        executive_summary=executive_summary,
        technical_summary=f"{len(insights)} hallazgos | {critical_fixes} críticos | {warning_fixes} advertencias",
        sales_talking_points=sales_points,
        estimated_deal_size=deal_size,
        urgency_level=urgency,
        analyzed_at=datetime.utcnow().isoformat()
    )
