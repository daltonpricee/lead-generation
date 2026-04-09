import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LEADS_OUTPUT_FILEPATH = os.getenv("LEADS_OUTPUT_FILEPATH", str(BASE_DIR / "data" / "leads.xlsx"))
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
THUMBTACK_API_KEY = os.getenv("THUMBTACK_API_KEY", "")
DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "Miami, FL")

# Optional configuration for source selection and query defaults.
GOOGLE_MAPS_SEARCH_QUERY = os.getenv("GOOGLE_MAPS_SEARCH_QUERY", "construction company")
THUMBTACK_SEARCH_QUERY = os.getenv("THUMBTACK_SEARCH_QUERY", "construction bookkeeping services")
