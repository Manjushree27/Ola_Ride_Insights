from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "OLA_DataSet.xlsx"
CLEANED_FILE = PROJECT_ROOT / "data" / "cleaned" / "ola_bookings_cleaned.csv"


def normalize_text(value):
    if value is None:
        return None
    text = str(value).strip()
    if text == "" or text.lower() in {"null", "none", "nan"}:
        return None
    return text


def ensure_output_dirs():
    for folder in [
        PROJECT_ROOT / "data" / "cleaned",
        PROJECT_ROOT / "outputs" / "query_results",
        PROJECT_ROOT / "outputs" / "reports",
        PROJECT_ROOT / "outputs" / "screenshots",
    ]:
        folder.mkdir(parents=True, exist_ok=True)

