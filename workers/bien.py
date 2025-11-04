import models
import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


def load_bien(engine: create_engine, df_real_estate: pd.DataFrame, df_adresse: pd.DataFrame, df_commune: pd.DataFrame):
  print("---- T/L Bien ----")
  try:
    # Transform
    df_raw_bien = df_real_estate[[
        "No voie", "Code type de voie", "Voie", 
        "1er lot", "Surface Carrez du 1er lot", "Type local", "Surface reelle bati", "Nombre pieces principales", "B/T/Q", "Code departement", "Code commune"]]
    df_bien_distinct = df_raw_bien.drop_duplicates()

    df_bien_clean = df_bien_distinct.rename(columns={
        "No voie": "numero_voie",
        "Code type de voie": "id_voie",
        "Voie": "nom_voie",
        "B/T/Q": "btq",
        "Nombre pieces principales": "nombre_pieces",
        "Surface Carrez du 1er lot": "surface_carrez",
        "Surface reelle bati": "surface_local",
        "Type local": "type_bien",
        "Code departement": "id_departement",
        "Code commune": "code_commune",
        "1er lot": "lot"
    })

    df_bien_clean['code_insee'] = df_bien_clean['id_departement'] + df_bien_clean ['code_commune']

    df_adresse_commune = pd.merge(
      df_adresse,
      df_commune,
      on="id_commune",
      how="inner"
    )

    print(f"{len(df_bien_clean)} biens founded.")

    df_bien_merged = pd.merge(
        df_bien_clean, df_adresse_commune, 
        on=["code_insee", "nom_voie", "id_voie", "numero_voie"], 
        how="inner")

    df_bien_to_load = df_bien_merged[["id_adresse", "btq", "nombre_pieces", "surface_carrez", "surface_local", "type_bien", "lot"]]

    # Prepare
    bien_data = df_bien_to_load.to_dict(orient="records")
    print(f"{len(bien_data)} biens to load.")

    # Load
    with Session(engine) as session:
      print("Loading biens in DB...")
      session.bulk_insert_mappings(models.Bien, bien_data)
      session.commit()
      print("Biens loaded successfully.")
    
    df_bien = pd.read_sql(select(models.Bien), engine)
    return df_bien

  except Exception as error:
    print(f"ERROR (Bien) : {error}")
    raise
