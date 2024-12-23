from typing import Dict, List, Optional, Tuple
import random
from datetime import datetime

# Import your new provider
from generation.providers.company_name_provider import CompanyNameProvider

from generation.global_faker import get_faker

class CareerGenerator:
    # Role prefixes stay consistent across levels of seniority
    ROLE_PREFIXES = {
        "entry_level": ["Junior", "Assistant", "Trainee", "Apprentice", "New Grad"],
        "mid_level": ["", "Lead", "Manager", "Supervisor"],
        "senior_level": ["Head of", "Senior", "Principal", "Director of", "Chief"],
        "executive_level": ["Chief", "Executive", "Director", "Vice President of", "President"]
    }

    # Expanded ROLE_DOMAINS to match education majors
    ROLE_DOMAINS = {
        'Retail': [
            ('Sales', 'Manager', 'Assistant'),
            ('Retail', 'Store', 'Sales'),
            ('Customer', 'Service', 'Management')
        ],
        'Engineering': [
            ('Engineer', 'Developer', 'Technician'),
            ('Mechanical', 'Electrical', 'Software', 'Systems'),
            ('Engineering', 'Development', 'Operations')
        ],
        'Computer Science': [
            ('Developer', 'Engineer', 'Architect'),
            ('Software', 'Systems', 'Data', 'Cloud'),
            ('Development', 'Engineering', 'Architecture')
        ],
        'Medicine': [
            ('Doctor', 'Physician', 'Specialist'),
            ('Medical', 'Clinical', 'Research'),
            ('Medicine', 'Healthcare', 'Practice')
        ],
        'Business': [
            ('Manager', 'Analyst', 'Consultant'),
            ('Business', 'Operations', 'Strategy'),
            ('Management', 'Operations', 'Development')
        ],
        'Education': [
            ('Teacher', 'Instructor', 'Educator'),
            ('Education', 'Training', 'Learning'),
            ('Development', 'Instruction', 'Coordination')
        ],
        'Law': [
            ('Lawyer', 'Attorney', 'Counsel'),
            ('Legal', 'Corporate', 'Patent'),
            ('Law', 'Litigation', 'Compliance')
        ],
        'Psychology': [
            ('Psychologist', 'Counselor', 'Therapist'),
            ('Clinical', 'Organizational', 'Research'),
            ('Psychology', 'Counseling', 'Therapy')
        ],
        'Marketing': [
            ('Marketer', 'Strategist', 'Manager'),
            ('Digital', 'Brand', 'Product'),
            ('Marketing', 'Communications', 'Strategy')
        ],
        'Accounting': [
            ('Accountant', 'Auditor', 'Controller'),
            ('Financial', 'Tax', 'Corporate'),
            ('Accounting', 'Finance', 'Compliance')
        ],
        'Information Technology': [
            ('Developer', 'Administrator', 'Engineer'),
            ('IT', 'Systems', 'Network'),
            ('Development', 'Administration', 'Support')
        ],
        'Pharmacy': [
            ('Pharmacist', 'Researcher', 'Specialist'),
            ('Clinical', 'Research', 'Retail'),
            ('Pharmacy', 'Healthcare', 'Development')
        ],
        'Literature': [
            ('Writer', 'Editor', 'Researcher'),
            ('Content', 'Technical', 'Creative'),
            ('Writing', 'Publishing', 'Communications')
        ],
        'Science': [
            ('Scientist', 'Researcher', 'Analyst'),
            ('Research', 'Laboratory', 'Data'),
            ('Science', 'Research', 'Development')
        ]
    }

    def salary_for_level(self, level: str) -> int:
        """Generate a salary for a given career level"""
        if level == "entry_level":
            salary_range = (15000, 50000)
        elif level == "mid_level":
            salary_range = (50000, 100000)
        elif level == "senior_level":
            salary_range = (100000, 200000)
        elif level == "executive_level":
            salary_range = (200000, 500000)
        return salary_range
    
    def get_salary(self, salary_range: Tuple[int, int]) -> str:
        """Generate a salary for a given career level"""
        generated_salary = random.randint(salary_range[0], salary_range[1])
        formatted_salary = f"${round(generated_salary / 1000, 1)}k USD"
        return formatted_salary

    def __init__(self, seed=None):
        self.faker = get_faker()
        # Register our custom company name provider
        self.faker.add_provider(CompanyNameProvider)

        if seed:
            self.faker.seed(seed)
            self.faker.random.seed(seed)
        self.current_year = datetime.now().year

    def _can_switch_careers(self, education_level: str) -> bool:
        """Determine if career switching is possible based on education"""
        switch_probabilities = {
            "High School": 0.1,
            "Associates": 0.2,
            "Bachelors": 0.3,
            "Masters": 0.4,
            "Doctorate": 0.5
        }
        return random.random() < switch_probabilities.get(education_level, 0)

    def _get_career_level(self, years_experience: int, education_level: str) -> str:
        """Determine career level based on experience and education"""
        if education_level == "High School":
            if years_experience < 5:
                return "entry_level"
            elif years_experience < 10:
                return "mid_level"
            return "senior_level"
        
        if education_level in ["Associates", "Bachelors"]:
            if years_experience < 3:
                return "entry_level"
            elif years_experience < 8:
                return "mid_level"
            elif years_experience < 15:
                return "senior_level"
            return "executive_level"
        
        if education_level in ["Masters", "Doctorate"]:
            if years_experience < 2:
                return "entry_level"
            elif years_experience < 5:
                return "mid_level"
            elif years_experience < 10:
                return "senior_level"
            return "executive_level"
        
        return "entry_level"

    def _generate_department(self, field: str) -> str:
        departments = {
            "Retail": ["Sales", "Customer Service", "Inventory Management", "Merchandising", "Marketing", "Store Management"],
            "Engineering": ["Research and Development", "Quality Control", "Production", "Maintenance", "Safety", "Environmental"],
            "Computer Science": ["Software Development", "Data Science", "Cybersecurity", "AI and Machine Learning", "Web Development", "Mobile Development"],
            "Medicine": ["Clinical", "Research", "Pharmaceutical", "Healthcare", "Public Health"],
            "Business": ["Sales", "Marketing", "Operations", "Finance", "Human Resources", "Legal", "Customer Service"],
            "Education": ["Teaching", "Administration", "Curriculum Development", "Student Services", "Research"],
            "Law": ["Litigation", "Corporate", "Intellectual Property", "Real Estate", "Tax"],
            "Psychology": ["Clinical", "Organizational", "Research", "Forensic", "Educational"],
            "Marketing": ["Digital Marketing", "Brand Management", "Product Marketing", "Advertising", "Market Research"],
            "Accounting": ["Audit", "Tax", "Financial Planning", "Risk Management", "Compliance"],
            "Information Technology": ["Software Development", "Network Administration", "Cybersecurity", "Data Analytics", "Cloud Computing"],
            "Pharmacy": ["Clinical", "Pharmaceutical", "Research", "Retail", "Public Health"],
            "Literature": ["Creative Writing", "Editing", "Publishing", "Literature Review", "Literary Criticism"],
            "Science": ["Laboratory", "Research", "Data Analysis", "Scientific Writing", "Scientific Communication"]
        }
        return random.choice(departments.get(field, ["General"]))

    def _generate_position_title(self, level: str, domain: str) -> str:
        """Generate a position title based on level and domain"""
        if domain not in self.ROLE_DOMAINS:
            # Handle career switchers or undefined domains
            domain = random.choice(list(self.ROLE_DOMAINS.keys()))
        
        prefix = random.choice(self.ROLE_PREFIXES[level])
        domain_parts = self.ROLE_DOMAINS[domain]
        
        if level == "executive_level" and random.random() < 0.3:
            return f"Chief {random.choice(domain_parts[0])} Officer"
        
        components = [random.choice(part) for part in domain_parts]
        return f"{prefix} {components[1]} {components[0]}" if prefix else f"{components[1]} {components[0]}"

    def _generate_company_name(self, domain: str) -> str:
        """
        Generate a sector-specific company name by mapping the domain to a sector
        and calling the Faker provider's company_name method.
        """
        # Use the domain-sector mapping from the provider
        from generation.providers.company_name_provider import CompanyNameProvider
        sector = CompanyNameProvider.DOMAIN_SECTOR_MAP.get(domain, "General")
        return self.faker.company_name(sector=sector)

    def generate_career_history(self, education_history: List[Dict], age: int) -> Dict:
        """
        Generate career history based primarily on age, allowing for concurrent education and work.
        Minimum working age is 16.
        """
        if age < 16:  # Too young to work
            return {
                'career_history': [],
                'career': None
            }

        # Calculate total possible working years (from age 16)
        years_working = age - 16
        if years_working <= 0:
            return {
                'career_history': [],
                'career': None
            }

        history = []

        # Get the highest completed or in-progress education
        latest_education = max(education_history, 
                             key=lambda e: e["start_year"] if isinstance(e["start_year"], int) else 0, 
                             default=None)

        # Determine starting domain based on education or random choice
        current_domain = None
        if latest_education:
            current_domain = latest_education.get("field_of_study")
        if not current_domain or current_domain == "General":
            current_domain = random.choice(list(self.ROLE_DOMAINS.keys()))

        # Calculate career start at age 16 or education start, whichever is later
        career_start_year = self.current_year - years_working

        # number of jobs can be up to ~1 job per 1.5 years, 1..7
        max_jobs = max(1, min(7, int(years_working // 1.5)))
        num_jobs = random.randint(1, max_jobs)

        remaining_years = years_working

        for i in range(num_jobs):
            # 20% chance of an unemployment gap if not first job
            if i > 0 and random.random() < 0.2:
                gap_length = random.randint(1, 2)
                if remaining_years - gap_length <= 0:
                    break
                start_gap = career_start_year + (years_working - remaining_years)
                end_gap = start_gap + gap_length
                history.append({
                    "position": "Unemployed",
                    "company": None,
                    "field": None,
                    "level": "unemployed",
                    "start_year": start_gap,
                    "end_year": end_gap,
                    "duration": gap_length,
                    "salary": None,
                    "department": None
                })
                remaining_years -= gap_length

            # Determine length for the next job (1..5 years), ensuring enough time remains
            if i == num_jobs - 1:
                job_length = remaining_years
            else:
                job_length = random.randint(1, 5)
                # Ensure at least 1 year remains for subsequent positions
                job_length = min(job_length, remaining_years - (num_jobs - i - 1))

            if job_length < 1:
                break

            # Calculate experience so far (excludes the upcoming job)
            years_experience = years_working - remaining_years

            # 30% chance of switching domains if allowed
            education_level = latest_education["level"] if latest_education else "High School"
            if self._can_switch_careers(education_level) and random.random() < 0.3:
                current_domain = random.choice(list(self.ROLE_DOMAINS.keys()))

            level = self._get_career_level(years_experience, education_level)

            start_job = career_start_year + (years_working - remaining_years)
            end_job = start_job + job_length

            # For current job, if it would end after current year, set to Present
            if end_job > self.current_year:
                end_job = "Present"
                job_length = self.current_year - start_job

            job = {
                "position": self._generate_position_title(level, current_domain),
                "company": self._generate_company_name(current_domain),
                "field": current_domain,
                "level": level,
                "start_year": start_job,
                "end_year": end_job,
                "salary": self.get_salary(self.salary_for_level(level)),
                "duration": job_length,
                "department": self._generate_department(current_domain),
                "years_experience": years_experience
            }

            history.append(job)
            remaining_years -= job_length

        # Use the most recent "employed" job as "career"
        latest_job = next(
            (j for j in reversed(history) if j['level'] not in ['unemployed', 'career_break']), 
            None
        )

        # If we found a latest job, ensure it has years_experience
        if latest_job:
            latest_job['years_experience'] = years_working

        return {
            'career_history': history,
            'career': latest_job
        }

    def get_current_career(self, career_history: List[Dict]) -> Optional[Dict]:
        """Get the current career position from history"""
        return career_history[-1] if career_history else None
