

"""
CARLOS ALBERTO GUZMAN MONTES NOV 25th 2025
Script Análisis de bondad de ajuste de una distribución normal
Incluye:
1. Carga de datos desde CSV.
2. Selección de variable relevante.
3. Prueba de normalidad (Shapiro-Wilk).
4. Cálculo de asimetría y curtosis.
5. Visualizaciones: histograma con curva normal y QQ plot.
6. Interpretación en comentarios.
"""

# =============================
# Importación de librerías
# =============================
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import shapiro, skew, kurtosis
import statsmodels.graphics.gofplots as gofplots

# =============================
# 1. Carga de datos
# =============================
file_path = "INDICADORES_MUNICIPALES.csv"
df = pd.read_csv(file_path)

# =============================
# 2. Selección de variable
# =============================
variable = "Promedio_Escolaridad (años)"
data = df[variable].dropna()

# =============================
# 3. Prueba de normalidad (Shapiro-Wilk)
# =============================
stat, p_value = shapiro(data)
print("\n=== PRUEBA DE NORMALIDAD (Shapiro-Wilk) ===")
print(f"Estadístico: {stat:.4f}, p-valor: {p_value:.4f}")
if p_value < 0.05:
    print("Conclusión: Los datos NO se ajustan a una distribución normal (p < 0.05)")
else:
    print("Conclusión: No se rechaza la normalidad (p >= 0.05)")

# =============================
# 4. Medidas de distribución
# =============================
asimetria = skew(data)
curtosis_val = kurtosis(data)
print("\n=== MEDIDAS DE DISTRIBUCIÓN ===")
print(f"Asimetría: {asimetria:.4f}")
print(f"Curtosis: {curtosis_val:.4f}")
# Comentario: Asimetría cercana a 0 indica simetría; curtosis negativa indica colas más ligeras.

# =============================
# 5. Visualizaciones
# =============================
# Histograma con curva normal
fig_hist = px.histogram(data, nbins=20, marginal="box",
                        title="Histograma de Escolaridad con Curva Normal",
                        labels={"value": "Años de Escolaridad"})
fig_hist.write_image("histograma_normalidad.png")

# QQ Plot
qq_fig = gofplots.qqplot(data, line='s')
qq_fig.savefig("qqplot_escolaridad.png")

# =============================
# Interpretación final (en comentarios)
# =============================
"""
Interpretación:
- La prueba Shapiro-Wilk indica que los datos NO son normales (p < 0.05).
- Asimetría ≈ 0 (0.03): distribución casi simétrica.
- Curtosis negativa (-1.26): distribución más plana que la normal, colas ligeras.
Impacto en la hipótesis:
- No podemos asumir normalidad estricta para modelos paramétricos.
- Sin embargo, la baja asimetría permite usar métodos robustos o transformaciones.
"""

print("\nGráficos generados: histograma_normalidad.png y qqplot_escolaridad.png")
print("Script completado. Análisis documentado paso a paso.")
