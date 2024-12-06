from data.location_data import location_data
from data.person_data import profile_data
from data.education_data import education_data
from datetime import datetime
import random


class EducationProfile:
    def __init__(self, country, age_group):
        self.country = country
        self.age_group = age_group

    def get_education_level(self, birth_year):
        current_year = datetime.now().year
        age = current_year - birth_year
        
        country_education = education_data["education_systems"][self.country]
        valid_levels = []
        
        for level in country_education["education_levels"]:
            if age >= education_data["degree_requirements"][level]["min_age"]:
                valid_levels.append(level)
                
        if not valid_levels:
            return "High School"
            
        return random.choice(valid_levels)

  # Gets major based on region
    def get_major(self, country):
        return random.choice(education_data["education_systems"][country]["major_fields"])

    def get_school_type(self, country, education_level):
        try:
            school_types = education_data["education_systems"][country]["school_types"]
            # Match school type to education level
            if education_level == "High School":
                return "High School"
            else:
                # For higher education, randomly choose between College and University
                return random.choice([st for st in school_types if st != "High School"])
        except KeyError:
            return "High School" if education_level == "High School" else "University"

    def generate_education_profile(self):
        birth_year = random.choice(profile_data["age_groups"][self.age_group]["birth_years"])
        education_level = self.get_education_level(birth_year)
        
        return {
            "education_level": f"{education_level}",
            "major_field": f"{self.get_major(self.country)}",
            "school_type": f"{self.get_school_type(self.country, education_level)}",
        }
