Task 1: Data Scraping and Collection Pipeline
Overview

This project aims to develop a data scraping and collection pipeline to extract relevant data from public Telegram channels related to Ethiopian medical businesses. The project will utilize the Telegram API and custom scripts for data extraction, focusing on both textual data and images for object detection.
Channels to Scrape

The following Telegram channels will be targeted for data scraping:

    Doctors Ethiopia
    Chemed Telegram Channel
    Lobelia Pharmacy and Cosmetics
    Yetenaweg
    Ethio-American Medical Trainings

Objectives

    Text Data Extraction: Scrape and collect textual data from the specified Telegram channels.
    Image Collection: Gather images from the targeted channels for future object detection tasks.

Completed Tasks

1. Telegram Data Scraping

   Use the telethon library in Python to interact with the Telegram API.
   Develop scripts to extract data from the specified channels.
   Alternatively, export content using the Telegram application if necessary.

2. Image and Data Collection

   Focus on collecting images specifically from:
   Chemed Telegram Channel
   Lobelia Pharmacy and Cosmetics
   Ensure that the images collected are suitable for object detection tasks.

🚀 Features

    Telegram data scraping with Telethon
    Data lake with partitioned JSON storage
    Star schema data warehouse in PostgreSQL
    dbt transformations with testing
    YOLOv8 image object detection
    FastAPI analytical endpoints
    Dagster pipeline orchestration
    Dockerized environment

📊 Business Insights

Answers key questions:

    Top 10 mentioned medical products
    Price/availability across channels
    Visual content analysis (pills vs creams)
    Daily/weekly posting trends
    Channel comparison metrics

🛠️ Technical Stack
Component Technology
Data Extraction Telethon
Data Storage PostgreSQL 13
Transformation dbt-core 1.10+
Object Detection YOLOv8 (Ultralytics)
API Framework FastAPI + Uvicorn
Orchestration Dagster
Infrastructure Docker + Docker Compose

Prerequisites

    Docker & Docker Compose
    Python 3.9+
    Telegram API credentials

Installation
Clone the repository:

git clone https://github.com/your-repo/ethiopian-medical-data-platform.git
cd ethiopian-medical-data-platform

Configure environment:

bash cp .env.example .env
Edit with your Telegram API credentials

Start services:

bash docker-compose up -d --build Initialize database:

bash docker-compose exec dbt python scripts/database/load_raw_data.py 🔍 Task Details Task 1: Data Scraping Key Components:

scripts/scraping/telegram_scraper.py: Main scraping script

scripts/scraping/image_downloader.py: Image download utility

Usage:

bash docker-compose exec dbt python scripts/scraping/telegram_scraper.py Output Structure:

text data/raw/ ├── telegram_messages/ │ └── YYYY-MM-DD/ │ └── channel_name.json └── telegram_images/ └── YYYY-MM-DD/ └── channel_name/ ├── 12345.jpg └── 12345.json Task 2: Data Modeling dbt Models:

Staging: stg_telegram_messages, stg_telegram_images

Dimensions: dim_channels, dim_dates

Facts: fct_messages, fct_image_detections

Run Transformations:

bash docker-compose exec dbt bash cd dbt/medical_analytics dbt run dbt test Task 3: Object Detection Processing Script:

bash docker-compose exec dbt python app/object_detection/process_images.py Detection Schema:

sql CREATE TABLE analytics.fct_image_detections ( detection_key VARCHAR(255) PRIMARY KEY, message_id INTEGER REFERENCES fct_messages, class_name VARCHAR(50), confidence FLOAT, is_medical BOOLEAN ); Task 4: Analytical API Endpoints:

GET /api/analytics/top-products

GET /api/channels/{channel}/activity

GET /api/search/messages?query=

Access API:

bash curl http://localhost:8000/api/analytics/top-products?limit=5 Task 5: Orchestration Run Pipeline:

bash dagster dev -f orchestration/init.py Scheduled Jobs:

python

Project Structure

+---.github
| └── workflows
| └── blank.yml
+---.vscode
| └── settings.json
+---api
| ├── init.py
+---Medical_Business_Data_Warehouse
| | ├── analyses
| | ├── dbt_packages
| | ├── logs
| | | ├── dbt.log
| | ├── macros
| | ├── models
| | | 
| | ├── seeds
| | ├── snapshots
| | ├── target
| | ├── tests
| └── .gitignore
| └── dbt_project.yml
| └── README.md
+---notebooks
| ├── init.ipynb
| ├── data_cleaning.ipynb
| └── README.md
| └── telegram_message_scrapper.ipynb
+---scripts
| ├── init.py
| └── README.md
| ├── data_cleaning.py
| ├── database_setup.py
| ├── image_scraper.py
| ├── telegram_scraper.py
+---src
| └── README.md
| └── init.py
+---tests
| └── init.py
| ├── README.md
| └── test_scraper.py
| ├── .gitignore
| ├── LICENSE
| ├── README.md
| └── requirements.txt