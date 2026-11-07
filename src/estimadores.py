import numpy as np
import pandas as pd
from statistics  import NormalDist

def estimate_total(sample: pd.DataFrame, variable: str, N: int, confidence: float = 0.95) -> dict():

    n = len(sample)

     #Validaciones
    if not isinstance(N, int) or isinstance(N, bool):
        raise TypeError("N debe ser un entero.")

    if not 2 <= n <= N:
        raise ValueError("Se requiere 2 <= n <= N.")

    if variable not in sample.columns:
        raise ValueError(f"No existe la columna {variable}.")

    y = sample[variable]


    if y.isna().any():
        raise ValueError("La variable contiene valores faltantes.")

    if not 0 < confidence < 1:
        raise ValueError("El nivel de confianza debe estar entre 0 y 1.")

    #Estimador del Total
    y_mean = y.mean()
    total_estimate = N * y_mean
    #Varianza muestral 
    s2 = y.var(ddof=1)
    #Correcion por poblacion finita
    f = n / N
    variance = N ** 2 * (1-f) * s2/n
    #Error estandar
    standard_error = np.sqrt(variance)
    #Intervalo de confianza
    z = NormalDist().inv_cdf((1 + confidence) / 2)
    ci_lower = total_estimate - z * standard_error
    ci_upper = total_estimate + z * standard_error

    return {"estimate": total_estimate, "variance": variance,
        "standard_error": standard_error, "ci_lower": ci_lower,
        "ci_upper": ci_upper, "Tamaño_muestra": n, "Total_Poblacion": N}


def estimate_ratio( sample: pd.DataFrame, numerator: str, denominator: str,
    N: int, confidence: float = 0.95) -> dict:

    n = len(sample)
    if not isinstance(N, int) or isinstance(N, bool):
        raise TypeError("N debe ser un entero.")

    if not 2 <= n <= N:
        raise ValueError("Se requiere 2 <= n <= N.")
        
    required = [numerator, denominator]
    missing = set(required) - set(sample.columns)

    if missing:
            raise ValueError(f"Columnas faltantes: {missing}")

    if sample[required].isna().any().any():
            raise ValueError("Existen valores faltantes.")

    if not 0 < confidence < 1:
        raise ValueError("El nivel de confianza debe estar entre 0 y 1.")
        

    y = sample[numerator]
    x = sample[denominator]
    if (x <= 0).any():
        raise ValueError("El denominador debe ser positivo en cada casilla.")

        #EStimador de razon
    ratio_estimate = y.sum() / x.sum()
    #Calculo de residuios
    residuals = y - ratio_estimate * x
    #Varianza residual
    s2_residuals = residuals.var(ddof=1)
    #varianza aproximada del estimador 
    f = n / N
    x_mean = x.mean()

    variance = (
        (1-f) * s2_residuals / (n * x_mean**2)
    )
    stdr_error = np.sqrt(variance)
    #Intervalo de confianza
    z = NormalDist().inv_cdf((1+ confidence) / 2)

    ci_lower = ratio_estimate - z * stdr_error 
    ci_upper = ratio_estimate + z * stdr_error

    return {
        "estimate":ratio_estimate,
        "variance":variance,
        "standard_error":stdr_error,
        "ci_upper":ci_upper,
        "ci_lower":ci_lower,
        "n":n,
        "N": N
    }   




