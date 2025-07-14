import pandas as pd
import logging
import re
import os

# Define the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ensure the logs directory exists at the project root
log_dir = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(log_dir, exist_ok=True)

# Configure logging
log_file = os.path.join(log_dir, "data_cleaning.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("🚀 Data Cleaning Log initialized successfully!")


def load_csv(file_path):
    """ Load CSV file into a Pandas DataFrame. """
    try:
        df = pd.read_csv(file_path)
        logging.info(f"✅ CSV file '{file_path}' loaded successfully.")
        return df
    except Exception as e:
        logging.error(f"❌ Error loading CSV file: {e}")
        raise

def remove_emojis(text):
    """ Remove emojis from the message text using a regex pattern. """
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U00002702-\U000027B0"  # Miscellaneous Symbols
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def extract_youtube_links(text):
    """ Extract YouTube links from text, return 'No YouTube link' if none found. """
    youtube_pattern = r"(https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+)"
    links = re.findall(youtube_pattern, text)
    return ', '.join(links) if links else "No YouTube link"

def remove_youtube_links(text):
    """ Remove YouTube links from the message text. """
    youtube_pattern = r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+"
    return re.sub(youtube_pattern, '', text).strip()

def clean_text(text):
    """ Standardize text by removing newline characters and unnecessary spaces. """
    if pd.isna(text):
        return "No Message"
    return re.sub(r'\n+', ' ', text).strip()

def clean_dataframe(df):
    """ Perform all cleaning and standardization steps while avoiding SettingWithCopyWarning. """
    try:
        # ✅ Convert Date to datetime format, replacing NaT with None
        df.loc[:, 'date'] = pd.to_datetime(df['date'], errors='coerce')
        df.loc[:, 'date'] = df['date'].where(df['date'].notna(), None)
        logging.info("✅ Date column formatted to datetime.")

        # ✅ Fill missing values
        df.loc[:, 'text'] = df['text'].fillna("No Message")
        logging.info("✅ Missing values filled.")

        # ✅ Standardize text columns
        df.loc[:, 'channel_name'] = df['channel_name'].str.strip()
        df.loc[:, 'channel_title'] = df['channel_title'].str.strip()
        df.loc[:, 'text'] = df['text'].apply(clean_text)
        logging.info("✅ Text columns standardized.")

        # ✅ Remove emojis from message text
        df.loc[:, 'text'] = df['text'].apply(remove_emojis)

        # ✅ Remove YouTube links from message text
        df.loc[:, 'text'] = df['text'].apply(remove_youtube_links)

        # ✅ Rename columns to match PostgreSQL schema
        df = df.rename(columns={
            "channel_name": "channel_name",
            "channel_title": "channel_title",
            "text": "message",
            "date": "text_date"
        })

        logging.info("✅ Data cleaning completed successfully.")
        return df
    except Exception as e:
        logging.error(f"❌ Data cleaning error: {e}")
        raise

def save_cleaned_data(df, output_path):
    """ Save cleaned data to a new CSV file. """
    try:
        df.to_csv(output_path, index=False)
        logging.info(f"✅ Cleaned data saved successfully to '{output_path}'.")
        print(f"✅ Cleaned data saved successfully to '{output_path}'.")
    except Exception as e:
        logging.error(f"❌ Error saving cleaned data: {e}")
        raise