import os
from datetime import datetime

import pandas as pd
from typing import List, Set

from src.models.lead import Lead


class LeadRepository:
    """
    Handles storing and retrieving leads from disk.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        # Make sure parent directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

    def load_existing_companies(self) -> Set[str]:
        """
        Loads existing company names to prevent duplicates.

        Returns:
            Set[str]: Set of company names.
        """
        if not os.path.exists(self.filepath):
            return set()

        df = pd.read_excel(self.filepath, engine='openpyxl')
        return set(df["Company"].str.lower())

    def save(self, leads: List[Lead]) -> None:
        """
        Appends new leads to the Excel file.

        Args:
            leads (List[Lead]): Leads to save.
        """
        new_data = pd.DataFrame([
            {
                "Name": l.name,
                "Company": l.company,
                "Website": l.website,
                "Email": l.email,
                "Phone": l.phone,
                "LinkedIn": l.linkedin_url,
                "Source": l.source,
                "Industry": l.industry,
                "Date Added": l.date_added or datetime.now(),
            }
            for l in leads
        ])

        if os.path.exists(self.filepath):
            existing = pd.read_excel(self.filepath, engine='openpyxl')
            combined = pd.concat([existing, new_data], ignore_index=True)
        else:
            combined = new_data

        # Save to Excel
        combined.to_excel(self.filepath, index=False, engine='openpyxl')