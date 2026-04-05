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
    """
    name: str
    company: str
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None