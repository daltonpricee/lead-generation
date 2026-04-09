from dataclasses import dataclass
from typing import Optional


@dataclass
class Lead:
    """
    Represents a single business lead.

    Attributes:
        name (str): Contact name.
        company (str): Company name.
        website (Optional[str]): Company website URL.
        email (Optional[str]): Extracted or enriched email.
        phone (Optional[str]): Extracted phone number.
        linkedin_url (Optional[str]): LinkedIn profile or company page.
        source (Optional[str]): Lead source (Google Maps, Thumbtack, etc.).
        industry (Optional[str]): Business industry tag.
        date_added (Optional[str]): Date the lead was discovered.
    """
    name: str
    company: str
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    source: Optional[str] = None
    industry: Optional[str] = None
    date_added: Optional[str] = None