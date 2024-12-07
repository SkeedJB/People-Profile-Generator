from data.career_data import career_data
import random

class CareerProfile:
    def __init__(self, age, education_level, major):
        self.age = age
        self.education_level = education_level
        self.major = major
        
    def get_career_level(self):
        # Determine career level based on education
        if self.education_level in ["High School", "Associates"]:
            return "entry_level"
        elif self.education_level == "Bachelors":
            return "mid_level" 
        elif self.education_level == "Masters":
            return "senior_level"
        elif self.education_level == "Doctorate":
            return "executive_level"
        return "entry_level"

    def get_career_pathway(self):
        if self.education_level == "Not in school yet":
            return "Not in school yet"
        elif self.education_level in ["Elementary School", "Middle School", "High School"]:
            return "Student"
        elif self.major in career_data["career_pathways"]:
            return self.major
        else:
            return "Business" # Change this to service or retail

    def get_job_title(self, career_pathway, career_level):
        if career_pathway == "Student" or career_pathway == "Not in school yet":
            return "Student"
        return random.choice(career_data["career_pathways"][career_pathway][career_level])

    def get_required_skills(self, career_pathway):
        if career_pathway == "Student" or career_pathway == "Not in school yet":
            return ["Learning"]
        return career_data["career_pathways"][career_pathway]["required_skills"]

    def generate_career_profile(self):
        # If under 18, return student profile
        if self.age < 18:
            return {
                "career_pathway": "Student",
                "level": "Not Applicable", 
                "job_title": "Student",
            }
            
        career_pathway = self.get_career_pathway()
        career_level = self.get_career_level()
        
        if career_pathway == "Not in school yet":
            return {
                "career_pathway": career_pathway,
                "level": "Not Applicable",
                "job_title": "None"
            }
            
        return {
            "career_pathway": career_pathway,
            "level": career_level,
            "job_title": self.get_job_title(career_pathway, career_level),
        }

