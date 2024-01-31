# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 19:06:49 2024

@author: namng
"""

import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


# Datenaufbereitung
df = pd.read_csv(r'capitalbikeshare-output.csv',  sep=',')
# dftime["Time"] = df["datetime"].dt.strftime("%H")
# .df gibt error, print Datentypen 
# Formatprüfung
print(df.info())
df["datetime"] = pd.to_datetime(df["datetime"], format='%Y-%m-%d %H:%M')

# Überschrift und Tabs
st.write("# Capital Bike Share")

show_tables = st.toggle("Datentabellen anzeigen")
tab1, tab2 = st.tabs(["Jährliche Datentabeellen", "Gesamte Datentabellen"])


with tab1:
    
    st.write("Wähle ein Jahr aus, um dessen Daten anzuzeigen:")
    year = st.multiselect("year", options=[2018, 2019, 2020, 2021], default=[2018, 2019, 2020, 2021])

    # 1. Wetterhäufigkeiten
    
    st.write("# 1. Wetterhäufigkeiten")
    
    df1 = df[df["Year"].isin(year)]
    st.bar_chart(
                 data=df1,
                 y="count",
                 x="weather_main",
                 width=0, height=500,
                 use_container_width=True
                 )
    if show_tables:
        df1 = df1.groupby("weather_main")["weather_main"].count()
        st.write(df1)
    
    # 2. Ausleihe nach Wetterbedingungen
    
    st.write("# 2. Ausleihe nach Wetterbedingungen")
    
    df2 = df[df["Year"].isin(year)]
    df2 = df2.groupby("weather_main")["count"].sum()
    
    st.bar_chart(
                 data=df2,
                 y="count",
                 width=0, height=500,
                 use_container_width=True
                 )
    if show_tables:
        st.write(df2)
        
    # Durchschnitt pro Stunde
    st.write("## Durchschnittliche Ausleihen pro Stunde nach Wetter")
    
    df21 = df[df["Year"].isin(year)]
    df21 = df21.groupby("weather_main")["count"].mean()
    
    # Streamlit
    st.bar_chart(
                 data=df21,
                 y="count",
                 width=0, height=500,
                 use_container_width=True
                 )
    if show_tables:
        st.write(df21)
    
    
    # 3. Ausleihe nach Wochentagen
    
    st.write("# 3. Ausleihe nach Wochentagen")
    
    df3 = df[df["Year"].isin(year)]
    pivot3 = df3.pivot_table(
        index="weather_main",
        columns="workingday",
        values="count",
        aggfunc="mean",
        )
    df3 = df3.groupby("workingday")["count"].sum()
    
    
    
    # Streamlit
    st.bar_chart(
                 data=df3,
                 y="count",
                 width=0, height=500,
                 use_container_width=True
                 )
    
    st.write("Aufgeteilt nach Wetter pro Stunde")
    
    # Streamlit
    st.bar_chart(
                 data=pivot3,
                 width=0, height=500,
                 use_container_width=True
                 )
    if show_tables:
        st.write(pivot3)

with tab2:
    # 4. Zusammenhang zwischen Windgeschwindigkeit und Ausleihe
    
    st.write("# 4. Zusammenhang zwischen Windgeschwindigkeit und Ausleihe")
    # nach Windgeschwindigkeit gruppieren und die durchschnitlliche Ausleihquote errechnen
    
    st.write("Folgende Daten gelten für den **gesamten** Zeitraum.")
    df4 = df.groupby("wind_speed")["count"].mean()
    if show_tables:
        st.write(df4)
    
    # Histogramm
    fig = plt.figure()
    hist = sns.histplot(
         data=df,
         x="wind_speed",
         binwidth=0.5,
         kde=True
         )
    plt.xlabel("Windgeschwindigkeit")
    plt.ylabel("Anzahl der Ausleihen")
    plt.xlim(0, 17.5)
    plt.title("Fahrradausleihe nach Windgeschwindigkeit", loc='left')
    
    # Streamlit
    st.pyplot(fig)
    
    
    # 5. Ausleihe nach Uhrzeit und Monat
    
    st.write("# 5. Monatliche Ausleihe nach Uhrzeit")
    
    df5 = df
    
    # Streamlit Auswahl
    styear = st.slider("Select year", 2018, 2021)
    stmonth = st.slider("Select month", 1, 12)
    
    df5stvalue = df5[(df5["datetime"].dt.year==styear) & (df5["datetime"].dt.month==stmonth)]
    st.bar_chart(
                 data=df5stvalue,
                 x="hour",
                 y="count",
                 width=0, height=500,
                 use_container_width=True
                 )

