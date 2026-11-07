import pandas as pd

def simple_random_sample(
    population: pd.DataFrame,
    n: int,
    seed: int| None = None
    ) -> pd.DataFrame:

    N = len(population)

    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"El tamaño de muestra debe ser un entero.")
    if not 1  <= n <= N:
        raise ValueError(f"El tamaño de muestra n debe estar entre 1 y {N}.")

    sample = population.sample(n=n, replace=False, random_state=seed)

    return sample.copy()