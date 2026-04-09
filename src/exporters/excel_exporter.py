import pandas as pd
from typing import List

from src.models.lead import Lead


class ExcelExporter:
    """
    Exports leads to an Excel file.
    """

    def export(self, leads: List[Lead], filepath: str) -> None:
        """
        Writes leads to an Excel file.

        Args:
            leads (List[Lead]): List of leads.
            filepath (str): Output file path.
        """
        data = [
            {
                "Name": lead.name,
                "Company": lead.company,
                "Website": lead.website,
                "Email": lead.email,
                "Phone": lead.phone,
                "LinkedIn": lead.linkedin_url,
                "Source": lead.source,
                "Industry": lead.industry,
                "Date Added": lead.date_added,
            }
            for lead in leads
        ]

        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)