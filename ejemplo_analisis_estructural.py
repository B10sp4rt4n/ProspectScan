#!/usr/bin/env python3
"""
ProspectScan - Ejemplo de uso del módulo de Análisis Estructural

Este script demuestra cómo usar el módulo analisis_estructural.py
para generar reportes narrativos de forma batch.

Uso:
    python ejemplo_analisis_estructural.py <archivo.csv>
    python ejemplo_analisis_estructural.py prospectscan_cruce_20260106.csv
"""

import sys
from analisis_estructural import (
    procesar_csv,
    procesar_dataframe,
    exportar_markdown,
    exportar_txt,
    generar_analisis_estructural
)
import pandas as pd


def main():
    if len(sys.argv) < 2:
        print("❌ Error: Falta el archivo CSV")
        print("\nUso:")
        print("  python ejemplo_analisis_estructural.py <archivo.csv>")
        print("\nEjemplo:")
        print("  python ejemplo_analisis_estructural.py prospectscan_cruce_20260106.csv")
        sys.exit(1)
    
    path_csv = sys.argv[1]
    
    print("=" * 80)
    print("PROSPECTSCAN - GENERADOR DE ANÁLISIS ESTRUCTURAL")
    print("=" * 80)
    print(f"\n📂 Procesando: {path_csv}\n")
    
    # ========================================================================
    # OPCIÓN 1: Procesar CSV directamente
    # ========================================================================
    print("🔄 Generando análisis...")
    resultados = procesar_csv(path_csv)
    print(f"✅ {len(resultados)} análisis generados\n")
    
    # ========================================================================
    # OPCIÓN 2: Exportar a diferentes formatos
    # ========================================================================
    
    # TXT
    output_txt = f"analisis_estructural_batch.txt"
    exportar_txt(resultados, output_txt)
    print(f"💾 Exportado TXT: {output_txt}")
    
    # Markdown
    output_md = f"analisis_estructural_batch.md"
    exportar_markdown(resultados, output_md)
    print(f"💾 Exportado Markdown: {output_md}")
    
    # CSV con análisis embebido
    output_csv = f"analisis_estructural_batch.csv"
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"💾 Exportado CSV: {output_csv}")
    
    # ========================================================================
    # VISTA PREVIA - PRIMER ANÁLISIS
    # ========================================================================
    print("\n" + "=" * 80)
    print("📋 VISTA PREVIA - PRIMER ANÁLISIS")
    print("=" * 80)
    print(f"\nEmpresa: {resultados[0]['empresa']}")
    print(f"Dominio: {resultados[0]['dominio']}\n")
    print(resultados[0]['analisis'])
    
    # ========================================================================
    # INTEGRACIÓN CON OPENAI (EJEMPLO)
    # ========================================================================
    print("\n" + "=" * 80)
    print("🤖 INTEGRACIÓN CON OPENAI/CHATGPT (EJEMPLO)")
    print("=" * 80)
    print("""
Este análisis puede ser enviado a OpenAI/ChatGPT para:

1. Reformular para diferentes audiencias:
   - C-Level (ejecutivo)
   - Técnico (CISO, IT)
   - Comercial (Sales, BDR)

2. Resumir o expandir el contenido

3. Auditar consistencia

4. Generar recomendaciones accionables

Ejemplo de prompt para ChatGPT:

    \"\"\"
    Eres un analista de ciberseguridad. A continuación recibirás
    un análisis estructural de una organización basado exclusivamente
    en datos observables de su superficie digital.
    
    Resume este análisis para un comité ejecutivo (C-Level),
    destacando únicamente los riesgos críticos y oportunidades
    de mejora, sin inventar información adicional.
    
    ANÁLISIS:
    {resultados[0]['analisis']}
    \"\"\"

Para integración programática con OpenAI:

    import openai
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Eres un analista de ciberseguridad. "
                          "Reformula análisis técnicos para diferentes audiencias."
            },
            {
                "role": "user",
                "content": f"Resume para C-Level:\\n{resultados[0]['analisis']}"
            }
        ]
    )
    
    print(response.choices[0].message.content)
""")
    
    print("\n" + "=" * 80)
    print("✅ PROCESO COMPLETADO")
    print("=" * 80)
    print(f"""
Archivos generados:
- {output_txt}
- {output_md}
- {output_csv}

Siguiente paso sugerido:
- Revisar los análisis generados
- Integrar con OpenAI/ChatGPT si es necesario
- Distribuir a stakeholders correspondientes
""")


if __name__ == "__main__":
    main()
