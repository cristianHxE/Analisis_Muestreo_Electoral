import pandas as pd
import numpy as np
import pytest

from src.estimadores import estimate_total, estimate_ratio

def test_estimate_total():
    sample = pd.DataFrame({"TOTAL_BRUGADA": [100,150,200]})

    result = estimate_total(sample, "TOTAL_BRUGADA", N =10)

    assert np.isclose(result["estimate"],1500)
    assert np.isclose(result["variance"], 58333.333333333336)
    assert np.isclose(result["standard_error"], np.sqrt(58333.333333333336))


def test_estimate_ratio():

    sample = pd.DataFrame({"TOTAL_BRUGADA":[120, 200, 150], "TOTAL_VOTOS":[300, 400, 300]})

    result = estimate_ratio(sample, numerator="TOTAL_BRUGADA", denominator="TOTAL_VOTOS", N=10)


    assert np.isclose(result["estimate"], 0.47)
    assert np.isclose(result["variance"], 0.0006993)
    assert np.isclose(
        result["standard_error"],
        np.sqrt(0.0006993))

def test_total_invalid_sample_size():
    sample = pd.DataFrame({"TOTAL_BRUGADA":[100, 150, 200]})

    with pytest.raises(ValueError):
        estimate_total(
            sample = sample,
            variable="TOTAL_BRUGADA",
            N=2
        )

def test_ratio_zero_denominator():
    
    sample = pd.DataFrame({"TOTAL_BRUGADA": [100, 150, 200],
        "TOTAL_VOTOS": [300, 0, 400]})

    with pytest.raises(ValueError):
        estimate_ratio(sample, numerator = "TOTAL_BRUGADA", denominator = "TOTAL_VOTOS", N= 10)

