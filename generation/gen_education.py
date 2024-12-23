from data.person_data import profile_data
from data.education_data import education_data
import random
from typing import Dict, List
from datetime import datetime

class EducationProfile:
    def __init__(self, age, filters=None):
        self.age = age
        self.current_year = datetime.now().year
        self.filters = filters or {}

    def get_education_level(self):
        """
        Returns the person's final education level in a more realistic, progressive way:
          1. K-12 path is age-based: Elementary (6 yrs), Middle (3 yrs), High (4 yrs).
          2. After high school, for each higher degree (Associates -> Bachelors -> Masters -> Doctorate),
             - check a random "success" probability
             - subtract time from the person's post‑HS years to model actuality
             - if not enough time remains, mark as "in progress"
          3. The function returns a single string, e.g. "Bachelors", "Masters (in progress)", etc.
        """

        # 1) If a specific education_level is set in filters (and person is old enough), use it directly
        if self.filters.get('education_level'):
            required_age = education_data["degree_requirements"][self.filters['education_level']]["min_age"]
            if self.age >= required_age:
                return self.filters['education_level']
            # If too young, fall back to age-based logic below

        # Durations (years) for each segment
        durations = {
            "Elementary School": 6,
            "Middle School": 3,
            "High School": 4,
            "Associates": 2,
            "Bachelors": 4,
            "Masters": 2,
            "Doctorate": 4
        }
        # Probability of entering each higher degree (after High School)
        # Each step is only attempted if the random check *and* time availability pass
        # This is a "progressive approach": if you skip Associates, you still may attempt Bachelors.
        # But you must first pass the random check for each step in sequence.
        degree_probability = {
            "Associates": 0.40,
            "Bachelors": 0.35,
            "Masters": 0.20,
            "Doctorate": 0.10
        }

        # 2) Model K-12 progression first
        #    Elementary (age 6..12), Middle (12..15), High (15..19).
        #    - If age < 6, "No Schooling" or "Elementary (in progress)"
        #    - If 6 <= age < 12, "Elementary (in progress)"
        #    - If 12 <= age < 15, "Middle (in progress)"
        #    - If 15 <= age < 19, "High School (in progress)"
        #    - If age >= 19, we consider High School completed, then move on to higher degrees.
        final_level = "No Schooling"

        # Check if old enough to have started elementary
        if self.age >= 6:
            if self.age < 12:
                # In progress of Elementary
                return "Elementary School (in progress)"
            else:
                final_level = "Elementary School"  # Completed

        # Check Middle School
        if self.age >= 12:
            if self.age < 15:
                return "Middle School (in progress)"
            else:
                final_level = "Middle School"

        # Check High School
        if self.age >= 15:
            if self.age < 19:
                return "High School (in progress)"
            else:
                final_level = "High School"

        # 3) If they've reached age 19, let's see how many post‑HS years are available
        post_hs_years = self.age - 19  # e.g. 23 y/o => 4 years after HS

        # Attempt each higher degree in a fixed order
        for degree in ["Associates", "Bachelors", "Masters", "Doctorate"]:
            # Check min_age from your config
            min_age = education_data["degree_requirements"][degree]["min_age"]
            if self.age < min_age:
                # Not old enough to start this degree at all
                continue

            # Roll random chance to see if they attempt this degree
            # If they fail the probability roll, we skip to the next degree
            if random.random() > degree_probability[degree]:
                continue

            # They decide to pursue the degree. Now check if they have enough time to finish it:
            needed = durations[degree]
            if post_hs_years >= needed:
                # Enough time to finish
                final_level = degree
                post_hs_years -= needed
            else:
                # Not enough time to finish => "in progress"
                final_level = f"{degree} (in progress)"
                # Once we mark in-progress for this degree, we won't attempt further degrees
                break

        return final_level

    # Gets major based on region
    def get_major(self):
        # Check if major field is specified in filters
        if self.filters.get('major_field'):
            return self.filters['major_field']
        return random.choice(education_data["education_systems"]["major_fields"])
    
    def get_school_type(self):
        return random.choice(education_data["school_types"])
    
    # Chronological education history
    def generate_education_history(self) -> List[Dict]:
        history = []
        highest_level = self.get_education_level()
        # Remove "(in progress)" if present to get base level
        base_level = highest_level.replace(" (in progress)", "")
        
        def add_education_entry(level: str, start_age: int, duration: int):
            if self.age < start_age:
                return None
                
            start_year = self.current_year - (self.age - start_age)
            end_year = start_year + duration
            
            # If still in school, mark as current
            is_current = False
            if level == base_level and "(in progress)" in highest_level:
                is_current = True
                # Calculate how many years they've completed so far
                years_completed = self.age - start_age
                if years_completed > 0:
                    end_year = start_year + years_completed
                else:
                    end_year = "Present"
            
            # Generate school name based on level
            school_type = self.get_school_type()
            school_name = f"{school_type} {'University' if level in ['Associates', 'Bachelors', 'Masters', 'Doctorate'] else 'School'}"
            
            entry = {
                "level": level,
                "institution": school_name,
                "start_year": start_year,
                "end_year": end_year,
                "duration": duration,
                "is_current": is_current,
                "type": school_type,
                "field_of_study": self.get_major() if level in ["Associates", "Bachelors", "Masters", "Doctorate"] else "General Education",
                "status": "Current" if is_current else "Completed",
            }
                
            return entry

        # Generate history entries based on final_level
        if self.age >= 6:
            elem_entry = add_education_entry("Elementary School", 6, 6)
            if elem_entry:
                history.append(elem_entry)

        if self.age >= 12 and base_level != "Elementary School":
            middle_entry = add_education_entry("Middle School", 12, 3)
            if middle_entry:
                history.append(middle_entry)

        if self.age >= 15 and base_level not in ["Elementary School", "Middle School"]:
            high_entry = add_education_entry("High School", 15, 4)
            if high_entry:
                history.append(high_entry)

        # Higher Education with same structure as before but with new fields
        if base_level in ["Associates", "Bachelors", "Masters", "Doctorate"]:
            current_age = 19  # Start after high school
            degree_durations = {
                "Associates": 2,
                "Bachelors": 4,
                "Masters": 2,
                "Doctorate": 4
            }
            for level in ["Associates", "Bachelors", "Masters", "Doctorate"]:
                if level == base_level:
                    break
                # 20% chance of gap year
                if random.random() < 0.2:
                    current_age += 1
                duration = degree_durations[level]
                entry = add_education_entry(level, current_age, duration)
                # 30% chance of keeping previous field of study
                if entry and history and random.random() < 0.3:
                    entry["field_of_study"] = history[-1]["field_of_study"]
                if entry:
                    history.append(entry)
                current_age += duration

        return sorted(history, key=lambda x: x["start_year"], reverse=True)