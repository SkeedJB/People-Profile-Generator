from data.location_data import location_data
from data.person_data import profile_data
from generation.gen_education import EducationProfile
from generation.gen_career import CareerProfile
import pandas as pd
from datetime import datetime
import random

class PersonProfile:
    def __init__(self):
        pass

    def generate_person_profile(self):
        self.country = random.choice(list(location_data["countries"].keys()))
        self.gender = random.choice(profile_data["sex"])
        
        # First randomly select age group
        self.age_group = random.choice(list(profile_data["age_groups"].keys()))
        birth_range = profile_data["age_groups"][self.age_group]["birth_years"]
        
        # Get age directly from range
        self.age_range = range(birth_range[0], birth_range[1])
        self.birth_year = random.choice(self.age_range)

        # Calculate age from birth year
        current_year = datetime.now().year
        self.age = current_year - self.birth_year

        if self.gender == "male":
            self.first_name = random.choice(profile_data["male_first_names"][self.country])
        else:
            self.first_name = random.choice(profile_data["female_first_names"][self.country])

        self.last_name = random.choice(profile_data["last_names"][self.country])

        # Store as instance variables
        self.education_profile = EducationProfile(
            country=self.country, 
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
                'Name', 'Birth Year', 'Age', 'Age Group', 'Gender',
                'Country', 'Languages',
                'Education Level', 'Major', 'School Type',
                'Career Pathway', 'Career Level', 'Job Title'
            ],
            'Value': [
                f"{self.first_name} {self.last_name}",
                self.birth_year,
                self.age,
                self.age_group,
                self.gender,
                self.country,
                location_data['countries'][self.country]['languages'],
                self.education_profile["education_level"],
                self.education_profile["major_field"],
                self.education_profile["school_type"],
                self.career_profile["career_pathway"],
                self.career_profile["level"],
                self.career_profile["job_title"]
            ]
        })
        
        return df



