from typing import Dict, List, Optional
import random

class CareerData:
    EDUCATION_TO_CAREER_LEVEL = {
        "Not in school yet": "none",
        "Elementary School": "none",
        "Middle School": "none",
        "High School": "entry_level",
        "Associates": "entry_level",
        "Bachelors": "mid_level",
        "Masters": "senior_level",
        "Doctorate": "executive_level"
    }