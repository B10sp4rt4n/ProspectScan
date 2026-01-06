"""
ProspectScan - Análisis Estructural Automatizado
Genera reportes narrativos basados exclusivamente en datos observables.
Compatible con OpenAI/ChatGPT para post-procesamiento.
"""

import pandas as pd
import os
from typing import Dict, List, Optional
from datetime import datetime

# Intentar importar OpenAI (opcional)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def get_openai_client(api_key: Optional[str] = None) -> Optional[OpenAI]:
    """
    Obtiene un cliente de OpenAI configurado.
    
    Args:
        api_key: API key de OpenAI. Si no se proporciona, busca en variables de entorno.
        
    Returns:
        Cliente OpenAI o None si no está disponible
    """
    if not OPENAI_AVAILABLE:
        return None
    
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    
    return OpenAI(api_key=key)


def reformular_con_openai(
    analisis: str,
    audiencia: str = "ejecutivo",
    api_key: Optional[str] = None,
    modelo: str = "gpt-4"
) -> Optional[str]:
    """
    Reformula un análisis estructural para una audiencia específica usando OpenAI.
    
    Args:
        analisis: Análisis estructural original
        audiencia: Tipo de audiencia ("ejecutivo", "tecnico", "comercial")
        api_key: API key de OpenAI
        modelo: Modelo a usar (gpt-4, gpt-4-turbo, gpt-3.5-turbo)
        
    Returns:
        Análisis reformulado o None si hay error
    """
    client = get_openai_client(api_key)
    if not client:
        return None
    
    # Prompts por audiencia
    prompts = {
        "ejecutivo": """Resume este análisis de ciberseguridad para un comité ejecutivo (C-Level).
        Enfócate en:
        - Riesgos críticos de negocio
        - Impacto financiero y reputacional
        - Recomendaciones estratégicas de alto nivel
        - Máximo 5 bullets, lenguaje ejecutivo, sin tecnicismos.""",
        
        "tecnico": """Resume este análisis para un equipo técnico (CISO, IT Security).
        Enfócate en:
        - Controles de seguridad específicos
        - Gaps técnicos identificados
        - Recomendaciones de implementación
        - Priorización por riesgo técnico.""",
        
        "comercial": """Reformula este análisis para un equipo de ventas/BDR.
        Enfócate en:
        - Oportunidades de venta específicas
        - Pain points del prospecto
        - Talking points para contacto inicial
        - Urgencia y timing recomendado."""
    }
    
    system_prompt = """Eres un analista de ciberseguridad experto. 
    Reformula el análisis proporcionado SOLO con la información disponible.
    NUNCA inventes datos, métricas o información que no esté en el análisis original.
    Si algo no está disponible, no lo menciones."""
    
    try:
        response = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{prompts.get(audiencia, prompts['ejecutivo'])}\n\nANÁLISIS:\n{analisis}"}
            ],
            temperature=0.3,  # Baja temperatura para ser más factual
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error en OpenAI: {e}")
        return None


def clasificar_urgencia_con_openai(
    analisis: str,
    api_key: Optional[str] = None,
    modelo: str = "gpt-4"
) -> Optional[Dict]:
    """
    Clasifica la urgencia de contacto basándose en el análisis.
    
    Args:
        analisis: Análisis estructural original
        api_key: API key de OpenAI
        modelo: Modelo a usar
        
    Returns:
        Dict con clasificación o None si hay error
    """
    client = get_openai_client(api_key)
    if not client:
        return None
    
    system_prompt = """Eres un analista de ciberseguridad experto.
    Clasifica la urgencia de contacto comercial basándote EXCLUSIVAMENTE en el análisis proporcionado.
    
    Responde en formato JSON con:
    {
        "urgencia": "critica|alta|media|baja",
        "razon": "explicación breve",
        "contactar_en": "timeframe recomendado (ej: 24-48h, esta semana, este mes)",
        "enfoque": "principal ángulo de conversación"
    }"""
    
    try:
        response = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Clasifica este análisis:\n\n{analisis}"}
            ],
            temperature=0.2,
            max_tokens=300,
            response_format={"type": "json_object"}
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        print(f"Error en OpenAI: {e}")
        return None


def generar_email_prospeccion_con_openai(
    analisis: str,
    api_key: Optional[str] = None,
    modelo: str = "gpt-4"
) -> Optional[str]:
    """
    Genera un email de prospección inicial basado en el análisis.
    
    Args:
        analisis: Análisis estructural original
        api_key: API key de OpenAI
        modelo: Modelo a usar
        
    Returns:
        Email de prospección o None si hay error
    """
    client = get_openai_client(api_key)
    if not client:
        return None
    
    system_prompt = """Eres un experto en prospección B2B de ciberseguridad.
    Genera un email de prospección inicial profesional, conciso y personalizado.
    
    Usa SOLO información del análisis proporcionado.
    Estructura:
    - Asunto: impactante, específico
    - Apertura: referencia a hallazgo específico
    - Valor: cómo podemos ayudar
    - CTA: call to action suave
    
    Máximo 150 palabras, tono profesional pero cercano."""
    
    try:
        response = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Genera email de prospección basado en:\n\n{analisis}"}
            ],
            temperature=0.4,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error en OpenAI: {e}")
        return None


def procesar_batch_con_openai(
    resultados: List[Dict],
    accion: str = "reformular_ejecutivo",
    api_key: Optional[str] = None,
    modelo: str = "gpt-4"
) -> List[Dict]:
    """
    Procesa múltiples análisis con OpenAI.
    
    Args:
        resultados: Lista de diccionarios con análisis
        accion: Tipo de procesamiento ("reformular_ejecutivo", "reformular_tecnico", 
                "reformular_comercial", "clasificar", "email")
        api_key: API key de OpenAI
        modelo: Modelo a usar
        
    Returns:
        Lista de resultados con campo adicional "openai_output"
    """
    if not OPENAI_AVAILABLE or not get_openai_client(api_key):
        return resultados
    
    resultados_procesados = []
    
    for idx, r in enumerate(resultados, 1):
        print(f"Procesando {idx}/{len(resultados)}: {r['dominio']}")
        
        output = None
        
        if accion == "reformular_ejecutivo":
            output = reformular_con_openai(r['analisis'], "ejecutivo", api_key, modelo)
        elif accion == "reformular_tecnico":
            output = reformular_con_openai(r['analisis'], "tecnico", api_key, modelo)
        elif accion == "reformular_comercial":
            output = reformular_con_openai(r['analisis'], "comercial", api_key, modelo)
        elif accion == "clasificar":
            output = clasificar_urgencia_con_openai(r['analisis'], api_key, modelo)
        elif accion == "email":
            output = generar_email_prospeccion_con_openai(r['analisis'], api_key, modelo)
        
        resultado_copia = r.copy()
        resultado_copia['openai_output'] = output
        resultado_copia['openai_accion'] = accion
        resultados_procesados.append(resultado_copia)
    
    return resultados_procesados


def generar_analisis_estructural(fila: Dict) -> str:
    """
    Genera el análisis estructural usando exclusivamente
    las columnas existentes en el dataset.
    
    Args:
        fila: Diccionario con los datos de una fila del DataFrame
        
    Returns:
        str: Análisis estructural en formato narrativo
    """
    
    def v(campo):
        """Helper para valores seguros - evita NaN y valores vacíos"""
        valor = fila.get(campo, "")
        if pd.isna(valor) or valor == "" or valor == "N/A":
            return "No disponible"
        return str(valor)
    
    # Formatear valores numéricos
    def format_num(campo):
        """Formatea números con separadores de miles"""
        val = fila.get(campo, "")
        if pd.isna(val) or val == "" or val == "No disponible":
            return "No disponible"
        try:
            return f"{int(val):,}".replace(",", ".")
        except (ValueError, TypeError):
            return str(val)
    
    # Formatear valores monetarios
    def format_budget(campo):
        """Formatea valores de presupuesto en USD"""
        val = fila.get(campo, "")
        if pd.isna(val) or val == "" or val == "No disponible":
            return "No disponible"
        try:
            num = float(val)
            return f"${num:,.0f} USD".replace(",", ".")
        except (ValueError, TypeError):
            return str(val)

    analisis = f"""
ANÁLISIS ESTRUCTURAL AUTOMATIZADO
Generado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. IDENTIFICACIÓN DE LA ORGANIZACIÓN

La empresa {v("empresa")}, asociada al dominio {v("dominio")},
opera en {v("pais")}. Cuenta con {format_num("empleados")} empleados y
un dominio con antigüedad aproximada de {v("dominio_antiguedad")}.

{f'Industria: {v("industria")}' if v("industria") != "No disponible" else ''}
{f'Ingresos anuales: {v("revenue")}' if v("revenue") != "No disponible" else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. POSTURA DECLARADA DEL ENTORNO DIGITAL

- Postura de identidad: {v("postura_identidad")}
- Postura de exposición: {v("postura_exposicion")}
- Postura general: {v("postura_general")}

Estas clasificaciones reflejan el nivel de madurez observado
en los controles evaluados, sin inferir tecnologías específicas.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. SUPERFICIE DE CORREO ELECTRÓNICO

- Proveedor de correo: {v("correo_proveedor")}
- Gateway de seguridad: {v("correo_gateway")}
- Mecanismo de envío: {v("correo_envio")}
- Estado SPF: {v("spf_estado")}
- Estado DMARC: {v("dmarc_estado")}

La información permite evaluar higiene básica de correo
y protección contra suplantación de identidad.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. SUPERFICIE WEB

- HTTPS: {v("https_estado")}
- CDN / WAF: {v("cdn_waf")}
- HSTS: {v("hsts")}
- CSP: {v("csp")}

Estos controles describen el nivel de endurecimiento
mínimo de la superficie web pública.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5. SCORE Y PRIORIDAD

- Score de Seguridad: {v("score")}
- Prioridad: {v("prioridad")}
- Prioridad numérica: {v("prioridad_num")}
- Score de Oportunidad: {v("score_oportunidad")}

Estos valores posicionan a la organización dentro del
conjunto analizado, sin inferir intención de compra.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6. NARRATIVA EXISTENTE

Factores positivos:
{v("factores_positivos")}

Factores negativos:
{v("factores_negativos")}

Talking points:
{v("talking_points")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7. INFORMACIÓN ECONÓMICA

- Budget mínimo: {format_budget("budget_min")}
- Budget máximo: {format_budget("budget_max")}

En ausencia de valores, no es posible inferir
capacidad presupuestal.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONCLUSIÓN

La organización presenta una postura general {v("postura_general")},
con una prioridad {v("prioridad")} y un score de seguridad de {v("score")},
derivados exclusivamente de los datos observables.
"""

    return analisis.strip()


def procesar_csv(path_csv: str, output_path: Optional[str] = None) -> List[Dict]:
    """
    Procesa un CSV completo y genera análisis estructural para cada fila.
    
    Args:
        path_csv: Ruta al archivo CSV de entrada
        output_path: Ruta opcional para guardar resultados en CSV
        
    Returns:
        Lista de diccionarios con empresa, dominio y análisis
    """
    df = pd.read_csv(path_csv)
    
    resultados = []
    
    for idx, fila in df.iterrows():
        analisis = generar_analisis_estructural(fila.to_dict())
        resultados.append({
            "empresa": fila.get("empresa", "N/A"),
            "dominio": fila.get("dominio", "N/A"),
            "analisis": analisis
        })
    
    if output_path:
        salida = pd.DataFrame(resultados)
        salida.to_csv(output_path, index=False, encoding="utf-8-sig")
    
    return resultados


def procesar_dataframe(df: pd.DataFrame) -> List[Dict]:
    """
    Procesa un DataFrame existente y genera análisis para cada fila.
    
    Args:
        df: DataFrame con los datos de ProspectScan
        
    Returns:
        Lista de diccionarios con empresa, dominio y análisis
    """
    resultados = []
    
    for idx, fila in df.iterrows():
        analisis = generar_analisis_estructural(fila.to_dict())
        resultados.append({
            "empresa": fila.get("empresa", "N/A"),
            "dominio": fila.get("dominio", "N/A"),
            "analisis": analisis
        })
    
    return resultados


def exportar_markdown(resultados: List[Dict], output_path: str):
    """
    Exporta los análisis a un archivo Markdown.
    
    Args:
        resultados: Lista de diccionarios con análisis
        output_path: Ruta del archivo .md de salida
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# ProspectScan - Análisis Estructural\n\n")
        f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total de organizaciones analizadas: {len(resultados)}\n\n")
        f.write("---\n\n")
        
        for idx, r in enumerate(resultados, 1):
            f.write(f"## {idx}. {r['empresa']} ({r['dominio']})\n\n")
            f.write("```\n")
            f.write(r['analisis'])
            f.write("\n```\n\n")
            f.write("---\n\n")


def exportar_txt(resultados: List[Dict], output_path: str):
    """
    Exporta los análisis a un archivo de texto plano.
    
    Args:
        resultados: Lista de diccionarios con análisis
        output_path: Ruta del archivo .txt de salida
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("═" * 80 + "\n")
        f.write("PROSPECTSCAN - ANÁLISIS ESTRUCTURAL BATCH\n")
        f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total: {len(resultados)} organizaciones\n")
        f.write("═" * 80 + "\n\n")
        
        for idx, r in enumerate(resultados, 1):
            f.write(f"\n{'═' * 80}\n")
            f.write(f"#{idx} - {r['empresa'].upper()} ({r['dominio']})\n")
            f.write("═" * 80 + "\n\n")
            f.write(r['analisis'])
            f.write("\n\n")


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python analisis_estructural.py <archivo.csv> [salida.csv]")
        sys.exit(1)
    
    path_csv = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"📂 Procesando: {path_csv}")
    resultados = procesar_csv(path_csv, output_path)
    
    print(f"✅ {len(resultados)} análisis generados")
    
    if output_path:
        print(f"💾 Guardado en: {output_path}")
    
    # Mostrar primer ejemplo
    if resultados:
        print("\n" + "═" * 80)
        print("EJEMPLO - PRIMER ANÁLISIS:")
        print("═" * 80)
        print(resultados[0]["analisis"])
