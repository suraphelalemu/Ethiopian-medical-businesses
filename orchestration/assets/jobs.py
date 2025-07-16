from dagster import define_asset_job, AssetSelection
from .assets import scraping, database, dbt

medical_data_pipeline = define_asset_job(
    name="medical_data_pipeline",
    selection=AssetSelection.all()
)