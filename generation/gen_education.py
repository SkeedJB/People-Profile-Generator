from data.location_data import location_data
from data.person_data import profile_data
from data.education_data import education_data
import random

class EducationProfile:
    def __init__(self, country, age_group):
        self.country = country
        self.age_group = age_group

    def get_education_level(self):
        country_education = education_data["education_systems"][self.country]
        return random.choice(country_education["education_levels"])

    def get_education_timeline(self, birth_year):
        education_level = self.get_education_level()
        requirements = education_data["degree_requirements"][education_level]
        start_age = requirements["min_age"]
        duration = requirements["years"]
        return {
            "start_year": birth_year + start_age,
            "end_year": birth_year + start_age + duration,
            "duration": duration,
    }

    # Gets major based on region
    def get_major(self, country):
        return random.choice(education_data["education_systems"][country]["major_fields"])

    def get_school_type(self, country):
        try:
            return random.choice(education_data["education_systems"][country]["school_types"])
        except KeyError:
            return "Public School"

    def generate_education_profile(self):
        birth_year = random.choice(profile_data["age_groups"][self.age_group]["birth_years"])
        education_level = self.get_education_level()
        
        return {
            "education_level": education_level,
            "timeline": self.get_education_timeline(birth_year),
            "major": self.get_major(self.country),
            "school_type": self.get_school_type(self.country),
        }
