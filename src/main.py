import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config.settings import LEADS_OUTPUT_FILEPATH, GOOGLE_MAPS_SEARCH_QUERY, THUMBTACK_SEARCH_QUERY
from src.collectors.website_collector import WebsiteCollector
from src.sources.google_maps_source import GoogleMapsSource
from src.sources.thumbtack_source import ThumbtackSource
from src.sources.yelp_source import YelpSource
from src.sources.foursquare_source import FoursquareSource
from src.sources.bing_source import BingSource
from src.storage.lead_repository import LeadRepository
from src.utils.http_client import HTTPClient


def main() -> None:
    """
    Full bookkeeping lead generation pipeline.

    Searches multiple sources for construction companies, deduplicates,
    enriches with contact info, and saves to Excel.
    """
    google_source = GoogleMapsSource()
    thumbtack_source = ThumbtackSource()
    yelp_source = YelpSource()
    foursquare_source = FoursquareSource()
    bing_source = BingSource()
    repo = LeadRepository(LEADS_OUTPUT_FILEPATH)

    http_client = HTTPClient()
    collector = WebsiteCollector(http_client)

    existing_companies = repo.load_existing_companies()

    google_leads = google_source.search(GOOGLE_MAPS_SEARCH_QUERY, max_results=200)
    thumbtack_leads = thumbtack_source.search(THUMBTACK_SEARCH_QUERY, max_results=200)
    yelp_leads = yelp_source.search(GOOGLE_MAPS_SEARCH_QUERY, max_results=200)
    foursquare_leads = foursquare_source.search(GOOGLE_MAPS_SEARCH_QUERY, max_results=200)
    bing_leads = bing_source.search(GOOGLE_MAPS_SEARCH_QUERY, max_results=200)

    all_leads = google_leads + thumbtack_leads + yelp_leads + foursquare_leads + bing_leads

    # TODO: Add more sources like Foursquare, Yellow Pages API (if available), or custom scrapers
    # Example: foursquare_source = FoursquareSource()
    # foursquare_leads = foursquare_source.search(GOOGLE_MAPS_SEARCH_QUERY, max_results=200)
    # all_leads += foursquare_leads
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
