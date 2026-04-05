from typing import List
from src.models.lead import Lead


class GoogleMapsSource:
    """
    Simulated Google Maps business source.

    NOTE:
    Replace this later with real scraping or API.
    """

    def search(self, query: str) -> List[Lead]:
        """
        Returns a list of businesses for a given search query.

        Args:
            query (str): Search term (e.g., "plumbers phoenix").

        Returns:
            List[Lead]: List of discovered leads.
        """
        # TEMP: Replace with real logic later
        return [
            Lead(name="Mike's Plumbing", company="Mike's Plumbing"),
            Lead(name="Desert HVAC Co", company="Desert HVAC Co"),
        ]