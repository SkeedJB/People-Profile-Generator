from location_data import location_data
from person_data import profile_data
from education_data import education_data

def generate_education_level(age_group, region):
    age_range = profile_data["age_groups"][age_group]["birth_years"]
    region_data = location_data["countries"][region]
    education_levels = education_data["education_systems"][region_data["country"]]["education_levels"]
    return random.choice(education_levels)

def get_education_timeline(birth_year, education_level):
    requirements = education_data["degree_requirements"][education_level]
    start_age = requirements["min_age"]
    duration = requirements["years"]
    prerequisites = requirements["prerequisites"]
    return {
        "start_year": birth_year + start_age,
        "end_year": birth_year + start_age + duration,
        "duration": duration,
    }

def get_major_by_region(region):
    region_data = location_data["countries"][region]
    industry_focus = region_data.get("industries", [])
    majors = education_data["major_fields"]
    return random.choice(majors)
