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
        
        # Calculate age range based on birth years
        current_year = datetime.now().year
        min_age = current_year - birth_range[1]  # Youngest possible age
        max_age = current_year - birth_range[0]  # Oldest possible age
        self.age = random.randint(min_age, max_age)
        self.birth_year = current_year - self.age

        if self.gender == "male":
            self.first_name = random.choice(profile_data["male_first_names"][self.country])
        else:
            self.first_name = random.choice(profile_data["female_first_names"][self.country])

        self.last_name = random.choice(profile_data["last_names"][self.country])

        # Store as instance variables
        self.education_profile = EducationProfile(
            country=self.country, 
            age_group=self.age_group
        ).generate_education_profile()

        self.career_profile = CareerProfile(
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



