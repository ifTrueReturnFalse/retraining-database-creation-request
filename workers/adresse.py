import models
import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


def load_adresse(
    engine: create_engine, df_real_estate: pd.DataFrame, df_commune: pd.DataFrame
) -> pd.DataFrame:
    print("---- T/L Adresse ----")
    try:
        # Transform
        df_raw_adresse = df_real_estate[
            ["No voie", "Code commune", "Code departement", "Code type de voie", "Voie"]
        ]
        df_adresse_distinct = df_raw_adresse.drop_duplicates()

        # Rename
        df_adresse_clean = df_adresse_distinct.rename(
            columns={
                "No voie": "numero_voie",
                "Code commune": "code_commune",
                "Code departement": "id_departement",
                "Code type de voie": "id_voie",
                "Voie": "nom_voie",
            }
        )
        print(f"{len(df_adresse_clean)} adresses founded.")

        df_adresse_clean["code_insee"] = (
            df_adresse_clean["id_departement"] + df_adresse_clean["code_commune"]
        )

        df_adresse_merged = pd.merge(
            df_adresse_clean, df_commune, on="code_insee", how="inner"
        )

        df_adresse_to_load = df_adresse_merged[
            ["id_commune", "numero_voie", "nom_voie", "id_voie"]
        ]

        # Prepare
        adresse_data = df_adresse_to_load.to_dict(orient="records")
        print(f"{len(adresse_data)} adresses to load.")

        # Load
        with Session(engine) as session:
            print("Loading adresses in DB...")
            session.bulk_insert_mappings(models.Adresse, adresse_data)
            session.commit()
            print("Adresses loaded successfully.")

        df_adresse = pd.read_sql(select(models.Adresse), engine)
        df_adresse["numero_voie"] = df_adresse["numero_voie"].astype("Int64")
        return df_adresse

    except Exception as error:
        print(f"ERROR (Adresse) : {error}")
        raise
