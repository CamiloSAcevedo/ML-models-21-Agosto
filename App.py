#Poner código de python
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification

# Configuración de la página
st.set_page_config(page_title="EDA Deportivo Interactivo", layout="wide")

# Título
st.title("🏋️ Análisis Exploratorio de Datos (EDA) - Deportes")

# Sidebar: Configuración de datos
st.sidebar.header("🎛️ Configura tu Dataset")

# Tamaño del dataset
num_muestras = st.sidebar.slider("Número de muestras", min_value=50, max_value=500, step=10, value=200)

# Columnas disponibles
columnas_disponibles = {
    "Edad": "cuantitativa",
    "Altura": "cuantitativa",
    "Peso": "cuantitativa",
    "Deporte": "cualitativa",
    "Nivel": "cualitativa",
    "Goles": "cuantitativa"
}

opciones_columnas = st.sidebar.multiselect("Selecciona hasta 6 columnas", options=list(columnas_disponibles.keys()), default=list(columnas_disponibles.keys())[:4], max_selections=6)

# Generar datos sintéticos
def generar_datos(n):
    np.random.seed(42)
    deportes = ['Fútbol', 'Básquet', 'Natación', 'Tenis', 'Ciclismo']
    niveles = ['Amateur', 'Intermedio', 'Profesional']

    data = pd.DataFrame({
        "Edad": np.random.randint(15, 40, size=n),
        "Altura": np.round(np.random.normal(1.75, 0.1, size=n), 2),
        "Peso": np.round(np.random.normal(70, 10, size=n), 1),
        "Deporte": np.random.choice(deportes, size=n),
        "Nivel": np.random.choice(niveles, size=n),
        "Goles": np.random.poisson(3, size=n)
    })

    return data

df = generar_datos(num_muestras)

# Mostrar tabla
st.subheader("📋 Vista previa de los datos")
st.dataframe(df[opciones_columnas])

# Visualización de gráficas
st.subheader("📊 Visualización de Datos")

tipo_grafico = st.selectbox("Elige el tipo de gráfico", ["Histograma", "Gráfico de barras", "Gráfico de dispersión", "Gráfico de líneas", "Gráfico de pastel"])

col1 = st.selectbox("Selecciona columna 1", opciones_columnas)
col2 = st.selectbox("Selecciona columna 2 (opcional)", ["Ninguna"] + opciones_columnas)

fig, ax = plt.subplots(figsize=(8,5))

# Lógica para mostrar gráficos
if tipo_grafico == "Histograma":
    sns.histplot(df[col1], kde=True, ax=ax)
    ax.set_title(f"Histograma de {col1}")

elif tipo_grafico == "Gráfico de barras":
    conteo = df[col1].value_counts()
    sns.barplot(x=conteo.index, y=conteo.values, ax=ax)
    ax.set_ylabel("Frecuencia")
    ax.set_title(f"Gráfico de Barras de {col1}")

elif tipo_grafico == "Gráfico de dispersión":
    if col2 != "Ninguna" and columnas_disponibles[col1] == "cuantitativa" and columnas_disponibles[col2] == "cuantitativa":
        sns.scatterplot(data=df, x=col1, y=col2, hue="Deporte", ax=ax)
        ax.set_title(f"Dispersión entre {col1} y {col2}")
    else:
        st.warning("Selecciona dos columnas cuantitativas para dispersión.")

elif tipo_grafico == "Gráfico de líneas":
    if columnas_disponibles[col1] == "cuantitativa":
        df_sorted = df.sort_values(by=col1)
        ax.plot(df_sorted[col1])
        ax.set_title(f"Gráfico de líneas de {col1}")
    else:
        st.warning("El gráfico de líneas requiere una variable cuantitativa.")

elif tipo_grafico == "Gráfico de pastel":
    if columnas_disponibles[col1] == "cualitativa":
        conteo = df[col1].value_counts()
        ax.pie(conteo.values, labels=conteo.index, autopct='%1.1f%%')
        ax.set_title(f"Gráfico de pastel de {col1}")
    else:
        st.warning("El gráfico de pastel solo funciona con variables cualitativas.")

st.pyplot(fig)

# Pie de página
st.markdown("---")
st.markdown("App de análisis interactivo hecha con ❤️ usando Streamlit | Datos sintéticos de deportes")
