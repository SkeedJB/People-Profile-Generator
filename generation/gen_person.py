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
    def __init__(self):
        pass

    def get_country(self):
        self.country = random.choice(COUNTRIES)
        self.country_code = COUNTRY_LOCALES[self.country]
        return self.country, self.country_code
    
    def get_address(self):
        fake = Faker(locale=self.country_code)
        self.address = fake.unique.address()
        return self.address
    
    def get_gender(self):
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
        birth_year = random.randint(profile_data["birth_range"][0], profile_data["birth_range"][1])
        self.age = datetime.now().year - birth_year
        return self.age

    def generate_person_profile(self):
        self.get_country()
        self.get_address()
        self.get_gender()
        self.get_name(self.gender)
        self.get_age()

        # Initialize EducationProfile
        education = EducationProfile(age=self.age)

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
        career_data = career_generator.generate_career_history(
            age=self.age,
            education_history=self.education_profile["education_history"]
        )

        if career_data['career'] is None:
            career_data['career'] = {
                "position": "Unemployed",
                "company": "N/A",
                "department": "N/A",
                "location": "N/A",
                "years_experience": 0
        }


        self.career_profile = {
            "career_history": career_data['career_history'],
            "career": career_data['career'],
            "job_title": career_data['career']['position'],
            "company": career_data['career']['company'],
            "department": career_data['career']['department'],
            "location": career_data['career']['location'],
            "years_experience": (career_data['career']['end_year'] - career_data['career']['start_year'])
        }


    def create_dataframe(self):
        self.generate_person_profile()

        name_display = self.full_name
        if self.full_name_romanized != self.full_name:
            name_display = f"{self.full_name}\n({self.full_name_romanized})"
        
        df = pd.DataFrame({
            'Category': [
                'Name', 'Age', 'Gender',
                'Country',
                'Education Level', 'Major', 'School Type',
                'Career Pathway', 'Career Level', 'Job Title'
            ],
            'Value': [
                name_display,
                self.age,
                self.gender,
                self.country,
                self.address,
                self.education_profile["education_history"],
                self.education_profile["education_level"],
                self.education_profile["major_field"],
                self.education_profile["school_type"],
                self.career_profile["career_pathway"],
                self.career_profile["level"],
                self.career_profile["job_title"]
            ]
        })
        
        return df