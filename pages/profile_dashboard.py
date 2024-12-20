import sys
import streamlit as st
import pandas as pd
from data.country_data import COUNTRIES
from data.education_data import education_data
from data.person_data import profile_data
import math

sys.path.append(".")  # Add the project root to Python path
from generation.gen_person import PersonProfile

st.set_page_config(layout="wide")

def main():
    
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
            st.session_state.profiles = generate_profiles(
                num_of_profiles, 
                selected_country, 
                selected_gender, 
                selected_age_range, 
                selected_education_level
            )

    if hasattr(st.session_state, 'profiles') and st.session_state.profiles:
        st.title("Generated Profiles")

        def render_profile(profile, idx):
            """Helper function to render a profile."""
            st.markdown(
                f"""
                <div style="
                    padding: 20px;
                    border-radius: 15px;
                    border: 2px solid #e0e0e0;
                    margin: 12px 0;
                    background-color: black;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <h3>{profile['name_display']}</h3>
                    <p>Age: {profile['age']}</p>
                    <p>Gender: {profile['gender']}</p>
                    <p>Country: {profile['country']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("View Profile", key=f"view_profile_{idx}"):
                st.session_state.selected_profile_idx = idx
                st.switch_page("pages/profile_viewer.py")

        # Dynamic grid generation
        total_profiles = len(st.session_state.profiles)
        rows = math.ceil(total_profiles / columns_per_row)

        for row in range(rows):
            cols = st.columns(columns_per_row)
            for col_idx in range(columns_per_row):
                idx = row * columns_per_row + col_idx
                if idx < total_profiles:
                    profile = st.session_state.profiles[idx]
                    with cols[col_idx]:
                        render_profile(profile, idx)

    
    # Only show "Generate New Profiles" button if profiles exist
    if hasattr(st.session_state, 'profiles') and st.session_state.profiles:
        if st.button("Generate New Profiles", use_container_width=True):
            with st.spinner("Generating new profiles..."):
                st.session_state.profiles = generate_profiles(num_of_profiles, selected_country, selected_gender, selected_age_range, selected_education_level)
        
    if st.button("Back to Home", use_container_width=True):
        st.switch_page("home.py")

# Generates 6 profiles
def generate_profiles(num_of_profiles, selected_country="All", selected_gender="All", selected_age_range=(18, 100), selected_education_level="All"):
    profiles = []
    filters = {}
    
    if selected_country != "All":
        filters['country'] = selected_country
    if selected_gender != "All":
        filters['gender'] = selected_gender
    if selected_age_range != (18, 100):
        filters['age_range'] = selected_age_range
    if selected_education_level != "All":
        filters['education_level'] = selected_education_level

    for i in range(num_of_profiles):
        person = PersonProfile(filters=filters)
        person.generate_person_profile()

        name_display = person.full_name
        if hasattr(person, 'full_name_romanized') and person.full_name_romanized != person.full_name:
            name_display = f"{person.full_name} \n({person.full_name_romanized})"

        profile = {
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
            'career': person.career_profile['career'],
            'job_title': person.career_profile['career']['position'] if person.career_profile['career'] else "N/A",
            'company': person.career_profile['career']['company'] if person.career_profile['career'] else "N/A",
            'department': person.career_profile['career']['department'] if person.career_profile['career'] else "N/A",
            'years_experience': person.career_profile['years_experience']
        }
        profiles.append(profile)
    return profiles

if __name__ == "__main__":
    main()

