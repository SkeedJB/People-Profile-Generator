import sys
import streamlit as st
import pandas as pd

sys.path.append(".")  # Add the project root to Python path
from generation.gen_person import PersonProfile

st.set_page_config(layout="wide")

def main():
    st.title("Generated Profiles")
    
    # Initialize or generate profiles
    if "profiles" not in st.session_state:
        with st.spinner("Generating profiles..."):
            st.session_state.profiles = generate_profiles()
    
    # Create two rows with 3 columns each
    for row in range(2):
        cols = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            if idx < len(st.session_state.profiles):
                profile = st.session_state.profiles[idx]
                with cols[col]:
                    # Create a box effect with markdown
                    st.markdown("""
                        <div style="
                            padding: 20px;
                            border-radius: 10px;
                            border: 1px solid #ddd;
                            margin: 10px 0;
                            background-color: #f8f9fa;
                        ">
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"### {profile['name']}")
                    st.write(f"Age: {profile['age']}")
                    st.write(f"Gender: {profile['gender']}")
                    st.write(f"Location: {profile['location']}")
                    
                    if st.button("View Profile", key=f"view_profile_{idx}"):
                        st.session_state.selected_profile_idx = idx
                        st.switch_page("pages/profile_viewer.py")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add a button to generate new profiles
    if st.button("Generate New Profiles", use_container_width=True):
        with st.spinner("Generating new profiles..."):
            st.session_state.profiles = generate_profiles()
            st.experimental_rerun()

    # Add a button to go back home
    if st.button("Back to Home", use_container_width=True):
        st.switch_page("home.py")

def generate_profiles():
    profiles = []
    for i in range(6):
        person = PersonProfile()
        person.generate_person_profile()
        profile = {
            'name': f"{person.first_name} {person.last_name}",
            'age': person.age,
            'gender': person.gender,
            'location': person.country,
            'birth_year': person.birth_year,
            'education_level': person.education_profile['education_level'],
            'major': person.education_profile['major_field'],
            'school_type': person.education_profile['school_type'],
            'career_pathway': person.career_profile['career_pathway'],
            'career_level': person.career_profile['level'],
            'job_title': person.career_profile['job_title']
        }
        profiles.append(profile)
        st.success(f"Generated profile {i+1}: {profile['name']}")
    return profiles

if __name__ == "__main__":
    main()

