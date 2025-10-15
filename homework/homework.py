
# %%
# Cargue los datos de las tabla "files/input/drivers.csv" a una variable llamada
# drivers, usando pandas 
import pandas as pd
import os
import matplotlib.pyplot as plt

# Crear las carpetas de salida si no existen
os.makedirs("../files/output", exist_ok=True)
os.makedirs("../files/plots", exist_ok=True)

drivers = pd.read_csv("../files/input/drivers.csv")


# %%
# Cargue los datos de las tabla "files/input/timesheet.csv" a una variable llamada
# timesheet, usando pandas
timesheet = pd.read_csv("../files/input/timesheet.csv")

# %%
# Calcule el promedio de las columnas "hours-logged" y "miles-logged" en la 
# tabla "timesheet", agrupando los resultados por cada conductor (driverId).
avg_timesheet = timesheet.groupby("driverId")[["hours-logged", "miles-logged"]].mean().reset_index()
avg_timesheet

# %%
# Cree una tabla llamada "timesheet_with_means" basada en la tabla "timesheet", 
# agregando una columna con el promedio de "hours-logged" para cada conductor (driverId).
timesheet_with_means = timesheet.merge(avg_timesheet[["driverId", "hours-logged"]], on="driverId", suffixes=("", "_mean"))

# %%
# Cree una tabla llamada "timesheet_below" a partir de "timesheet_with_means", filtrando los registros 
# donde "hours-logged" sea menor que "mean_hours-logged".
timesheet_below = timesheet_with_means[timesheet_with_means["hours-logged"] < timesheet_with_means["hours-logged_mean"]]
timesheet_below

# %%
## Cree una tabla llamada "summary" que contenga el total de horas y millas
# registradas en "timesheet_below", agrupando los resultados por cada conductor (driverId).
summary = timesheet_below.groupby("driverId")[["hours-logged", "miles-logged"]].sum().reset_index()
summary

# %%
# Cree una tabla llamada "summary_with_names" basada en la tabla "summary",
# agregando la columna "name" de la tabla "drivers".
summary_with_names = summary.merge(drivers[["driverId", "name"]], on="driverId", how="left")
summary_with_names

# %%
# Guarde la tabla "summary_with_names" en un archivo CSV llamado "files/output/summary.csv",
# sin incluir el índice.
summary_with_names.to_csv("../files/output/summary.csv", index=False)

# %%
# Cree un gráfico de barras que muestre las 10 conductoras (drivers)
import matplotlib.pyplot as plt
top10_drivers = summary_with_names.nlargest(10, "miles-logged")
plt.figure(figsize=(10, 6))
plt.bar(top10_drivers["name"], top10_drivers["miles-logged"], color='skyblue')
plt.xlabel("Driver Name")
plt.ylabel("Miles Logged")
plt.title("Top 10 Drivers by Miles Logged")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("../files/plots/top10_drivers.png")
plt.show()
