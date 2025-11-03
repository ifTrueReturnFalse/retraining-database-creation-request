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
  session.execute(text(f"DELETE FROM {models.Commune.__tablename__}"))
  session.execute(text(f"DELETE FROM {models.Departement.__tablename__}"))
  session.execute(text(f"DELETE FROM {models.Region.__tablename__}"))

  session.commit()

print("Tables ready to be loaded.")

# Region extract
try:
  print("Reading geographic reference...")
  column_type = {
      'dep_code': str,
      'com_nom_maj': str,
      "com_code": str
  }

  df_geographic_ref = pd.read_excel(
      "./source_data/fr-esr-referentiel-geographique.xlsx",
      dtype=column_type)
  # df_geographic_ref['dep_code'] = df_geographic_ref['dep_code'].astype(str)
  # df_geographic_ref['com_nom_maj'] = df_geographic_ref['com_nom_maj'].astype(
  #     str)

  workers.load_region(engine, df_geographic_ref)
  workers.load_departement(engine, df_geographic_ref)
  workers.load_commune(engine, df_geographic_ref)

except FileNotFoundError:
  print("ERROR: Source file not found")
except KeyError as error:
  print(f"ERROR: Column not found : {error}")
except Exception as error:
  print(f"A error has occured : {error}")
