import models
import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


def load_region(engine: create_engine, df_geographic_ref: pd.DataFrame):
  print("---- T/L Region ----")
  try:
    # Transform
    df_raw_regions = df_geographic_ref[["reg_code", "reg_nom"]]
    df_regions_distinct = df_raw_regions.drop_duplicates()

    # Rename
    df_regions_clean = df_regions_distinct.rename(columns={
        "reg_code": "id_region",
        "reg_nom": "nom"
    })
    print(f"{len(df_regions_clean)} regions founded.")

    # Check
    df_actual = pd.read_sql(
        select(models.Region.id_region),
        engine
    )

    if not df_actual.empty:
      existing_ids = df_actual['id_region'].tolist()
      df_to_load = df_regions_clean[~df_regions_clean['id_region'].isin(
          existing_ids)]
    else:
      df_to_load = df_regions_clean

    # Prepare
    regions_data = df_to_load.to_dict(orient="records")
    print(f"{len(regions_data)} regions to load.")

    # Load
    with Session(engine) as session:
      print("Loading regions in DB...")
      session.bulk_insert_mappings(models.Region, regions_data)
      session.commit()
      print("Regions loaded successfully.")

  except Exception as error:
    print(f"ERROR (Region) : {error}")
    raise
