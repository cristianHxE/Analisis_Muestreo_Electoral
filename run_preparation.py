from pathlib import Path

from src.data_processed import preparation_data
from src.electoral_variables import create_electoral_variables

#Integracion de la base de datos
votos = preparation_data("data/raw/2024_SEE_GOB_CDMX_CAS.csv",
       "data/raw/DIS_FED_09.csv" )

#Construccion de variables
votos = create_electoral_variables(votos)

#Almacenamiento del resultado

output_path = Path("data/processed/votos_cdmx_limpio.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

votos.to_csv(output_path, index=False)

print(f"Casillas: {len(votos):,}")
print(votos[["TOTAL_BRUGADA","TOTAL_TABOADA","MC"]].sample())