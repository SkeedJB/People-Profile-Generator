from data.person_data import profile_data
from data.education_data import education_data
import random


class EducationProfile:
    def __init__(self, age):
        self.age = age

    def get_education_level(self):
        # Determines the minimum level based on age
        base_level = "No Schooling"
        for level in education_data["education_systems"]["education_levels"]:
            if self.age >= education_data["degree_requirements"][level]["min_age"]:
                base_level = level

        # Education probability factors
        higher_ed_probability = {
            "Associates": 0.40,  # 40% chance of pursuing associates
            "Bachelors": 0.35,  # 35% chance of pursuing bachelors
            "Masters": 0.15,    # 15% chance of pursuing masters
            "Doctorate": 0.05   # 5% chance of pursuing doctorate
        }

        # If person is of college age or older
        if self.age >= education_data["degree_requirements"]["Associates"]["min_age"]:
            # Start with high school as minimum for adults
            if base_level in ["Elementary School", "Middle School"]:
                return "High School"
                
            # Determine highest achieved education
            for degree in ["Associates", "Bachelors", "Masters", "Doctorate"]:
                if (self.age >= education_data["degree_requirements"][degree]["min_age"] and 
                    random.random() < higher_ed_probability[degree]):
                    return degree
                    
            return "High School"  # Default to high school if no higher education
            
        return base_level  # Return base level for young people still in school

  # Gets major based on region
    def get_major(self):
        return random.choice(education_data["education_systems"]["major_fields"])

    def get_school_type(self, education_level):
        school_type = random.choice(education_data["education_systems"]["school_types"][education_level])
        return school_type

    def generate_education_profile(self):
        education_level = self.get_education_level()
        
        # Get major field for college-level education, otherwise None
        major_field = None
        if education_level in ["Bachelors", "Masters", "Doctorate", "Associates"]:
            major_field = self.get_major()
        else:
            major_field = "No College Degree"
        
        return {
            "education_level": f"{education_level}",
            "major_field": f"{major_field}",
        }
