from dagster import ScheduleDefinition
from .jobs import medical_data_pipeline

daily_pipeline_schedule = ScheduleDefinition(
    job=medical_data_pipeline,
    cron_schedule="0 2 * * *",  # 2 AM daily
    name="daily_medical_data_pipeline"
)