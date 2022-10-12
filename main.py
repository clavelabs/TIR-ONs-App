import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Leer precios ON
Data_ON = pd.read_pickle("parsed_data")

# Figura
tamaños = list(
    Data_ON.select_dtypes(
        include=["int16", "int32", "int64", "float16", "float32", "float64"]
    ).columns
)
tamaños.insert(0, None)
tamaños.remove("TIR")  # TIR negativas no permiten usarlas para asignar tamaños

colores = list(Data_ON.columns)
colores.insert(0, None)
colores.remove("Vencimiento")  #


def main_plot(color, size, text, data):
    fig = px.scatter(
        data,
        x="MD",
        y="TIR",  # ,
        size=size,
        color=color,
        size_max=60,
        text=text,
        log_x=False,  # size_max=60,
        trendline="ols",
        trendline_options=dict(
            log_x=True
        ),  #'lowess', 'rolling', 'ewm', 'expanding', 'ols'
        template="plotly_dark",
    )

    fig.update_traces(textposition="top center")
    return fig


## Dashboard

# config y titulo
st.set_page_config(
    page_title="Curva de obligaciones negociables", page_icon="✅", layout="wide",
)

st.image("banner.jpeg")
url = "https://twitter.com/ezemorzan"
url2 = "https://twitter.com/dammishere"
st.markdown("Ezequiel Morzan [@EzeMorzan](%s)" % url)
st.markdown("Damian Piuselli [@DammIsHere](%s)" % url2)
st.title("Curva de obligaciones negociables")

## curva de ons

# filtros
col1, col2, col3 = st.columns(3)
with col1:
    color_filter = st.selectbox("Colores:", colores)
with col2:
    size_filter = st.selectbox("Tamaño:", tamaños)
with col3:
    text_filter = st.radio("Texto:", ("Ticker", "Empresa"), horizontal=True)


# plot
if text_filter == "Ticker":
    text = Data_ON["ticker_dolares"]
if text_filter == "Empresa":
    text = Data_ON["Empresa"]

fig = main_plot(color=color_filter, size=size_filter, text=text, data=Data_ON,)
st.plotly_chart(fig, use_container_width=True)

# Dataframe
st.markdown("### Datos:")
st.dataframe(Data_ON)
