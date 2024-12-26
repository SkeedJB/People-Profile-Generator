import random
import asyncio
from datetime import datetime
from deep_translator import GoogleTranslator
from profiles.data.country_data import COUNTRIES, COUNTRY_LOCALES
from profiles.data.person_data import profile_data
from profiles.generation.gen_education import EducationProfile
from profiles.generation.gen_career import CareerGenerator
from profiles.generation.global_faker import get_faker
import uuid

class PersonProfile:
    """
    Represents a single person. Provides async methods to fetch name
    and address (with translation if necessary).
    """
    def __init__(self, filters=None):
        """
        Initialize PersonProfile with optional filters, e.g.:
        {
            'country': 'USA',
            'gender': 'female',
            'age_range': (25, 35),
            'education_level': 'Bachelor'
        }
        """
        self.filters = filters if filters else {}
        self.country = None
        self.country_code = None
        self.gender = None
        self.age = None
        self.birth_year = None

        self.first_name = None
        self.last_name = None
        self.full_name = None
        self.full_name_romanized = None
        self.address = None

        self.education_profile = {}
        self.career_profile = {}

    async def async_translate(self, text):
        """
        Helper for doing I/O-bound translation asynchronously.
        Includes error handling and retries.
        """
        try:
            translator = GoogleTranslator(source='auto', target='en')
            # Add retry logic and better error handling
            for _ in range(3):  # Try up to 3 times
                try:
                    return await asyncio.to_thread(translator.translate, text)
                except Exception as e:
                    await asyncio.sleep(1)  # Wait before retry
            # If all retries fail, return original text
            return text
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Fallback to original text if translation fails

    def is_ascii(self, s: str) -> bool:
        return all(ord(c) < 128 for c in s)

    def set_country(self):
        """
        Sets self.country to either a user-chosen country (if 'country' in filters)
        or picks randomly from list of COUNTRIES. Also sets self.country_code.
        """
        if 'country' in self.filters and self.filters['country'] != 'All':
            self.country = self.filters['country']
        else:
            self.country = random.choice(COUNTRIES)
        self.country_code = COUNTRY_LOCALES[self.country]

    async def get_address(self):
        """
        Gets a random address (via faker) and translates it to ASCII if necessary.
        """
        try:
            fake = get_faker(self.country_code)
            addr = fake.unique.address().replace('\n', ' ')
            if not self.is_ascii(addr):
                translated = await self.async_translate(addr)
                self.address = translated if translated else addr
            else:
                self.address = addr
        except Exception as e:
            print(f"Address generation error: {e}")
            self.address = "Address generation failed"

    async def get_name(self):
        """
        Generates first_name, last_name (via faker) and sets both self.full_name
        and self.full_name_romanized (translated if needed).
        """
        try:
            fake = get_faker(self.country_code)
            if self.gender == "male":
                self.first_name = fake.unique.first_name_male()
            else:
                self.first_name = fake.unique.first_name_female()
            self.last_name = fake.unique.last_name()

            full_name_local = f"{self.first_name} {self.last_name}"
            self.full_name = full_name_local
            self.full_name_romanized = full_name_local

            # Translate if it contains non-latin characters
            if not self.is_ascii(full_name_local):
                translated = await self.async_translate(full_name_local)
                self.full_name_romanized = translated if translated else full_name_local
        except Exception as e:
            print(f"Name generation error: {e}")
            self.first_name = "John"
            self.last_name = "Doe"
            self.full_name = "John Doe"
            self.full_name_romanized = "John Doe"

    def set_gender(self):
        """
        Sets self.gender to either a user-chosen gender or picks randomly.
        """
        if 'gender' in self.filters and self.filters['gender'] != 'All':
            self.gender = self.filters['gender']
        else:
            self.gender = random.choice(profile_data["sex"])

    def set_birth_year_and_age(self):
        """
        Randomly sets birth year (based on either an 'age_range' in filters
        or defaulting to profile_data) and calculates age.
        """
        year_now = datetime.now().year
        if 'age_range' in self.filters and isinstance(self.filters['age_range'], tuple):
            min_age, max_age = self.filters['age_range']
            self.birth_year = year_now - random.randint(min_age, max_age)
        else:
            # fallback to default
            self.birth_year = random.randint(profile_data["birth_range"][0], profile_data["birth_range"][1])
        self.age = year_now - self.birth_year

    def build_education_profile(self):
        """
        Builds an EducationProfile, sets it in self.education_profile.
        """
        education_filters = {}
        if self.filters.get('education_level') and self.filters['education_level'] != 'All':
            education_filters['education_level'] = self.filters['education_level']
        if self.filters.get('major_field'):
            education_filters['major_field'] = self.filters['major_field']

        edu = EducationProfile(age=self.age, filters=education_filters)
        level = edu.get_education_level()
        history = edu.generate_education_history()
        major = edu.get_major()

        self.education_profile = {
            "education_level": level,
            "education_history": history,
            "major_field": major
        }

    def build_career_profile(self):
        """
        Builds a CareerGenerator, sets it in self.career_profile.
        """
        career_generator = CareerGenerator()
        career_info = career_generator.generate_career_history(
            age=self.age,
            education_history=self.education_profile["education_history"]
        )
        
        # If no career was found, default data:
        if career_info['career'] is None:
            career_info['career'] = {
                "position": "Unemployed",
                "company": "N/A",
                "company_id": None,
                "department": "N/A",
                "salary": "N/A",
                "years_experience": 0
            }

        self.career_profile = {
            "career_history": career_info['career_history'],
            "career": career_info['career'],
            "job_title": career_info['career'].get('position', 'N/A'),
            "company": career_info['career'].get('company', 'N/A'),
            "company_id": career_info['career'].get('company_id'),
            "department": career_info['career'].get('department', 'N/A'),
            "years_experience": career_info['career'].get('years_experience', 0)
        }

    def _generate_career_entry(self, start_year, duration):
        """Generate a single career entry with a valid business UUID"""
        company_name = self.faker.company()
        # Generate a deterministic UUID for the company based on its name
        company_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, company_name))
        
        return {
            'position': self.faker.job(),
            'company': company_name,
            'company_id': company_id,  # Add UUID for company
            'department': self.faker.department(),
            'level': random.choice(self.career_levels),
            'field': random.choice(self.career_fields),
            'salary': f"${random.randint(30000, 150000):,}/year",
            'start_year': start_year,
            'end_year': start_year + duration,
            'duration': duration
        }

    def _generate_career_history(self):
        """Generate career history with consistent company IDs"""
        career_history = []
        current_year = self.current_year
        remaining_years = self.work_years

        while remaining_years > 0:
            duration = min(random.randint(1, 5), remaining_years)
            start_year = current_year - remaining_years
            
            career_entry = self._generate_career_entry(start_year, duration)
            career_history.append(career_entry)
            
            remaining_years -= duration

        # Sort career history by start_year in descending order
        career_history.sort(key=lambda x: x['start_year'], reverse=True)
        return career_history

    def _generate_current_career(self):
        """Generate current career with valid business UUID"""
        if random.random() < 0.9:  # 90% chance of being employed
            company_name = self.faker.company()
            # Generate a deterministic UUID for the company based on its name
            company_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, company_name))
            
            return {
                'position': self.faker.job(),
                'company': company_name,
                'company_id': company_id,  # Add UUID for company
                'department': self.faker.department(),
                'salary': f"${random.randint(30000, 150000):,}/year"
            }
        return None

    async def generate_person_profile(self):
        """
        Master async method to fill out entire profile.
        Includes better error handling and ensures all required fields are set.
        """
        try:
            # Set basic info first
            self.set_country()
            self.set_gender()
            self.set_birth_year_and_age()

            # Generate name and address concurrently with error handling
            await asyncio.gather(
                self.get_name(),
                self.get_address()
            )

            # Verify critical fields are set
            if not all([self.full_name, self.address, self.country, self.gender, self.age]):
                raise ValueError("Critical profile information is missing")

            # Build education/career
            self.build_education_profile()
            self.build_career_profile()

        except Exception as e:
            print(f"Profile generation error: {e}")
            # Set fallback values for critical fields
            if not self.full_name:
                self.full_name = "John Doe"
                self.full_name_romanized = "John Doe"
            if not self.address:
                self.address = "Unknown Address"
            if not self.country:
                self.country = "United States"
                self.country_code = "en_US"
            if not self.gender:
                self.gender = "male"
            if not self.age:
                self.age = 30
                self.birth_year = datetime.now().year - 30