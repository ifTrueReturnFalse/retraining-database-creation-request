import models
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def load_type_voie(engine: create_engine, df_real_estate: pd.DataFrame):
    print("---- T/L TypeVoie ----")
    try:
        # Transform
        df_raw_type_voie = df_real_estate[["Code type de voie", "Type de voie"]]
        df_type_voie_distinct = df_raw_type_voie.drop_duplicates()

        # Rename
        df_type_voie_clean = df_type_voie_distinct.rename(
            columns={"Code type de voie": "id_voie", "Type de voie": "voie"}
        )
        print(f"{len(df_type_voie_clean)} way types founded.")

        # Prepare
        df_type_voie_clean["voie"] = df_type_voie_clean["voie"].fillna("")
        type_voie_data = df_type_voie_clean.to_dict(orient="records")
        print(f"{len(type_voie_data)} way types to load.")

        # Load
        with Session(engine) as session:
            print("Loading way types in DB...")
            session.bulk_insert_mappings(models.TypeVoie, type_voie_data)
            session.commit()
            print("Way types loaded successfully.")

    except Exception as error:
        print(f"ERROR (TypeVoie) : {error}")
        raise
