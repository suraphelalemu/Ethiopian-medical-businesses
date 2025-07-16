# orchestration/definitions.py
from dagster import Definitions
from .assets import scrape_telegram_data, load_raw_data, run_dbt_transformations
from .jobs import medical_data_pipeline
from .schedules import daily_pipeline_schedule

defs = Definitions(
    assets=[scrape_telegram_data, load_raw_data, run_dbt_transformations],
    jobs=[medical_data_pipeline],
    schedules=[daily_pipeline_schedule]
)