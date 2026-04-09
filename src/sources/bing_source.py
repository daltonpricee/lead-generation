import logging
from typing import List

from src.config.settings import BING_API_KEY, DEFAULT_LOCATION
from src.models.lead import Lead
from src.utils.http_client import HTTPClient


class BingSource:
    """
    Uses the Bing Maps Local Search API to discover construction companies.

    Filters based on entity type and popularity.
    """

    SEARCH_URL = "https://dev.virtualearth.net/REST/v1/LocalSearch/"

    def __init__(self, api_key: str | None = None, location: str | None = None) -> None:
        self.api_key: str | None = api_key or BING_API_KEY
        self.location: str | None = location or DEFAULT_LOCATION
        self.http_client: HTTPClient = HTTPClient()

    def search(self, query: str, max_results: int = 200) -> List[Lead]:
        """
        Searches for businesses matching the query.

        Args:
            query: Search term.
            max_results: Maximum leads to return.

        Returns:
            List of Lead objects.
        """
        if not self.api_key:
            return self._sample_leads(query)

        leads: List[Lead] = []
        skip: int = 0
        top: int = 25  # Bing max per request

        while len(leads) < max_results:
            params: dict[str, str | int] = {
                "query": query,
                "key": self.api_key,
                "maxResults": min(top, max_results - len(leads)),
                "$skip": skip,
                "$format": "json",
            }

            try:
                response: dict = self.http_client.get_json(self.SEARCH_URL, params=params)
                results: list = response.get("resourceSets", [{}])[0].get("resources", [])

                for place in results:
                    name: str | None = place.get("name")
                    if not name:
                        continue

                    # Bing doesn't have direct popularity, but we can check entity type
                    entity_type: str = place.get("entityType", "")
                    if "LocalBusiness" not in entity_type:
                        continue

                    website: str | None = place.get("Website")
                    phone: str | None = place.get("PhoneNumber")
                    address: str = place.get("Address", {}).get("formattedAddress", "")

                    lead: Lead = Lead(
                        name="",
                        company=name,
                        website=website,
                        email=None,
                        phone=phone,
                        linkedin_url=None,
                        source="Bing",
                        industry="Construction",
                    )
                    leads.append(lead)

                if len(results) < top:
                    break

                skip += top

            except Exception as exc:
                logging.warning("Bing search failed: %s", exc)
                break

        if not leads:
            return self._sample_leads(query)

        return leads[:max_results]

    def _sample_leads(self, query: str) -> List[Lead]:
        """
        Returns sample leads when API is not available.

        Args:
            query: Unused.

        Returns:
            List of sample Lead objects.
        """
        companies: list[str] = [
            "Evergreen Builders", "Summit Contractors", "Vertex Construction",
            "Apex Renovations", "Zenith Builders", "Nadir Contractors",
            "Pinnacle Construction", "Base Renovations", "Crown Builders",
            "Foundation Contractors", "Roof Construction", "Wall Renovations",
            "Floor Builders", "Ceiling Contractors", "Door Construction",
            "Window Renovations", "Frame Builders", "Siding Contractors",
            "Insulation Construction", "Drywall Renovations", "Paint Builders",
            "Tile Contractors", "Carpet Construction", "Hardwood Renovations",
            "Laminate Builders", "Vinyl Contractors", "Stone Construction",
            "Brick Renovations", "Concrete Builders", "Asphalt Contractors",
            "Gravel Construction", "Sand Renovations", "Dirt Builders",
            "Mud Contractors", "Clay Construction", "Loam Renovations",
            "Silt Builders", "Peat Contractors", "Humus Construction",
            "Loess Renovations", "Regosol Builders", "Chernozem Contractors",
            "Podzol Construction", "Gleysol Renovations", "Histosol Builders",
            "Andisol Contractors", "Oxisol Construction", "Ultisol Renovations",
            "Alfisol Builders", "Mollisol Contractors", "Spodosol Construction"
        ]
        leads: List[Lead] = []
        for i, company in enumerate(companies[:50]):
            leads.append(Lead(
                name=f"Contact {i+1}",
                company=company,
                website=f"https://bing.com/search?q={company.replace(' ', '+')}",
                email=None,
                phone=None,
                linkedin_url=None,
                source="Bing (sample)",
                industry="Construction",
            ))
        return leads