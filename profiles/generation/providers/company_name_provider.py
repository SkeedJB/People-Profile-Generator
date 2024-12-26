"""
File: generation/providers/company_name_provider.py

Provides a custom Faker provider that generates unique,
sector-specific company names. To add or modify sectors,
update the SECTOR_PATTERNS dictionary.
"""

from faker.providers import BaseProvider
import random

class CompanyNameProvider(BaseProvider):
    # Stores already generated names to ensure uniqueness
    used_company_names = set()

    # Define your patterns and variables for various sectors
    SECTOR_PATTERNS = {
        "Tech": [
            # Patterns: e.g., {prefix} {core} {suffix}
            ("Tech", "Nova", "Solutions"),
            ("Cyber", "Peak", "Systems"),
            ("Data", "Logic", "Labs"),
            ("Cloud", "Sync", "Corporation"),
            ("Net", "Horizon", "Innovations"),
            ("Open", "Source", "AI"),
        ],
        "Finance": [
            ("Fin", "Core", "Holdings"),
            ("Capital", "Vantage", "Group"),
            ("Money", "Line", "Partners"),
            ("Prime", "Ledger", "Advisors"),
        ],
        "Healthcare": [
            ("Medi", "Sphere", "Clinics"),
            ("Health", "Guard", "Associates"),
            ("Well", "Point", "Care"),
            ("Bio", "Life", "Research"),
            ("Care", "Plus", "Centers"),
        ],
        "Business": [
            ("Global", "Biz", "Resources"),
            ("Venture", "Edge", "Enterprises"),
            ("Enterprise", "Quest", "Ltd"),
            ("Corp", "Scope", "Consulting"),
        ],
        "Education": [
            ("Edu", "Wise", "Academy"),
            ("Learn", "Bridge", "Institute"),
            ("Mentor", "Path", "Group"),
            ("NextGen", "Scholars", "Lab"),
        ],
        "Law": [
            ("Lex", "Shield", "Legal"),
            ("Justice", "Link", "Attorneys"),
            ("Law", "Matrix", "Group"),
            ("Legal", "Focus", "Advisors"),
        ],
        "General": [
            ("Alpha", "Sync", "Group"),
            ("Iron", "Stone", "Enterprises"),
            ("Royal", "Crest", "Industries"),
            ("Star", "Way", "Holdings"),
        ],
    }

    # Optional sector mappings, if your domain differs from the sector name
    DOMAIN_SECTOR_MAP = {
        "Engineering": "Tech",
        "Computer Science": "Tech",
        "Medicine": "Healthcare",
        "Business": "Business",
        "Education": "Education",
        "Law": "Law",
        "Psychology": "Healthcare",
        "Marketing": "Business",
        "Accounting": "Finance",
        "Information Technology": "Tech",
        "Pharmacy": "Healthcare",
        "Literature": "General",
        "Science": "General",
    }

    def company_name(self, sector: str = "General") -> str:
        """
        Generate a unique company name for the given sector.
        Falls back to 'General' sector if not found.
        """
        if sector not in self.SECTOR_PATTERNS:
            sector = "General"

        patterns = self.SECTOR_PATTERNS[sector]
        # Attempt to generate a unique name
        for _ in range(1000):  # Arbitrary limit to avoid infinite loops
            prefix, core, suffix = random.choice(patterns)
            name = f"{prefix}{core} {suffix}"
            if name not in self.used_company_names:
                self.used_company_names.add(name)
                return name

        # Fallback in case we can't generate a unique name
        return self.generator.company()  # Use the standard Faker fallback if needed 