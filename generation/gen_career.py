from faker import Faker
from typing import Dict, List, Optional
import random
from datetime import datetime
from countryinfo import CountryInfo
import pycountry

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

    def __init__(self, seed=None):
        self.faker = Faker()
        if seed:
            Faker.seed(seed)
            random.seed(seed)
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

    def generate_career_history(self, education_history: List[Dict], age: int) -> Dict:
        """Generate career history based on education timeline"""
        if not education_history or age < 18:
            return {
                'career_history': [],
                'career': None
            }

        history = []

        # Find the latest education completion
        latest_education = max(
            (edu for edu in education_history if not edu["is_current"]), 
            key=lambda x: x["end_year"],
            default=None
        )
        if not latest_education:
            return {
                'career_history': [],
                'career': None
            }

        career_start_year = latest_education["end_year"]
        years_working = self.current_year - career_start_year

        if years_working <= 0:
            return {
                'career_history': [],
                'career': None
            }

        # Determine number of job changes
        max_jobs = max(1, min(5, years_working // 2))  # Atleast 1 job, maximum 5 jobs, minimum 2 years per job
        num_jobs = random.randint(1, max_jobs)

        remaining_years = years_working
        current_domain = latest_education.get("major", random.choice(list(self.ROLE_DOMAINS.keys())))

        for i in range(num_jobs):
            # Determine job duration
            if i == num_jobs - 1:  # Last job extends to present
                job_length = remaining_years
            else:
                job_length = min(
                    random.randint(2, 5),
                    remaining_years - (num_jobs - i - 1) * 2  # Ensure at least 2 years for remaining jobs
                )

            # Calculate years of experience at this point
            years_experience = years_working - remaining_years

            # Possibility of career switch
            if self._can_switch_careers(latest_education["level"]):
                current_domain = random.choice(list(self.ROLE_DOMAINS.keys()))

            # Generate job entry
            level = self._get_career_level(years_experience, latest_education["level"])

            job = {
                "position": self._generate_position_title(level, current_domain),
                "company": self.faker.company(),
                "field": current_domain,
                "level": level,
                "start_year": career_start_year + (years_working - remaining_years),
                "end_year": career_start_year + (years_working - remaining_years) + job_length,
                "duration": job_length,
            }

            history.append(job)
            remaining_years -= job_length

        for job in history:
            job['department'] = self._generate_department(job['field'])

        return {
            'career_history': history,
            'career': history[-1] if history else None  # Current job is last in history
        }

    def get_current_career(self, career_history: List[Dict]) -> Optional[Dict]:
        """Get the current career position from history"""
        return career_history[-1] if career_history else None
