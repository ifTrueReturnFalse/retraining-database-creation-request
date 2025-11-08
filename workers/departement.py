import models
import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


def load_departement(engine: create_engine, df_geographic_ref: pd.DataFrame):
    print("---- T/L Departement ----")
    try:
        # Transform
        df_raw_departement = df_geographic_ref[["dep_code", "dep_nom", "reg_code"]]
        df_departement_distinct = df_raw_departement.drop_duplicates()

        # Rename
        df_departement_clean = df_departement_distinct.rename(
            columns={
                "dep_code": "id_departement",
                "dep_nom": "nom",
                "reg_code": "id_region",
            }
        )
        print(f"{len(df_departement_clean)} departements founded.")

        # Check
        df_actual = pd.read_sql(select(models.Departement.id_departement), engine)

        if not df_actual.empty:
            existing_ids = df_actual["id_departement"].tolist()
            df_to_load = df_departement_clean[
                ~df_departement_clean["id_departement"].isin(existing_ids)
            ]
        else:
            df_to_load = df_departement_clean

        # Prepare
        departement_data = df_to_load.to_dict(orient="records")
        print(f"{len(departement_data)} to load.")

        # Load
        with Session(engine) as session:
            print("Loading departements in DB...")
            session.bulk_insert_mappings(models.Departement, departement_data)
            session.commit()
            print("Departements loaded successfully.")
    except Exception as error:
        print(f"ERROR (Departement) : {error}")
        raise
