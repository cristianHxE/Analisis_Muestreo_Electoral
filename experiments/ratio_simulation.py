import pandas as pd

from src.simple_random_sampling import simple_random_sample
from src.estimadores import estimate_ratio

votos = pd.read_csv("data/processed/votos_cdmx_limpio.csv")

population = votos.loc[votos["MUNICIPIO"] != "VOTO EN EL EXTRANJERO"].copy()

N = len(population)
#Ratio poblacional 
true_ratio = (population["TOTAL_BRUGADA"].sum() / population["TOTAL_VOTOS"].sum())

#Configuracion
n = 100
B = 500

estimates = []
for b in range(B):
    sample = simple_random_sample(population=population, n=n, seed=1000+b)

    result = estimate_ratio(sample= sample, numerator = "TOTAL_BRUGADA", denominator = "TOTAL_VOTOS",N=N)
    estimates.append(result["estimate"])

estimates = pd.Series(estimates)

# Resumen de resultados
print(f"Parámetro poblacional: {true_ratio:.4%}")
print(f"Media de las estimaciones: {estimates.mean():.4%}")
print(f"Sesgo empírico: {estimates.mean() - true_ratio:.6f}")
print(f"Varianza empírica: {estimates.var(ddof=1):.8f}")