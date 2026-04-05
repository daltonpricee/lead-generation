from src.sources.google_maps_source import GoogleMapsSource
from src.storage.lead_repository import LeadRepository
from src.utils.http_client import HTTPClient
from src.collectors.website_collector import WebsiteCollector


def main() -> None:
    """
    Full lead generation pipeline.
    """
    source = GoogleMapsSource()
    repo = LeadRepository("data/leads.xlsx")

    http_client = HTTPClient()
    collector = WebsiteCollector(http_client)

    # STEP 1: Load existing companies
    existing_companies = repo.load_existing_companies()

    # STEP 2: Get new businesses
    leads = source.search("plumbers phoenix")

    new_leads = []

    for lead in leads:
        if lead.company.lower() in existing_companies:
            continue  # skip duplicates

        print(f"Processing: {lead.company}")

        # STEP 3: (optional) enrich if website exists
        if lead.website:
            contact = collector.scrape_contact_info(lead.website)
            lead.email = contact["email"]
            lead.phone = contact["phone"]

        new_leads.append(lead)

    # STEP 4: Save only new leads
    if new_leads:
        repo.save(new_leads)
        print(f"Added {len(new_leads)} new leads")
        print("Saved to Excel: data/leads.xlsx")
    else:
        print("No new leads found")


if __name__ == "__main__":
    main()