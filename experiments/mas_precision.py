
import numpy as np
import pandas as pd

from src.simple_random_sampling import simple_random_sample
from src.estimadores import estimate_ratio

votos = pd.read_csv("data/processed/votos_cdmx_limpio.csv")

population = votos[votos["MUNICIPIO"] != "VOTO EN EL EXTRANJERO"].copy()

N = len(population)

true_ratio = (population["TOTAL_BRUGADA"].sum() / population["TOTAL_VOTOS"].sum())

print(f"Población: {N:,} casillas")
print(f"Razón poblacional: {true_ratio:.4%}")
#Configuracion de las simulaciones
sample_sizes = [50, 100, 200, 500, 1000]
B = 500

results = []

for j, n in enumerate(sample_sizes):
    estimates = []
    estimated_variances = []
    coverage = []
    for b in range(B):

        #Seleccionamos la muestra MAS
        sample = simple_random_sample(population = population, n=n, seed = 10000 + b)

        #Estimador de razon y varianza

        result = estimate_ratio(sample=sample,numerator = "TOTAL_BRUGADA", denominator = "TOTAL_VOTOS", N=N)

        estimates.append(result["estimate"])
        estimated_variances.append(result["variance"])

        #¿EL intervalo contiene al parametro?
        inside = (result["ci_lower"] <=true_ratio <=result["ci_upper"])

        coverage.append(inside)
    
    estimates = np.array(estimates)
    estimated_variances = np.array(estimated_variances)

    #Media de las poblaciones
    estimate_mean = estimates.mean()
    
    #Sesgo empirico
    bias = estimate_mean - true_ratio 
    #VArianza observada entre muestras
    empirical_variance = estimates.var(ddof=1)

    #promedio de las varianzas estimadas
    mean_estimated_variance = estimated_variances.mean()
    # Error cuadrático medio
    mse = np.mean((estimates - true_ratio) ** 2)

    # desviacion de MSE
    rmse = np.sqrt(mse)
     # Cobertura empírica
    empirical_coverage = np.mean(coverage)

    # Guardar los resultados de este tamaño muestral
    results.append({
        "n": n,
        "mean_estimate": estimate_mean,
        "bias": bias,
        "empirical_variance": empirical_variance,
        "mean_estimated_variance": mean_estimated_variance,
        "mse": mse,
        "rmse": rmse,
        "coverage": empirical_coverage
    })

# Convertir los resultados a DataFrame
results_df = pd.DataFrame(results)

print("\nResultados de la simulación:")
print(results_df.round(6).to_string(index=False))


import matplotlib.pyplot as plt
from pathlib import Path

output_dir = Path('reports/figures')
output_dir.mkdir(parents = True, exist_ok = True)

#Comparacion de varianzas
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(results_df["n"],
results_df["empirical_variance"],
marker="o",
label="Varianza empirica"
)

ax.plot(
    results_df["n"],
    results_df["mean_estimated_variance"],
    marker="s",
    linestyle="--",
    label="Varianza linealizada promedio"
)

ax.set(xlabel="Tamaño de muestra",
    ylabel="Varianza de la razon estimada",
    title="Precision del estimador de razon bajo MAS" 
)
ax.legend()
ax.grid(alpha=0.3)

fig.tight_layout()
fig.savefig(output_dir / "mas_variance_comparison.png", dpi=150)
plt.show()

fig, ax = plt.subplots(figsize=(8,5)) 
ax.plot( results_df["n"],
    results_df["coverage"],
    marker="o",
    label="Cobertura empirica"  
    )

ax.axhline(y=0.95,
    linestyle="--",
    label="Cobertura al 95%" )
ax.set(xlabel="Tamaño de muestra", 
    ylabel="Cobertura", 
    title="Cobetura de intervalos confianza bajo MAS",
    ylim=(0,1))

ax.legend()
ax.grid(alpha = 0.3)

fig.tight_layout()
fig.savefig(output_dir / "mas_coverage.png", dpi=150)
plt.show()
