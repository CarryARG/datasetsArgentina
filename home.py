import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Cargar los datasets para analizar los KPIs
file_path_serie = './datasets/cebada-cervecera-serie-1938-1973.csv'
file_path_anual = './datasets/cebada-cervecera-anual-1938-1973.csv'

# Volver a intentar leer los archivos con una codificación diferente (ISO-8859-1)
df_serie = pd.read_csv(file_path_serie, encoding='ISO-8859-1')
df_anual = pd.read_csv(file_path_anual, encoding='ISO-8859-1')


# Removing duplicates in both datasets
df_serie_dedup = df_serie.drop_duplicates()
df_anual_dedup = df_anual.drop_duplicates()

# Checking for missing values in the deduplicated datasets
missing_values_serie = df_serie_dedup.isnull().sum()
missing_values_anual = df_anual_dedup.isnull().sum()

# Number of records before and after deduplication
duplicates_serie = len(df_serie) - len(df_serie_dedup)
duplicates_anual = len(df_anual) - len(df_anual_dedup)

duplicates_serie, duplicates_anual, missing_values_serie, missing_values_anual

# df_anual_dedup

# Calcula el crecimiento anual de la producción
df_anual_dedup['crecimiento_anual'] = df_anual_dedup['produccion_cebada_cervecera_tm'].pct_change() * 100

# Calcula la media del crecimiento anual de los últimos 10 años
crecimiento_promedio = df_anual_dedup['crecimiento_anual'].tail(10).mean()

# Estima el crecimiento para el próximo año
produccion_actual = df_anual_dedup['produccion_cebada_cervecera_tm'].iloc[-1]
estimacion_crecimiento = produccion_actual * (1 + crecimiento_promedio / 100)

# Calcula la tasa de cosecha
df_anual_dedup['tasa_cosecha'] = df_anual_dedup['superficie_cosechada_cebada_cervecera_ha'] / df_anual_dedup['superficie_sembrada_cebada_cervecera_ha']

# Calcula la media de la tasa de cosecha de los últimos 5 años
tasa_cosecha_promedio = df_anual_dedup['tasa_cosecha'].tail(10).mean()

# Ajuste por un porcentaje de incremento (por ejemplo, 2%)
ajuste_porcentaje_tasa_cosecha = 0.02
tasa_cosecha_estimada = tasa_cosecha_promedio * (1 + ajuste_porcentaje_tasa_cosecha)

superficie_sembrada_actual = df_anual_dedup['superficie_sembrada_cebada_cervecera_ha'].iloc[-1]
superficie_cosechada_estimada = superficie_sembrada_actual * tasa_cosecha_estimada

# Calcula el rendimiento promedio de los últimos 5 años
rendimiento_promedio = df_anual_dedup['rendimiento_cebada_cervecera_kgxha'].tail(10).mean()

# Ajuste por un porcentaje de incremento (por ejemplo, 3%)
ajuste_porcentaje_rendimiento = 0.03
rendimiento_estimado = rendimiento_promedio * (1 + ajuste_porcentaje_rendimiento)

st.subheader("KPIs Estimados para el Próximo Año")

st.write(f"**Estimación de Crecimiento Anual:** {crecimiento_promedio:.2f}%")
st.write(f"**Estimación de Producción:** {estimacion_crecimiento:.2f} tm")

st.write(f"**Estimación de Tasa de Cosecha:** {tasa_cosecha_estimada:.2f}")
st.write(f"**Estimación de Superficie Cosechada:** {superficie_cosechada_estimada:.2f} ha")

st.write(f"**Estimación de Rendimiento:** {rendimiento_estimado:.2f} kg/ha")

# Gráficos
st.subheader("Gráficos de Tendencias")
fig, ax = plt.subplots()
ax.plot(df_anual_dedup['indice_tiempo'], df_anual_dedup['produccion_cebada_cervecera_tm'])
ax.plot(df_anual_dedup['indice_tiempo'].iloc[-1] + 1, estimacion_crecimiento, marker='o', markersize=10, color='red')
st.pyplot(fig)

fig, ax = plt.subplots()
ax.plot(df_anual_dedup['indice_tiempo'], df_anual_dedup['tasa_cosecha'])
ax.plot(df_anual_dedup['indice_tiempo'].iloc[-1] + 1, tasa_cosecha_estimada, marker='o', markersize=10, color='red')
st.pyplot(fig)

fig, ax = plt.subplots()
ax.plot(df_anual_dedup['indice_tiempo'], df_anual_dedup['rendimiento_cebada_cervecera_kgxha'])
ax.plot(df_anual_dedup['indice_tiempo'].iloc[-1] + 1, rendimiento_estimado, marker='o', markersize=10, color='red')
st.pyplot(fig)