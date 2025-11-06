import models
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def load_vente(engine: create_engine, df_real_estate: pd.DataFrame, df_commune: pd.DataFrame, df_bien: pd.DataFrame):
  print("---- T/L Vente ----")
  try:
    # Transform
    df_raw_vente = df_real_estate[[
        "No voie", "Code type de voie", "Voie", 
        "1er lot", "Code departement", "Code commune", 
        "Date mutation", "Valeur fonciere", "Surface Carrez du 1er lot", "Type local"]]

    df_raw_vente = df_raw_vente.dropna(subset=["Valeur fonciere"])

    df_vente_clean = df_raw_vente.rename(columns={
        "No voie": "numero_voie",
        "Code type de voie": "id_voie",
        "Voie": "nom_voie",
        "Code departement": "id_departement",
        "Code commune": "code_commune",
        "1er lot": "lot",
        "Date mutation": "date_vente",
        "Valeur fonciere": "valeur",
        "Surface Carrez du 1er lot": "surface_carrez",
        "Type local": "type_bien"
    })

    df_vente_clean['code_insee'] = df_vente_clean['id_departement'] + df_vente_clean ['code_commune']

    print(f"{len(df_vente_clean)} ventes founded.")

    df_commune_bien = pd.merge(
      df_bien,
      df_commune,
      on="id_commune",
      how="inner"
    )
    
    df_vente_merged = pd.merge(
        df_vente_clean, df_commune_bien, 
        on=["code_insee", "lot", "surface_carrez", "type_bien"], 
        how="inner")

    df_vente_to_load = df_vente_merged[["id_bien", "date_vente", "valeur"]]

    # Prepare
    vente_data = df_vente_to_load.to_dict(orient="records")
    print(f"{len(vente_data)} ventes to load.")

    # Load
    with Session(engine) as session:
      print("Loading ventes in DB...")
      session.bulk_insert_mappings(models.Vente, vente_data)
      session.commit()
      print("Ventes loaded successfully.")

  except Exception as error:
    print(f"ERROR (Vente) : {error}")
    raise
