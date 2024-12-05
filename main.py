from data.education_data import education_data
from data.location_data import location_data
from data.person_data import profile_data
from generation.gen_education import EducationProfile
from generation.gen_person import PersonProfile

person_profile = PersonProfile().generate_person_profile()
print(person_profile)
