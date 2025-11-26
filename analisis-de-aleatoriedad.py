

""" DONE BY CARLOS GUZMAN NOV 25TH 2025 DISEÑOS EXPERIMENTALES 
Script completo para análisis de datos municipales: ANALISIS DE ALEATORIEDAD
Incluye:
1. Carga de datos desde CSV.
2. Estadísticos descriptivos de la variable Promedio_Escolaridad.
3. Prueba de aleatoriedad (Runs Test).
4. Visualizaciones: histograma y boxplot.
5. Modelo de regresión lineal con interacción (escolaridad × tipo de municipio) para explicar ingreso.
6. Interpretaciones en comentarios.
"""

# =============================
# Importación de librerías
# =============================
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import norm
import statsmodels.formula.api as smf

# =============================
# 1. Carga de datos
# =============================
file_path = "INDICADORES_MUNICIPALES.csv"
df = pd.read_csv(file_path)

# Variables clave
var_escolaridad = "Promedio_Escolaridad (años)"
var_ingreso = "Ingreso_Promedio_Mensual (MXN)"

# =============================
# 2. Estadísticos descriptivos
# =============================
escolaridad = df[var_escolaridad].dropna()
descriptivos = escolaridad.describe()
print("\n=== ESTADÍSTICOS DESCRIPTIVOS ===")
print(descriptivos)
# Comentario: Esto nos da una idea de la distribución general de la escolaridad.

# =============================
# 3. Prueba de aleatoriedad (Runs Test)
# =============================
# Convertimos la serie en secuencia A/B según mediana
mediana = np.median(escolaridad)
secuencia = ["A" if x >= mediana else "B" for x in escolaridad]

# Contar número de runs
runs = 1
for i in range(1, len(secuencia)):
    if secuencia[i] != secuencia[i-1]:
        runs += 1

n1 = secuencia.count("A")
n2 = secuencia.count("B")

# Calcular estadístico Z
esperado = ((2*n1*n2)/(n1+n2)) + 1
varianza = ((2*n1*n2)*(2*n1*n2 - n1 - n2))/(((n1+n2)**2)*(n1+n2-1))
z = (runs - esperado)/np.sqrt(varianza)
p_valor = 2*(1 - norm.cdf(abs(z)))

print("\n=== PRUEBA DE ALEATORIEDAD (Runs Test) ===")
print(f"Número de runs: {runs}")
print(f"Esperado: {esperado:.2f}")
print(f"Z: {z:.3f}")
print(f"p-valor: {p_valor:.4f}")
if p_valor < 0.05:
    print("Conclusión: La secuencia NO es aleatoria (p < 0.05)")
else:
    print("Conclusión: No se rechaza la aleatoriedad (p >= 0.05)")
# Comentario: Si p >= 0.05, podemos asumir independencia en el orden de los datos.

# =============================
# 4. Visualizaciones
# =============================
# Histograma de escolaridad
titulo_hist = "Distribución de Promedio de Escolaridad"
fig_hist = px.histogram(escolaridad, nbins=20,
                        title=titulo_hist,
                        labels={"value":"Años de Escolaridad"})
fig_hist.write_image("histograma_escolaridad.png")

# Boxplot por tipo de municipio
titulo_box = "Promedio de Escolaridad por Tipo de Municipio"
fig_box = px.box(df, x="Tipo_Municipio", y=var_escolaridad,
                 title=titulo_box,
                 labels={"Tipo_Municipio":"Tipo de Municipio", var_escolaridad:"Años de Escolaridad"})
fig_box.write_image("boxplot_escolaridad.png")

# Comentario: El histograma muestra la distribución general; el boxplot evidencia diferencias por tipo de municipio.

# =============================
# 5. Modelo de regresión lineal con interacción
# =============================
formula = f'Q("{var_ingreso}") ~ Q("{var_escolaridad}") * C(Tipo_Municipio)'
modelo = smf.ols(formula=formula, data=df).fit()

print("\n=== MODELO DE REGRESIÓN LINEAL CON INTERACCIÓN ===")
print(modelo.summary())
# Comentario: Revisamos coeficientes y significancia.
# - Si el término de interacción es significativo, el efecto de escolaridad depende del tipo de municipio.

# =============================
# 6. Visualización del modelo
# =============================
pred_df = df.copy()
pred_df['Prediccion'] = modelo.predict(df)
fig_modelo = px.scatter(pred_df, x=var_escolaridad, y=var_ingreso, color="Tipo_Municipio",
                        trendline="ols",
                        title="Relación Escolaridad vs Ingreso por Tipo de Municipio",
                        labels={var_escolaridad:"Años de Escolaridad", var_ingreso:"Ingreso Mensual (MXN)"})
fig_modelo.write_image("modelo_interaccion.png")

# =============================
# Interpretación final (en comentarios)
# =============================
"""
Interpretación:
- La escolaridad no muestra patrón sistemático (p ≈ 0.107), por lo que podemos asumir aleatoriedad.
- El tipo de municipio influye en la escolaridad (urbano > rural).
- El modelo indica que el tipo de municipio sí afecta el ingreso, y la interacción sugiere que el efecto de escolaridad varía según contexto.
- R² bajo: hay otros factores que explican el ingreso.
"""

print("\nScript completado. Se han generado los gráficos y el análisis paso a paso.")
