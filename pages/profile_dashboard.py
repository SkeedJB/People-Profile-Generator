import sys
import streamlit as st
import pandas as pd
from data.country_data import COUNTRIES
from data.education_data import education_data
from data.person_data import profile_data
import math
import uuid
import random  # Needed for random operations

sys.path.append(".")  # Add the project root to Python path
from generation.gen_person import PersonProfile

st.set_page_config(layout="wide")

def main():
    # Initialize profiles in session state if not present
    if 'profiles' not in st.session_state:
        st.session_state.profiles = {}
    
    # Filter profile creation by country
    with st.expander("Filter Profiles"):
        selected_country = st.selectbox("Select Country", ["All"] + list(set(COUNTRIES)))
        selected_gender = st.selectbox("Select Gender", ["All"] + list(set(profile_data["sex"])))
        selected_age_range = st.slider("Select Age Range", 18, 100, (18, 100))
        selected_education_level = st.selectbox("Select Education Level", ["All"] + list(set(education_data["education_systems"]["education_levels"])))

    num_of_profiles = st.slider("Number of Profiles", 1, 15, 6)
    columns_per_row = st.slider("Columns per Row", 1, 5, 3)

    if st.button("Generate Profiles", use_container_width=True):
        with st.spinner("Generating profiles..."):
            new_profiles = generate_profiles(
                num_of_profiles, 
                selected_country, 
                selected_gender, 
                selected_age_range, 
                selected_education_level
            )
            # Update the profiles dictionary with new profiles
            st.session_state.profiles.update(new_profiles)

    if st.session_state.profiles:
        st.title("Generated Profiles")

        def render_profile(profile):
            st.markdown(
                f"""
                <div style="
                    padding: 20px;
                    border-radius: 15px;
                    border: 2px solid #e0e0e0;
                    margin: 12px 0;
                    background-color: rgba(0,0,0,0.8);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                    transition: transform 0.2s;
                    cursor: pointer;
                ">
                    <div style="display: flex; align-items: center;">
                        <div style="width: 60px; height: 60px; border-radius: 50%; background-color: {profile.get('color', '#444')}; margin-right: 15px;"></div>
                        <div>
                            <h3 style="margin: 0; color: #fff;">{profile['name_display']}</h3>
                            <p style="margin: 5px 0; color: #ccc;">Age: {profile['age']} | {profile['gender']}</p>
                            <p style="margin: 5px 0; color: #ccc;">{profile['job_title']} at {profile['company']}</p>
                            <p style="margin: 5px 0; color: #ccc;">{profile['country']}</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("View Profile", key=f"view_profile_{profile['uuid']}"):
                st.session_state.selected_profile_uuid = profile['uuid']
                st.switch_page("pages/profile_viewer.py")

        # Allows user to change number of columns per row
        total_profiles = len(st.session_state.profiles)
        rows = math.ceil(total_profiles / columns_per_row)

        # Sort profiles for consistent display
        sorted_profiles = list(st.session_state.profiles.values())

        for row in range(rows):
            cols = st.columns(columns_per_row)
            for col_idx in range(columns_per_row):
                idx = row * columns_per_row + col_idx
                if idx < total_profiles:
                    profile = sorted_profiles[idx]
                    with cols[col_idx]:
                        render_profile(profile)

    # Only show "Generate New Profiles" button if profiles exist
    if st.session_state.profiles:
        if st.button("Generate New Profiles", use_container_width=True):
            with st.spinner("Generating new profiles..."):
                new_profiles = generate_profiles(
                    num_of_profiles, 
                    selected_country, 
                    selected_gender, 
                    selected_age_range, 
                    selected_education_level
                )
                st.session_state.profiles.update(new_profiles)
    
    if st.button("Back to Home", use_container_width=True):
        st.switch_page("home.py")

# Generates profiles based on user selection
def generate_profiles(num_of_profiles, selected_country="All", selected_gender="All", selected_age_range=(18, 100), selected_education_level="All"):
    profiles = {}
    filters = {}

    # Filters profiles based on user selection
    if selected_country != "All":
        filters['country'] = selected_country
    if selected_gender != "All":
        filters['gender'] = selected_gender
    if selected_age_range != (18, 100):
        filters['age_range'] = selected_age_range
    if selected_education_level != "All":
        filters['education_level'] = selected_education_level

    for _ in range(num_of_profiles):
        person = PersonProfile(filters=filters)
        person.generate_person_profile()

        name_display = person.full_name
        if hasattr(person, 'full_name_romanized') and person.full_name_romanized != person.full_name:
            name_display = f"{person.full_name} \n({person.full_name_romanized})"

        career = person.career_profile.get('career', {})
        profile_uuid = str(uuid.uuid4())

        profile = {
            # Unique identifier for each profile
            'uuid': profile_uuid,
            'parents': [
                {
                    'relation': 'father', 
                    'constraints': {'country': person.country, 'min_age_diff': 16, 'child_age': person.age}
                },
                {
                    'relation': 'mother', 
                    'constraints': {'country': person.country, 'min_age_diff': 16, 'child_age': person.age}
                }
            ],

            'name': person.full_name,
            'name_display': name_display,
            'name_romanized': person.full_name_romanized,
            'age': person.age,
            'gender': person.gender,
            'country': person.country,
            'address': person.address,
            'education_level': person.education_profile['education_level'],
            'education_history': person.education_profile['education_history'],  # Ensure this is included
            'major': person.education_profile['major_field'],
            'career_history': person.career_profile['career_history'],
            'career': career,
            'job_title': career.get('position', "N/A") if career else "N/A",
            'company': career.get('company', "N/A") if career else "N/A",
            'department': career.get('department', "N/A") if career else "N/A",
            'years_experience': career.get('years_experience', 'N/A') if career else 'N/A'
        }
        profiles[profile_uuid] = profile
    return profiles

# Generates a profile based on constraints (for on-demand parent generation)
def generate_selected_profile(constraints):
    gender = constraints.get('gender', 'All')
    country = constraints.get('country', 'All')
    min_age_diff = constraints.get('min_age_diff', 0)
    last_name = constraints.get('last_name', 'All')
    child_age = constraints.get('child_age', 25)  # Default if not provided
    relation = constraints.get('relation', 'parent')

    person = PersonProfile(filters={'country': country, 'gender': gender, 'last_name': last_name, 'min_age_diff': min_age_diff, 'child_age': child_age})
    person.generate_person_profile()

    # Adjust age based on min_age_diff
    generated_age = child_age + min_age_diff + random.randint(1, 10)
    person.age = generated_age

    # Set gender based on relation
    if relation == 'father':
        person.gender = 'male'
    elif relation == 'mother':
        person.gender = 'female'

    # Regenerate profile with updated age and gender
    person.generate_person_profile()

    name_display = person.full_name
    if hasattr(person, 'full_name_romanized') and person.full_name_romanized != person.full_name:
        name_display = f"{person.full_name} \n({person.full_name_romanized})"

    career = person.career_profile.get('career', {})
    profile_uuid = str(uuid.uuid4())

    profile = {
        'uuid': profile_uuid,
        'parents': [
            {
                'relation': 'father', 
                'constraints': {'country': person.country, 'last_name': person.last_name, 'gender': person.gender, 'min_age_diff': 16, 'child_age': person.age}
            },
            {
                'relation': 'mother', 
                'constraints': {'country': person.country, 'last_name': person.last_name, 'gender': person.gender, 'min_age_diff': 16, 'child_age': person.age}
            }
        ],

        'name': person.full_name,
        'name_display': name_display,
        'name_romanized': person.full_name_romanized,
        'age': person.age,
        'gender': person.gender,
        'country': person.country,
        'address': person.address,
        'education_level': person.education_profile['education_level'],
        'education_history': person.education_profile['education_history'],
        'major': person.education_profile['major_field'],
        'career_history': person.career_profile['career_history'],
        'career': career,
        'job_title': career.get('position', "N/A") if career else "N/A",
        'company': career.get('company', "N/A") if career else "N/A",
        'department': career.get('department', "N/A") if career else "N/A",
        'years_experience': career.get('years_experience', 'N/A') if career else 'N/A'
    }
    return profile

if __name__ == "__main__":
    main()

