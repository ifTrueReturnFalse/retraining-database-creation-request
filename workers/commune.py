import models
import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


def load_commune(engine: create_engine, df_geographic_ref: pd.DataFrame) -> pd.DataFrame:
  print("---- T/L Commune ----")
  try:
    # Transform
    df_raw_commune = df_geographic_ref[["dep_code", "com_nom_maj", "com_code"]]
    df_commune_distinct = df_raw_commune.drop_duplicates()
    df_commune_distinct['code_commune'] = df_commune_distinct['com_code'].str[-3:]

    # Rename
    df_commune_clean = df_commune_distinct.rename(columns={
        "dep_code": "id_departement",
        "com_nom_maj": "nom",
        "com_code": "code_insee"
    })
    print(f"{len(df_commune_clean)} communes founded.")

    df_commune_clean['nom'] = normalize_commune(df_commune_clean['nom'])

    # Prepare
    commune_data = df_commune_clean.to_dict(orient="records")
    print(f"{len(commune_data)} to load.")

    # Load
    with Session(engine) as session:
      print("Loading commune in DB...")
      session.bulk_insert_mappings(models.Commune, commune_data)
      session.commit()
      print("Communes loaded successfully.")
  except Exception as error:
    print(f"ERROR (Commune) : {error}")
    raise


def normalize_commune(commune_series: pd.Series) -> pd.Series:
  print("Normalizing 'communes'.")
  normalized_series = commune_series.str.upper()

  normalized_series = normalized_series.replace('FALSE', 'FAUX')

  normalized_series = normalized_series.str.replace(
      r"^(L')(.+)", r"\2 (L )", regex=True
  )

  normalized_series = normalized_series.str.replace(
      r"^(LE )(.+)", r"\2 (LE)", regex=True
  )

  normalized_series = normalized_series.str.replace(
      r"^(LA )(.+)", r"\2 (LA)", regex=True
  )

  normalized_series = normalized_series.str.replace(
      r"^(LES )(.+)", r"\2 (LES)", regex=True
  )

  normalized_series = normalized_series.str.strip()
  print("Normalization ended.")
  return normalized_series
