""" Asignacion de distritos deferales a las 
casillas de la eleccion para Jefatura de Gobierno de la CDMX 2024 
"""

from pathlib import Path
import sys
import pandas as pd

KEY = ["ID_ESTADO", "SECCION", "TIPO_CASILLA", "ID_CASILLA", "EXT_CONTIGUA"]
FOREING = "VOTO EN EL EXTRANJERO"
ESP = {"VOTO ANTICIPADO", "VOTO PERSONAS EN PRISION PREVENTIVA"}

def preparation_data(election_path: Path | str, district_path: Path | str) -> pd.DataFrame:
    b_electoral = pd.read_csv(election_path)
    distritos_id = pd.read_csv(district_path)

    if b_electoral.duplicated(KEY).any() or distritos_id.duplicated(KEY).any():
        raise ValueError("Hay claves de casillas duplicadad; revisa antes de unir.")
    
    result = b_electoral.merge(distritos_id[KEY + ["ID_DISTRITO_FEDERAL"]], on =KEY,
     how="left", validate="one_to_one", indicator=True)
    #Deteccion de casillas no identificadas
    missing = result["_merge"] == "left_only"
    unexpected = missing & ~result["MUNICIPIO"].isin(ESP | {FOREING})
    
    if unexpected.any():
        raise ValueError(f"Hay {unexpected.sum()} casillas no identidicados")
    seccion_distrito = distritos_id.groupby(["ID_ESTADO","SECCION"])["ID_DISTRITO_FEDERAL"].agg(["nunique","first"])
    if(seccion_distrito["nunique"] > 1).any():
        raise ValueError(
            "Hay secciones que se asocian a mas de un distrito federal"
        )
    #Asignacion de casillas especiales
    seccion_lookup = seccion_distrito["first"]
    esp_mask = missing & result["MUNICIPIO"].isin(ESP)
    seccion_keys = pd.MultiIndex.from_frame(result.loc[esp_mask, ["ID_ESTADO","SECCION"]])
    result.loc[esp_mask, "ID_DISTRITO_FEDERAL"] = seccion_lookup.reindex(seccion_keys).to_numpy()
    #Asignacion de la casilla voto en el extranjero
    foreing_mask = missing & result["MUNICIPIO"].eq(FOREING)
    result.loc[foreing_mask, "ID_DISTRITO_FEDERAL"] = 0

    #Comprobaciones 
    if result["ID_DISTRITO_FEDERAL"].isna().any():
        raise ValueError("No fue posible asignar algunas casillas a su distrito federal asociado")

    if len(result) != len(b_electoral):
        raise ValueError(f"El numero de casillas paso de {len(b_electoral)} a {len(result)}")
    result["ID_DISTRITO_FEDERAL"] = result["ID_DISTRITO_FEDERAL"].astype("int64")

    return result.drop(columns="_merge")

if __name__ == "__main__":
    if len(sys.argv) !=4:
        raise SystemExit(
            "Uso: python data_processed.py VOTOS.csv DISTRITOS.csv SALIDA.csv")
    output = preparation_data(sys.argv[1], sys.argv[2])

    output_path = Path(sys.argv[3])
    output_path.parent.mkdir(parents=True,exist_ok =True)
    output.to_csv(output_path, index=False) 

    print(f"Archivo creado: {output_path} ({len(output):,} filas)")
    print(output.groupby("MUNICIPIO")["ID_DISTRITO_FEDERAL"].count().tail())
