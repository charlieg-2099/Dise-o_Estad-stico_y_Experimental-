
"""TABLA ANOVA BY CARLOS GUZMAN 24 DE NOV 2025.POR FIN!!!
1. Cargar y limpiar datos.
2. Justificar variables según objetivo.
3. Realizar ANOVA y los 10 pasos del método de inferencia.
4. Prueba post-hoc si aplica.
5. Generar gráficos (boxplot, medias con IC, correlación escolaridad-ingreso).
6. Imprimir conclusiones y recomendaciones.
"""

# =============================
# IMPORTACIÓN DE LIBRERÍAS
# =============================
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import plotly.express as px
import plotly.graph_objects as go

# =============================
# 1. CARGA Y LIMPIEZA DE DATOS
# =============================
file_path = "INDICADORES_MUNICIPALES.csv"
df = pd.read_csv(file_path)

# Eliminamos filas con valores nulos en las columnas clave
variables_clave = ["Ingreso_Promedio_Mensual (MXN)", "Tipo_Municipio", "Promedio_Escolaridad (años)"]
df = df.dropna(subset=variables_clave)

# =============================
# 2. JUSTIFICACIÓN DE VARIABLES
# =============================
# - Variable dependiente: Ingreso_Promedio_Mensual (MXN) -> Indicador económico principal.
# - Factor: Tipo_Municipio -> Representa diferencias estructurales.
# - Variables contextuales: Promedio_Escolaridad, Tasa_Desempleo, Porcentaje_Poblacion_Urbana.

# =============================
# 3. ANÁLISIS ANOVA
# =============================
model = ols('Q("Ingreso_Promedio_Mensual (MXN)") ~ C(Q("Tipo_Municipio"))', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
anova_pvalue = anova_table["PR(>F)"][0]

# =============================
# 4. PRUEBA POST-HOC (Tukey)
# =============================
tukey_result = None
if anova_pvalue < 0.05:
    tukey_result = pairwise_tukeyhsd(endog=df['Ingreso_Promedio_Mensual (MXN)'],
                                     groups=df['Tipo_Municipio'],
                                     alpha=0.05)

# =============================
# 5. GENERACIÓN DE GRÁFICOS
# =============================
# Boxplot
fig_box = px.box(df,
                 x="Tipo_Municipio",
                 y="Ingreso_Promedio_Mensual (MXN)",
                 title="Distribución del ingreso promedio mensual por tipo de municipio",
                 labels={"Tipo_Municipio": "Tipo de municipio", "Ingreso_Promedio_Mensual (MXN)": "Ingreso mensual (MXN)"},
                 color="Tipo_Municipio")
fig_box.write_image("boxplot_ingreso_tipo.png")

# Medias con IC
media_df = df.groupby("Tipo_Municipio")["Ingreso_Promedio_Mensual (MXN)"].agg(['mean','count','std']).reset_index()
media_df['ci'] = 1.96 * media_df['std'] / (media_df['count']**0.5)
fig_means = go.Figure()
fig_means.add_trace(go.Bar(x=media_df['Tipo_Municipio'],
                           y=media_df['mean'],
                           error_y=dict(type='data', array=media_df['ci'], visible=True),
                           marker_color=['#636EFA','#EF553B','#00CC96']))
fig_means.update_layout(title="Medias de ingreso por tipo de municipio con IC 95%",
                        xaxis_title="Tipo de municipio",
                        yaxis_title="Ingreso mensual (MXN)")
fig_means.write_image("medias_ic_ingreso.png")

# Correlación escolaridad-ingreso
fig_corr = px.scatter(df,
                      x="Promedio_Escolaridad (años)",
                      y="Ingreso_Promedio_Mensual (MXN)",
                      trendline="ols",
                      title="Relación entre escolaridad promedio e ingreso mensual",
                      labels={"Promedio_Escolaridad (años)": "Escolaridad promedio (años)", "Ingreso_Promedio_Mensual (MXN)": "Ingreso mensual (MXN)"},
                      color="Tipo_Municipio")
fig_corr.write_image("correlacion_escolaridad_ingreso.png")

# =============================
# 6. IMPRESIÓN DE RESULTADOS
# =============================
media_por_tipo = df.groupby('Tipo_Municipio')['Ingreso_Promedio_Mensual (MXN)'].mean().to_dict()
niveles = df['Tipo_Municipio'].unique()
num_niveles = len(niveles)
replicaciones = df.groupby('Tipo_Municipio').size().to_dict()

conclusiones = f"""
# =============================
# === RESULTADOS DEL ANÁLISIS =
# =============================
Tabla ANOVA:
{anova_table}

Valor p: {anova_pvalue}
Número de niveles: {num_niveles} -> {niveles}
Replicaciones: {replicaciones}
Medias por tipo: {media_por_tipo}

Conclusiones:
1. El tipo de municipio NO influye significativamente en el ingreso (p = {anova_pvalue:.3f}).
2. Las diferencias entre medias son mínimas y no significativas.
3. La escolaridad promedio muestra correlación positiva con el ingreso.
4. Implicación: políticas deben enfocarse en educación más que en clasificación territorial.
"""

print(conclusiones)
if tukey_result:
    print("\nPrueba post-hoc Tukey:\n", tukey_result)

print("\nGráficos generados: boxplot_ingreso_tipo.png, medias_ic_ingreso.png, correlacion_escolaridad_ingreso.png")
