from typing import List
from src.models.lead import Lead


class GoogleMapsSource:
    """
    Demo Google Maps source that simulates discovering local businesses.
    """

    def search(self, query: str) -> List[Lead]:
        """
        Simulates searching for businesses.

        Args:
            query (str): Search term.

        Returns:
            List[Lead]: Fake but realistic leads.
        """
        return [
            Lead(
                name="Mike Johnson",
                company="Mike's Plumbing",
                website="https://mikesplumbingaz.com",
                linkedin_url="https://linkedin.com/company/mikesplumbing"
            ),
            Lead(
                name="Sarah Lee",
                company="Desert Air HVAC",
                website="https://desertairhvac.com",
                linkedin_url="https://linkedin.com/company/desertairhvac"
            ),
            Lead(
                name="Carlos Ramirez",
                company="Phoenix Home Roofing",
                website="https://phxroofingpros.com",
                linkedin_url="https://linkedin.com/company/phxroofing"
            ),
        ]