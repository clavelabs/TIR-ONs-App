import pandas as pd
import numpy as np
from funciones_financieras import tir, duration


url = "https://iol.invertironline.com/mercado/cotizaciones/argentina/obligaciones%20negociables"
ON = pd.read_html(url)[0]

# formateo de datos > precios_ON
precios_ON = pd.DataFrame()
precios_ON["ÚltimoOperado"] = (
    ON["ÚltimoOperado"]
    .str.replace(".", "", regex=True)
    .str.replace(",", ".", regex=True)
    .astype(float)
)
precios_ON["MontoOperado"] = (
    ON["MontoOperado"]
    .str.replace(".", "", regex=True)
    .str.replace(",", ".", regex=True)
    .astype(float)
)
precios_ON["Ticker"] = ON["Símbolo"]
precios_ON = precios_ON[["Ticker", "ÚltimoOperado", "MontoOperado"]]
precios_ON.set_index("Ticker", inplace=True)

# parsear cashflows_ON.xlsx
Data_ON = tickers = pd.read_excel("cashflows_ON.xlsx", sheet_name="Data_ON")
comunes = list(set(precios_ON.index) & set(Data_ON["ticker_dolares"]))
comunes.sort()
Data_ON = Data_ON.loc[Data_ON["ticker_dolares"].isin(comunes)].sort_values(
    by=["ticker_dolares"]
)
Data_ON["Precio_dolares"] = list(precios_ON.loc[comunes]["ÚltimoOperado"] / 100)
Data_ON["Precio_pesos"] = list(precios_ON.loc[Data_ON["ticker_pesos"]]["ÚltimoOperado"])
Data_ON["Volumen"] = list(precios_ON.loc[Data_ON["ticker_pesos"]]["MontoOperado"])
Data_ON["Amortizacion"] = Data_ON["Amortizacion"].replace(
    np.nan, "No Bullet", regex=True
)
Data_ON.set_index(["ticker_pesos"], inplace=True)
Data_ON["inversion_minima"] = Data_ON["Precio_dolares"] * Data_ON["lamina_minima"] / 100

cashflows = {}
for i in Data_ON.index:
    CF = pd.read_excel("cashflows_ON.xlsx", sheet_name=i)
    cashflows[i] = CF

TIR = {}
for j in Data_ON.index:
    tir_j = tir(cashflows[j], Data_ON.loc[j, "Precio_dolares"], plazo=1)
    TIR[j] = (
        round(
            (
                duration(cashflows[j], Data_ON.loc[j, "Precio_dolares"], plazo=1)
                / (1 + tir_j / 100)
            ),
            2,
        ),
        tir_j,
    )

TIR = pd.DataFrame.from_dict(TIR, orient="index")
TIR.columns = ["MD", "TIR"]

Data_ON["MD"] = TIR["MD"]
Data_ON["TIR"] = TIR["TIR"]

Data_ON.to_pickle("parsed_data")
