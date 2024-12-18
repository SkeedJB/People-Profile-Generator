from data.career_data import CareerData
from faker import Faker
from typing import Dict, List, Optional
import random

class CareerGenerator:
    ROLE_PREFIXES = {
        "entry_level": ["Junior", "Assistant", "Trainee", "Apprentice", "New Grad"],
        "mid_level": ["", "Lead", "Manager", "Supervisor"],
        "senior_level": ["Head of", "Senior", "Principal", "Director of", "Chief"],
        "executive_level": ["Chief", "Executive", "Director", "Vice President of", "President"]
    }

    ROLE_DOMAINS = {
        'No College Degree': [
            ('Salesperson', 'Technician', 'Customer Service', 'Receptionist', 'Cashier'),
            ('Retail', 'Sales', 'Customer Service'),
            ('Reception', 'Cashier', 'Unemployed'),
        ],
        'Computer Science': [
            ('Developer', 'Engineering', 'Technology'),
            ('Software', 'Systems', 'Data', 'Cloud', 'Security'),
            ('Development', 'Architecture', 'Operations', 'Infrastructure')
        ],
        'Business': [
            ('Manager', 'Analyst', 'Consultant', 'Strategist'),
            ('Business', 'Operations', 'Strategy', 'Sales'),
            ('Development', 'Operations', 'Growth', 'Transformation')
        ],
        'Psychology': [
            ('Counselor', 'Therapist', 'Psychologist', 'Researcher'),
            ('Clinical', 'Behavioral', 'Cognitive', 'Research'),
            ('Psychology', 'Health', 'Wellness', 'Development')
        ],
        'Graphic Design': [
            ('Designer', 'Art Director', 'Creative Director', 'Visual Designer'),
            ('Graphic', 'UI/UX', 'Visual', 'Branding', 'Illustration'),
            ('Design', 'Illustration', 'Branding', 'Packaging', 'Print')
        ],
        'Accounting': [
            ('Accountant', 'Bookkeeper', 'Auditor', 'Tax Preparer'),
            ('Financial', 'Cost', 'Audit', 'Tax'),
            ('Director', 'Vice President', 'Chief')
        ],
        'Economics': [
            ('Economist', 'Financial Analyst', 'Market Researcher', 'Policy Analyst'),
            ('Head', 'Financial', 'Lead', 'Policy'),
            ('Analysis', 'Research', 'Forecasting', 'Consulting')
        ],
        'Political Science': [
            ('Political Analyst', 'Policy Researcher', 'Public Relations Specialist', 'Strategist'),
            ('Political', 'Policy', 'Public', 'Strategic'),
            ('Analysis', 'Research', 'Consulting', 'Strategic')
        ],
        'International Relations': [
            ('Diplomat', 'International Relations Specialist', 'Foreign Policy Analyst', 'Strategist'),
            ('Diplomatic', 'International', 'Foreign', 'Strategic'),
            ('Relations', 'Policy', 'Consulting', 'Strategic')
        ]
    }

    DEPARTMENT_SUFFIXES = [
        "Department", 
        "Division",  
        "Section", 
        "Team", 
        "Group", 
        "Office", 
        "Service",
    ]


    def __init__(self, seed=None):
        self.faker = Faker(seed=seed)
        if seed:
            Faker.seed(seed)
            random.seed(seed)

    def _generate_position_title(self, level: str, domain: str) -> str:
        if level == "none" or domain not in self.ROLE_DOMAINS:
            return "Unemployed"
        
        prefix = random.choice(self.ROLE_PREFIXES[level])
        domain_parts = self.ROLE_DOMAINS[domain]
        
        components = [random.choice(part) for part in domain_parts]
        if level == "executive_level":
            if random.random() < 0.3:
                return f"Chief {components[0]} Officer"
            
        if prefix:
            patterns = [
                f"{prefix} {components[0]}",
                f"{prefix} {components[1]} {components[0]}",
                f"{prefix} {components[2]} {components[0]}"
            ]
        else:
            patterns = [
                f"{components[1]} {components[0]}",
                f"{components[2]} {components[0]}",
                f"{components[1]} {components[2]} {components[0]}"
            ]
        
        return random.choice(patterns)
               
    def _get_career_level(self, age: int, education_level: str) -> str:
        """Determine career level based on age and education"""
        if age < 18 or education_level in ["Not in school yet", "Elementary School", "Middle School"]:
            return "none"

        years_experience = age - 18
        education_weights = {
            "High School": {"entry_level": 0.9, "mid_level": 0.1},
            "Associates": {"entry_level": 0.7, "mid_level": 0.3},
            "Bachelors": {"entry_level": 0.3, "mid_level": 0.5, "senior_level": 0.2},
            "Masters": {"mid_level": 0.4, "senior_level": 0.5, "executive_level": 0.1},
            "Doctorate": {"senior_level": 0.6, "executive_level": 0.4}
        }

        if education_level not in education_weights:
            return "none"

        # Adjust weights based on years of experience
        weights = education_weights[education_level].copy()
        if years_experience > 15:
            weights["executive_level"] = weights.get("executive_level", 0) + 0.3
        elif years_experience > 10:
            weights["senior_level"] = weights.get("senior_level", 0) + 0.3
        elif years_experience > 5:
            weights["mid_level"] = weights.get("mid_level", 0) + 0.2

        # Normalize weights
        total = sum(weights.values())
        weights = {k: v/total for k, v in weights.items()}

        return random.choices(list(weights.keys()), list(weights.values()))[0]

    def generate_career(self, age: int, education_level: str, major: str) -> Optional[Dict]:
        """Generate a complete career profile"""
        level = self._get_career_level(age, education_level)
        if level == "none":
            return None

        position = self._generate_position_title(level, major)
        company_name = self.faker.company()
        
        career = {
            "position": position,
            "company": company_name,
            "level": level,
            "field": major,
            "years_experience": max(0, age - 18),
            "department": f"{random.choice(self.ROLE_DOMAINS[major][1])} {random.choice(self.DEPARTMENT_SUFFIXES)}",
        }

        # Optional: Add company industry, size, etc. using Faker
        if random.random() < 0.3:  # 30% chance to be remote
            career["location"] = "Remote"
        else:
            career["location"] = self.faker.city()

        return career

    def generate_career_history(self, age: int, education_level: str, major: str) -> List[Dict]:
        """Generate a person's career history"""
        if age < 18:
            return []

        years_working = age - 18
        num_jobs = min(1 + years_working // 3, 5)  # Average job change every 3 years, max 5 jobs
        
        history = []
        remaining_years = years_working
        
        for i in range(num_jobs):
            job_length = min(
                random.randint(1, 5) if i < num_jobs - 1 else remaining_years,
                remaining_years
            )
            
            career = self.generate_career(
                age=age - (years_working - remaining_years),
                education_level=education_level,
                major=major
            )
            
            if career:
                career["duration"] = job_length
                career["start_year"] = 2024 - remaining_years
                career["end_year"] = career["start_year"] + job_length
                history.append(career)
            
            remaining_years -= job_length