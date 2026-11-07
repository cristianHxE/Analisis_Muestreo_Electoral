import pandas as pd

BRUGADA_COLS = ["PVEM","PT","MORENA","PT_MORENA","PVEM_PT_MORENA","PVEM_PT","PVEM_MORENA"]

TABOADA_COLS = ["PAN","PRI","PRD","PRI_PRD","PAN_PRI_PRD","PAN_PRI","PAN_PRD"]

def create_electoral_variables(df: pd.DataFrame) -> pd.DataFrame:
     data = df.copy()

     require_cols = (BRUGADA_COLS + TABOADA_COLS 
     + ["MC", "NUM_VOTOS_VALIDOS", "NUM_VOTOS_NULOS", "NUM_VOTOS_CAN_NREG"])

     missings_cols = set(require_cols) - set(data.columns)

     if missings_cols:
          raise ValueError(f"Columnas faltates: {missings_cols}")

     if data[require_cols].isna().any().any():
          raise ValueError("Existen valores faltantes en columnas electorales")
     
     if (data[require_cols] <0).any().any():
          raise ValueError("Votos invalidos")

     data["TOTAL_BRUGADA"] = data[BRUGADA_COLS].sum(axis=1)
     data["TOTAL_TABOADA"] = data[TABOADA_COLS].sum(axis=1)
     return data