import pandas as pd

from src.simple_random_sampling import simple_random_sample
from src.estimadores import estimate_total, estimate_ratio

#Carga de los datos procesados

votos = pd.read_csv("data/processed/votos_cdmx_limpio.csv")

#Poblacion de estudio

population = votos.loc[votos["MUNICIPIO"] != "VOTO_EXTRANJERO"].copy()

#seleccionamos muestra
N = len(population)
n = 100

sample = simple_random_sample(population, n, 31299)

#Estimador al total de votos
total_brugada = estimate_total(sample=sample, variable= "TOTAL_BRUGADA", N=N)

#EStimacion de la proporcion de votos
ratio_brugada = estimate_ratio(sample=sample, numerator = "TOTAL_BRUGADA",denominator="TOTAL_VOTOS", N=N)
#Verificacion de los datos
#Datos poblacionales
true_total = population["TOTAL_BRUGADA"].sum()
true_ratio = population["TOTAL_BRUGADA"].sum() / population["TOTAL_VOTOS"].sum()

print(f"Tamaño poblacional: {N}")
print(f"Tamaño de muestra: {n}")
print("\n =====Total de votos=====")
print(f"Total poblacional: {true_total:,.0f}")
print(f"Tamaño estimado:{total_brugada['estimate']:,.0f}")
print(f"Error estandar: {total_brugada['standard_error']:,.2f}")
print(
    f"IC 95%: [{total_brugada['ci_lower']:,.0f}, "
    f"{total_brugada['ci_upper']:,.0f}]"
)

#Proporcion de votos
print(f"Proporcion poblacional:{true_ratio:,.4%}")
print(f"Proporcion estimado:{ratio_brugada['estimate']:,.4%}")
print(f"Error estandar: {ratio_brugada['standard_error']:,.6f}")
print(
    f"IC 95%: [{ratio_brugada['ci_lower']:,.4%}, "
    f"{ratio_brugada['ci_upper']:,.4%}]"
)