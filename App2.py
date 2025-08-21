import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de página
st.set_page_config(page_title="EDA Interactivo - Tu CSV", layout="wide")
st.title("🔍 Análisis Exploratorio Interactivo (tu CSV)")

# Subida del archivo
st.sidebar.header("Carga tu archivo CSV")
uploaded_file = st.sidebar.file_uploader("Selecciona un archivo CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Datos cargados (vista previa)")
    st.dataframe(df.head())

    # Sidebar: Selección de columnas
    todas_columnas = list(df.columns)
    seleccion_cols = st.sidebar.multiselect(
        "Selecciona hasta 6 columnas", todas_columnas, default=todas_columnas[:4]
    )

    # Filtro de filas
    max_rows = st.sidebar.slider("Número máximo de filas a mostrar", 10, min(500, df.shape[0]), value=100, step=10)

    df_sel = df[seleccion_cols].head(max_rows)

    st.subheader("Datos seleccionados")
    st.dataframe(df_sel)

    # Tipos de variables
    tipos = {}
    st.sidebar.markdown("### Define tipo de variable:")
    for col in seleccion_cols:
        tip = st.sidebar.selectbox(f"Tipo de '{col}'", ("Cuantitativa", "Cualitativa", "Mixta"), index=0)
        tipos[col] = tip

    # Selección del tipo de gráfico
    st.subheader("Visualización de gráficas")
    grafico_tipo = st.selectbox("Elige tipo de gráfico", ["Histograma", "Barras", "Dispersión", "Línea", "Pastel"])

    col1 = st.selectbox("Columna 1", seleccion_cols)
    col2 = st.selectbox("Columna 2 (opcional)", ["-- Ninguna --"] + seleccion_cols)

    fig, ax = plt.subplots(figsize=(8, 5))

    try:
        if grafico_tipo == "Histograma":
            if tipos[col1] == "Cuantitativa":
                sns.histplot(df_sel[col1].dropna().astype(float), kde=True, ax=ax)
                ax.set_title(f"Histograma de {col1}")
            else:
                st.warning("El histograma requiere datos cuantitativos.")

        elif grafico_tipo == "Barras":
            counts = df_sel[col1].value_counts(dropna=True)
            sns.barplot(x=counts.index.astype(str), y=counts.values, ax=ax)
            ax.set_title(f"Gráfico de barras de {col1}")
            ax.set_ylabel("Frecuencia")
            plt.xticks(rotation=45)

        elif grafico_tipo == "Dispersión":
            if col2 != "-- Ninguna --" and tipos[col1] == "Cuantitativa" and tipos[col2] == "Cuantitativa":
                sns.scatterplot(data=df_sel, x=col1, y=col2, ax=ax)
                ax.set_title(f"Dispersión entre {col1} y {col2}")
            else:
                st.warning("Selecciona dos columnas cuantitativas para dispersión.")

        elif grafico_tipo == "Línea":
            if tipos[col1] == "Cuantitativa":
                serie = df_sel[col1].dropna().astype(float)
                serie = serie.reset_index(drop=True)
                ax.plot(serie)
                ax.set_title(f"Serie de {col1}")
            else:
                st.warning("El gráfico de líneas requiere datos cuantitativos.")

        elif grafico_tipo == "Pastel":
            if tipos[col1] == "Cualitativa":
                counts = df_sel[col1].value_counts(dropna=True)
                ax.pie(counts.values, labels=counts.index.astype(str), autopct='%1.1f%%')
                ax.set_title(f"Pastel de {col1}")
            else:
                st.warning("El gráfico de pastel requiere variable cualitativa.")

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error al generar gráfico: {e}")

else:
    st.info("Sube un archivo CSV para empezar el análisis.")
