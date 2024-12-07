from data.location_data import location_data
from data.person_data import profile_data
from data.education_data import education_data
from datetime import datetime
import random


class EducationProfile:
    def __init__(self, country, age):
        self.country = country
        self.age = age

    def get_education_level(self, age, country):

        country_education = education_data["education_systems"][country]["education_levels"]
        
        for level in country_education:
            available_levels = []
            if age >= education_data["degree_requirements"][level]["min_age"] and age <= education_data["degree_requirements"][level]["max_age"]:
                available_levels.append(level)
        return random.choice(available_levels)

  # Gets major based on region
    def get_major(self, country):
        return random.choice(education_data["education_systems"][country]["major_fields"])

    def get_school_type(self, country, education_level):
        return random.choice(education_data["education_systems"][country]["school_types"][education_level])

    def generate_education_profile(self):
        education_level = self.get_education_level(self.age, self.country)
        
        # Get major field for college-level education, otherwise None
        major_field = None
        if education_level in ["Bachelors", "Masters", "Doctorate", "Associates"]:
            major_field = self.get_major(self.country)
        else:
            major_field = "No College Degree"
        
        return {
            "education_level": f"{education_level}",
            "major_field": f"{major_field}",
        }
