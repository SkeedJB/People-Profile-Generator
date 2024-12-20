from faker import Faker
from data.person_data import profile_data
from generation.gen_education import EducationProfile
from generation.gen_career import CareerGenerator
from data.country_data import COUNTRIES, COUNTRY_LOCALES
import pandas as pd
import random
from datetime import datetime
from deep_translator import GoogleTranslator
import langdetect

class PersonProfile:
    def __init__(self, filters=None):
        """
        Initialize PersonProfile with optional filters
        filters: dict of attributes to filter by, e.g., 
        {
            'country': 'USA',
            'gender': 'female',
            'age_range': (25, 35),
            'education_level': 'Bachelor'
        }
        """
        self.filters = filters or {}

    def get_country(self):
        if 'country' in self.filters:
            self.country = self.filters['country']
        else:
            self.country = random.choice(COUNTRIES)
        self.country_code = COUNTRY_LOCALES[self.country]
        return self.country, self.country_code
    
    def get_address(self):
        fake = Faker(locale=self.country_code)
        self.address = fake.unique.address()
        self.address = self.address.replace('\n', '\n')

        # Format the address to be more readable
        if langdetect.detect(self.address) != 'en':
            translator = GoogleTranslator(source='auto', target='en')
            self.address = translator.translate(self.address)
        return self.address
    
    def get_gender(self):
        if 'gender' in self.filters:
            self.gender = self.filters['gender']
        else:
            self.gender = random.choice(profile_data["sex"])
        return self.gender

    def get_name(self, gender):
        fake = Faker(locale=self.country_code)
        if gender == "male":
            self.first_name = fake.unique.first_name_male()
        else:
            self.first_name = fake.unique.first_name_female()
        self.last_name = fake.unique.last_name()

        self.full_name = f"{self.first_name} {self.last_name}"
        self.full_name_romanized = self.full_name

        # Check if the name contains any non-ASCII characters, if so, translate it to English
        if langdetect.detect(self.full_name) != 'en':
            translator = GoogleTranslator(source='auto', target='en')
            self.full_name_romanized = translator.translate(self.full_name)

        return self.first_name, self.last_name, self.full_name_romanized

    def get_age(self):
        if 'age_range' in self.filters:
            min_age, max_age = self.filters['age_range']
            birth_year = datetime.now().year - random.randint(min_age, max_age)
        else:
            birth_year = random.randint(profile_data["birth_range"][0], profile_data["birth_range"][1])
        self.age = datetime.now().year - birth_year
        return self.age

    # Uses all the functions to generate a person profile
    def generate_person_profile(self):
        self.get_country()
        self.get_address()
        self.get_gender()
        self.get_name(self.gender)
        self.get_age()

        # Initialize EducationProfile with relevant filters
        education_filters = {
            'education_level': self.filters.get('education_level'),
            'major_field': self.filters.get('major_field')
        }
        education = EducationProfile(age=self.age, filters=education_filters)

        # Get education level
        education_level = education.get_education_level()

        # Get education history
        education_history = education.generate_education_history()

        # Combine into a dictionary
        self.education_profile = {
            "education_level": education_level,
            "education_history": education_history,
            "major_field": education.get_major()
        }

        # Generate Career Profile
        career_generator = CareerGenerator()
        career_info = career_generator.generate_career_history(
            age=self.age,
            education_history=self.education_profile["education_history"]
        )
        if career_info['career'] is None:
            career_info['career'] = {
                "position": "Unemployed",
                "company": "N/A",
                "department": "N/A",
                "location": "N/A",
                "years_experience": 0
        }
        career_info['career']['years_experience'] = 0

        self.career_profile = {
            "career_history": career_info['career_history'],
            "career": career_info['career'],
            "job_title": career_info['career']['position'],
            "company": career_info['career']['company'],
            "department": career_info['career']['department'],
            "years_experience": career_info['career']['years_experience']
        }