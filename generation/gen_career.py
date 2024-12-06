from data.career_data import career_data
import random

class CareerProfile:
    def __init__(self, education_level, major):
        self.education_level = education_level
        self.major = major

    def get_career_pathway(self):
        # Map education major to career pathway
        # Default to Business if major doesn't match exactly
        if self.major in career_data["career_pathways"]:
            return self.major
        return "Business"

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

    def get_job_title(self, pathway, level):
        return random.choice(career_data["career_pathways"][pathway][level])

    def get_required_skills(self, pathway):
        return career_data["career_pathways"][pathway]["required_skills"]

    def generate_career_profile(self):
        # Return no job if person has no education yet
        if not self.education_level or self.education_level == "None":
            return {
                "career_pathway": "None",
                "level": "None", 
                "job_title": "None",
                "required_skills": "None",
                "education_requirements": "None"
            }
            
        career_pathway = self.get_career_pathway()
        career_level = self.get_career_level()
        
        return {
            "career_pathway": f"{career_pathway}",
            "level": f"{career_level}",
            "job_title": f"{self.get_job_title(career_pathway, career_level)}",
            "required_skills": f"{self.get_required_skills(career_pathway)}",
            "education_requirements": f"{career_data['career_pathways'][career_pathway]['required_education']}"
        }

