
"""
Inferencia de desviaciones: Comparación de varianzas entre tipos de municipio
Incluye:
- Estadísticos descriptivos
- Prueba F por pares
- Análisis de normalidad, asimetría y curtosis
- Gráficos: histograma, QQ plot, boxplot
"""

import pandas as pd
import numpy as np
from scipy.stats import shapiro, skew, kurtosis, f_oneway
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
df = pd.read_csv("INDICADORES_MUNICIPALES.csv")
var_ingreso = "Ingreso_Promedio_Mensual (MXN)"
var_tipo = "Tipo_Municipio"

# Grupos
grupos = df.groupby(var_tipo)[var_ingreso]
rural = grupos.get_group("Rural-C")
semi = grupos.get_group("Semiurbano-B")
urbano = grupos.get_group("Urbano-A")

# Estadísticos descriptivos
print("\n=== ESTADÍSTICOS DESCRIPTIVOS ===")
for nombre, datos in [("Rural-C", rural), ("Semiurbano-B", semi), ("Urbano-A", urbano)]:
    print(f"{nombre}: n={len(datos)}, media={np.mean(datos):.2f}, varianza={np.var(datos, ddof=1):.2f}, desv={np.std(datos, ddof=1):.2f}")

# Normalidad
stat, p = shapiro(df[var_ingreso])
print(f"\nPrueba Shapiro-Wilk (Ingreso): Estadístico={stat:.4f}, p-valor={p:.4f}")
print(f"Asimetría={skew(df[var_ingreso]):.4f}, Curtosis={kurtosis(df[var_ingreso]):.4f}")

# Prueba F por pares
def prueba_f(var1, var2):
    F = np.var(var1, ddof=1) / np.var(var2, ddof=1)
    return F

print("\n=== PRUEBA F POR PARES ===")
print(f"Rural vs Semi: F={prueba_f(rural, semi):.3f}")
print(f"Rural vs Urbano: F={prueba_f(rural, urbano):.3f}")
print(f"Semi vs Urbano: F={prueba_f(semi, urbano):.3f}")

# Gráficos
plt.figure(figsize=(8,5))
sns.histplot(df[var_ingreso], bins=20, kde=True)
plt.title("Histograma del Ingreso")
plt.savefig("histograma_ingreso.png")

plt.figure(figsize=(8,5))
sns.boxplot(x=var_tipo, y=var_ingreso, data=df)
plt.title("Boxplot Ingreso por Tipo de Municipio")
plt.savefig("boxplot_ingreso.png")

# QQ plot
import statsmodels.api as sm
sm.qqplot(df[var_ingreso], line='s')
plt.title("QQ Plot Ingreso")
plt.savefig("qqplot_ingreso.png")

print("\nAnálisis completado. Gráficos guardados.")
