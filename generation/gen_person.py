from data.location_data import location_data
from data.person_data import profile_data
from generation.gen_education import EducationProfile
from datetime import datetime
import random

class PersonProfile:
    def __init__(self):
        pass

    def generate_person_profile(self):
        self.country = random.choice(list(location_data["countries"].keys()))
        self.gender = random.choice(profile_data["sex"])
        self.age_group = random.choice(list(profile_data["age_groups"].keys()))
        self.birth_year = random.choice(profile_data["age_groups"][self.age_group]["birth_years"])

        if self.gender == "male":
            self.first_name = random.choice(profile_data["male_first_names"][self.country])
        else:
            self.first_name = random.choice(profile_data["female_first_names"][self.country])

        self.last_name = random.choice(profile_data["last_names"][self.country])

        current_year = datetime.now().year
        self.age = current_year - self.birth_year

        person_profile = {
            "personal": {
                "name": f"{self.first_name} {self.last_name}",
                "birth_year": self.birth_year,
                "age": self.age,
                "age_group": self.age_group,
                "gender": self.gender,
            },
            "location": {
                "country": self.country,
                "languages": location_data["countries"][self.country]["languages"]  
            },
            "education": EducationProfile(country=self.country, age_group=self.age_group).generate_education_profile(),
        }

        return person_profile

