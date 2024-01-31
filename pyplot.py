# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 18:44:29 2024

@author: namng
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import imageio


# Datenaufbereitung
df = pd.read_csv(r'capitalbikeshare-complete.csv',  sep=',')
# dftime["Time"] = df["datetime"].dt.strftime("%H")
# .df gibt error, print Datentypen 
# Formatprüfung
print(df.info())
df["datetime"] = pd.to_datetime(df["datetime"], format='%Y-%m-%d %H:%M')

# nun die Stunden, monate und Jahre als zusätzliche Spalten extrahieren
df["hour"] = df["datetime"].dt.hour
df["Month"] = df["datetime"].dt.month
df["Year"] = df["datetime"].dt.year
# Wochentagbennennung
df["workingday"] = df["workingday"].replace({0: "Wochenende", 1: "Wochentag"})
df.to_csv('capitalbikeshare-output.csv')



# 1. Wetterhäufigkeiten
# Einzelne Spalte mit value_counts()
df1 = df["weather_main"]
df1 = df1.value_counts()

# groupby.count
df11 = df.groupby("weather_main")["weather_main"].count()

# Plot mit Achsen
plt.figure()
df11.plot.barh()
plt.title("Wetterhäufigkeit")
plt.ylabel("Wetter")
plt.xlabel("Anzahl aufgenommener Stunden [h]")
plt.savefig(r"images/Wetterhäufigkeit.png", dpi=300)


# 2. Ausleihe nach Wetterbedingungen
df2 = df.groupby("weather_main")["count"].sum()
plt.figure()
df2.plot.barh()
plt.title("Ausleihe nach Wetterbedingungen")
plt.ylabel("Wetter")
plt.xlabel("Anzahl ausgeliehener Fahrräder [Millionen]")
plt.savefig(r"images/Ausleihe nach Wetter.png", dpi=300)

# Durchschnitt pro Stunde
df21 = df.groupby("weather_main")["count"].mean()

plt.figure()
df21.plot.barh()
plt.title("Durchschnittliche Ausleihe nach Wetterbedingungen")
plt.ylabel("Wetter")
plt.xlabel("Anzahl ausgeliehener Fahrräder pro Stunde")
plt.savefig(r"images/Ausleihe nach Wetter pro Stunde.png", dpi=300)


# 3. Ausleihe nach Wochentagen 

pivot3 = df.pivot_table(
    index="weather_main",
    columns="workingday",
    values="count",
    aggfunc="mean",
    )

df3wk = df.groupby("workingday")["count"].sum()

plt.figure()
df3wk.plot.bar()
plt.title("Ausleihe nach Wochentag")
plt.xlabel("Wochentag")
plt.ylabel("Anzahl ausgeliehener Fahrräder [Millionen]")
plt.savefig(r"images/Ausleihe nach Wochentag.png", dpi=300)

plt.figure()
pivot3.plot.barh()
plt.title("Durchschnittliche Ausleihe nach Wochentag und Wetter")
plt.ylabel("Wetter")
plt.xlabel("Anzahl ausgeliehener Fahrräder pro Stunde")
plt.savefig(r"images/Ausleihe nach Wochentag.png", dpi=300)


# 4. Zusammenhang zwischen Windgeschwindigkeit und Ausleihe

# nach Windgeschwindigkeit gruppieren und die durchschnitlliche Ausleihquote errechnen
df4 = df.groupby("wind_speed")["count"].mean()

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


# 5. Ausleihe nach Uhrzeit und Monat
df5 = df
# Ausleihe des ersten Monats

# Balkendiagramm für einen Monat
df5first = df5[(df5["datetime"].dt.year==2018) & (df5["datetime"].dt.month==1)]

# durchschnitlliche Ausleihe pro Stunde
df5hourmean = df5first.groupby("hour")["count"].mean()


plt.figure()
df5hourmean.plot.bar()
plt.xlabel("Uhrzeit in Std")
plt.ylabel("Anzahl der Ausleihen")
plt.title("Fahrradausleihe 2018-01", loc='left')

# Balkendiagramm
plt.figure()
sns.barplot(
     data=df5first,
     x="hour",
     y="count",
     estimator="mean",
     #native_scale=True
     )
plt.xlabel("Uhrzeit in Std")
plt.ylabel("Anzahl der Ausleihen")
plt.title("Fahrradausleihe 2018-01", loc='left')

# Diagrammgeneration
# alle Monate
for yeari in range(2018, 2022, 1):
    for monthi in range(1, 13, 1):
        print(str(yeari) + "-" + str(monthi), end=", ")
        df5i = df5[(df5["datetime"].dt.year==yeari) & (df5["datetime"].dt.month==monthi)]

        plt.figure()
        plt.axis([0, 23, 0, 1500])
        plt.title("Fahrradausleihe " + str(yeari) + "-" + str(monthi), loc='left')
        # es gibt leere monate, welche einen error geben
        try:
            sns.barplot(
                  data=df5i,
                  x="hour",
                  y="count",
                  estimator="mean"
                  )   
        #     df5mean.plot.hist(bins=24)
        except ValueError:
            pass
        
        plt.xlabel("Uhrzeit in Std")
        plt.ylabel("Durchschnittliche Anzahl der Ausleihen am Tag")
        plt.savefig(r"images/monate/test" + str(yeari) + "-" + str(monthi) + ".png", dpi=90)
        plt.close()


# Animation
images = []
for yeari in range(2018, 2022, 1):
    for monthi in range(1, 13, 1):
        bild = imageio.imread(r"images/monate/test" + str(yeari) + "-" + str(monthi) + ".png")
        images.append(bild)

imageio.mimsave(r"images/animation.gif", images, fps=5)