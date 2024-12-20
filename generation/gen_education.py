from data.person_data import profile_data
from data.education_data import education_data
import random
from faker import Faker
from typing import Dict, List
from datetime import datetime

class EducationProfile:
    def __init__(self, age, filters=None):
        self.age = age
        self.current_year = datetime.now().year
        self.filters = filters or {}

    def get_education_level(self):
        # Check if education level is specified in filters
        if self.filters.get('education_level'):
            # Verify age meets minimum requirements
            required_age = education_data["degree_requirements"][self.filters['education_level']]["min_age"]
            if self.age >= required_age:
                return self.filters['education_level']
            # If too young for filtered education level, fall back to age-appropriate level
        
        # Original education level logic
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
        # Check if major field is specified in filters
        if self.filters.get('major_field'):
            return self.filters['major_field']
        return random.choice(education_data["education_systems"]["major_fields"])
    
    def get_school_type(self):
        return random.choice(education_data["education_systems"]["school_types"])
    
    # Chronological education history
    def generate_education_history(self) -> List[Dict]:
        history = []
        highest_level = self.get_education_level()
        
        def add_education_entry(level: str, start_age: int, duration: int):
            if self.age < start_age:
                return None
                
            start_year = self.current_year - (self.age - start_age)
            end_year = start_year + duration
            
            # If still in school, mark as current
            is_current = False
            if end_year > self.current_year:
                end_year = self.current_year
                is_current = True
            
            # Generate school name based on level
            school_type = self.get_school_type(level) if level in education_data["school_types"] else ""
            school_name = f"{school_type} {'University' if level in ['Associates', 'Bachelors', 'Masters', 'Doctorate'] else 'School'}"
            
            entry = {
                "level": level,
                "institution": school_name,
                "start_year": start_year,
                "end_year": end_year if not is_current else "Present",
                "duration": duration,
                "is_current": is_current,
                "type": school_type,
                "field_of_study": self.get_major() if level in ["Associates", "Bachelors", "Masters", "Doctorate"] else "General Education",
                "status": "Current" if is_current else "Completed",
            }
                
            return entry

        # Generate history entries
        if self.age >= 6:
            elem_entry = add_education_entry("Elementary School", 6, 6)
            if elem_entry:
                history.append(elem_entry)

        if self.age >= 12 and highest_level != "Elementary School":
            middle_entry = add_education_entry("Middle School", 12, 3)
            if middle_entry:
                history.append(middle_entry)

        if self.age >= 15 and highest_level not in ["Elementary School", "Middle School"]:
            high_entry = add_education_entry("High School", 15, 4)
            if high_entry:
                history.append(high_entry)

        # Higher Education with same structure as before but with new fields
        if highest_level in ["Associates", "Bachelors", "Masters", "Doctorate"]:
            current_age = 19
            degree_durations = {
                "Associates": 2,
                "Bachelors": 4,
                "Masters": 2,
                "Doctorate": 4
            }
            for level in ["Associates", "Bachelors", "Masters", "Doctorate"]:
                if level == highest_level:
                    break
                if random.random() < 0.2:
                    current_age += 1
                duration = degree_durations[level]
                entry = add_education_entry(level, current_age, duration)
                if entry and history and random.random() < 0.3:
                    entry["field_of_study"] = history[-1]["field_of_study"]
                if entry:
                    history.append(entry)
                current_age += duration

        return sorted(history, key=lambda x: x["start_year"], reverse=True)