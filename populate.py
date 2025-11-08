import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import workers
import models

# Engine setup
engine = create_engine("sqlite:///data_immo.db")

# DB cleanup
print("Cleaning tables")
with Session(engine) as session:
    session.execute(text(f"DELETE FROM {models.Vente.__tablename__}"))
    session.execute(text(f"DELETE FROM {models.Bien.__tablename__}"))
    # session.execute(text(f"DELETE FROM {models.TypeVoie.__tablename__}"))
    # session.execute(text(f"DELETE FROM {models.Adresse.__tablename__}"))
    session.execute(text(f"DELETE FROM {models.Commune.__tablename__}"))
    session.execute(text(f"DELETE FROM {models.Departement.__tablename__}"))
    session.execute(text(f"DELETE FROM {models.Region.__tablename__}"))

    session.commit()

print("Tables ready to be loaded.")

# Region extract
try:
    print("Reading geographic reference...")
    reference_column_type = {"dep_code": str, "com_nom_maj": str, "com_code": str}

    df_geographic_ref = pd.read_excel(
        "./source_data/fr-esr-referentiel-geographique.xlsx",
        dtype=reference_column_type,
    )

    print("Reading real estate sales...")
    estate_column_type = {
        "Code departement": str,
        "Code commune": str,
        "Code type de voie": int,
        "No voie": pd.Int64Dtype(),
        "B/T/Q": str,
    }
    df_real_estate = pd.read_excel(
        "./source_data/Valeurs-foncieres.xlsx", dtype=estate_column_type
    )
    df_real_estate["B/T/Q"] = df_real_estate["B/T/Q"].fillna("")

    print("Reading cities info...")
    commune_info_type = {"CODDEP": str, "CODCOM": str, "PTOT": int}
    df_commune_info = pd.read_excel(
        "./source_data/donnees_communes.xlsx", dtype=commune_info_type
    )

    workers.load_region(engine, df_geographic_ref)
    workers.load_departement(engine, df_geographic_ref)
    df_commune = workers.load_commune(engine, df_geographic_ref, df_commune_info)
    # workers.load_type_voie(engine, df_real_estate)
    # df_adresse = workers.load_adresse(engine, df_real_estate, df_commune)
    df_bien = workers.load_bien(engine, df_real_estate, df_commune)
    workers.load_vente(engine, df_real_estate, df_commune, df_bien)

except FileNotFoundError:
    print("ERROR: Source file not found")
except KeyError as error:
    print(f"ERROR: Column not found : {error}")
except Exception as error:
    print(f"A error has occured : {error}")
