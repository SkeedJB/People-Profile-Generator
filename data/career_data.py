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

    CAREER_PATHS = {
        "Computer Science": {
            "entry_level": ["Software Engineer", "Data Scientist", "Machine Learning Engineer"],
            "mid_level": ["Senior Software Engineer", "Data Analyst", "Machine Learning Scientist"],
            "senior_level": ["Lead Software Engineer", "Data Manager", "Machine Learning Manager"],
            "executive_level": ["Chief Technology Officer", "Chief Data Officer", "Chief Machine Learning Officer"],
            "min_education": "Bachelors"
        },
        "Business": {
            "entry_level": ["Business Analyst", "Financial Analyst", "Operations Manager"],
            "mid_level": ["Senior Business Analyst", "Financial Manager", "Operations Director"],
            "senior_level": ["Lead Business Analyst", "Financial Director", "Operations Vice President"],
            "executive_level": ["Chief Business Officer", "Chief Financial Officer", "Chief Operations Officer"],
            "min_education": "Bachelors"
        },
        "Psychology": {
            "entry_level": ["Psychologist", "Clinical Psychologist", "Educational Psychologist"],
            "mid_level": ["Senior Psychologist", "Clinical Psychologist", "Educational Psychologist"],
            "senior_level": ["Lead Psychologist", "Clinical Psychologist", "Educational Psychologist"],
            "executive_level": ["Chief Psychologist", "Clinical Psychologist", "Educational Psychologist"],
            "min_education": "Masters"
        },
        "Graphic Design": {
            "entry_level": ["Graphic Designer", "UI/UX Designer", "Visual Designer"],
            "mid_level": ["Senior Graphic Designer", "UI/UX Designer", "Visual Designer"],
            "senior_level": ["Lead Graphic Designer", "UI/UX Designer", "Visual Designer"],
            "executive_level": ["Chief Graphic Designer", "UI/UX Designer", "Visual Designer"],
            "min_education": "Associates"
        },
        "Accounting": {
            "entry_level": ["Accountant", "Bookkeeper", "Tax Preparer"],
            "mid_level": ["Financial Analyst", "Cost Accountant", "Auditor"],
            "senior_level": ["Lead Accountant", "Financial Manager", "Auditor"],
            "executive_level": ["Chief Accountant", "Financial Manager", "Auditor"],
            "min_education": "Bachelors"
        },
        "Economics": {
            "entry_level": ["Economist", "Financial Analyst", "Market Researcher"],
            "mid_level": ["Senior Economist", "Financial Analyst", "Market Researcher"],
            "senior_level": ["Lead Economist", "Financial Analyst", "Market Researcher"],
            "executive_level": ["Chief Economist", "Financial Analyst", "Market Researcher"],
            "min_education": "Bachelors"
        },
        "Political Science": {
            "entry_level": ["Political Analyst", "Policy Researcher", "Public Relations Specialist"],
            "mid_level": ["Senior Political Analyst", "Policy Researcher", "Public Relations Specialist"],
            "senior_level": ["Lead Political Analyst", "Policy Researcher", "Public Relations Specialist"],
            "executive_level": ["Chief Political Analyst", "Policy Researcher", "Public Relations Specialist"],
            "min_education": "Bachelors"
        },
        "International Relations": {
            "entry_level": ["Diplomat", "International Relations Specialist", "Foreign Policy Analyst"],
            "mid_level": ["Senior Diplomat", "International Relations Specialist", "Foreign Policy Analyst"],
            "senior_level": ["Lead Diplomat", "International Relations Specialist", "Foreign Policy Analyst"],
            "executive_level": ["Chief Diplomat", "International Relations Specialist", "Foreign Policy Analyst"],
            "min_education": "Bachelors"
        }
    }