from faker import Faker
from data.person_data import profile_data
from generation.gen_education import EducationProfile
from generation.gen_career import CareerProfile
from data.country_data import COUNTRIES, COUNTRY_LOCALES
import pandas as pd
import random
from datetime import datetime

class PersonProfile:
    def __init__(self):
        pass

    def get_country(self):
        self.country = random.choice(COUNTRIES)
        self.country_code = COUNTRY_LOCALES[self.country]
        return self.country, self.country_code

    def get_gender(self):
        self.gender = random.choice(profile_data["sex"])
        return self.gender

    def get_name(self):
        fake = Faker(locale=self.country_code)
        self.first_name = fake.unique.first_name_male()
        self.last_name = fake.unique.last_name()
        return self.first_name, self.last_name
    
    def get_age(self):
        birth_year = random.randint(profile_data["birth_range"][0], profile_data["birth_range"][1])
        self.age = datetime.now().year - birth_year
        return self.age

    def generate_person_profile(self):
        self.get_country()
        self.get_gender()
        self.get_name()
        self.get_age()
        # Store as instance variables
        self.education_profile = EducationProfile(
            age=self.age
        ).generate_education_profile()

        self.career_profile = CareerProfile(
            age=self.age,
            education_level=self.education_profile["education_level"],
            major=self.education_profile["major_field"]
        ).generate_career_profile()

    def create_dataframe(self):
        # Call generate_person_profile first
        self.generate_person_profile()
        
        # Create a 2-column DataFrame for better Streamlit display
        df = pd.DataFrame({
            'Category': [
                'Name', 'Age', 'Gender',
                'Country',
                'Education Level', 'Major', 'School Type',
                'Career Pathway', 'Career Level', 'Job Title'
            ],
            'Value': [
                f"{self.first_name} {self.last_name}",
                self.age,
                self.gender,
                self.country,
                self.education_profile["education_level"],
                self.education_profile["major_field"],
                self.education_profile["school_type"],
                self.career_profile["career_pathway"],
                self.career_profile["level"],
                self.career_profile["job_title"]
            ]
        })
        
        return df