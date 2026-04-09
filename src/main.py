import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config.settings import LEADS_OUTPUT_FILEPATH, GOOGLE_MAPS_SEARCH_QUERY, THUMBTACK_SEARCH_QUERY
from src.collectors.website_collector import WebsiteCollector
from src.sources.google_maps_source import GoogleMapsSource
from src.sources.thumbtack_source import ThumbtackSource
from src.storage.lead_repository import LeadRepository
from src.utils.http_client import HTTPClient


def main() -> None:
    """
    Full bookkeeping lead generation pipeline.
    """
    google_source = GoogleMapsSource()
    thumbtack_source = ThumbtackSource()
    repo = LeadRepository(LEADS_OUTPUT_FILEPATH)

    http_client = HTTPClient()
    collector = WebsiteCollector(http_client)

    existing_companies = repo.load_existing_companies()

    google_leads = google_source.search(GOOGLE_MAPS_SEARCH_QUERY, max_results=30)
    thumbtack_leads = thumbtack_source.search(THUMBTACK_SEARCH_QUERY, max_results=30)

    all_leads = google_leads + thumbtack_leads
    new_leads = []
    seen_companies = set(existing_companies)

    for lead in all_leads:
        company_key = lead.company.strip().lower()
        if not company_key or company_key in seen_companies:
            continue

        print(f"Processing: {lead.company}")

        if lead.website:
            contact = collector.scrape_contact_info(lead.website)
            lead.email = lead.email or contact["email"]
            lead.phone = lead.phone or contact["phone"]

        new_leads.append(lead)
        seen_companies.add(company_key)

    if new_leads:
        repo.save(new_leads)
        print(f"Added {len(new_leads)} new leads")
        print(f"Saved to Excel: {LEADS_OUTPUT_FILEPATH}")
    else:
        print("No new leads found")


if __name__ == "__main__":
    main()
