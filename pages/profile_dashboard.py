import sys
import streamlit as st
import pandas as pd

sys.path.append(".")  # Add the project root to Python path
from generation.gen_person import PersonProfile

st.set_page_config(layout="wide")

def main():
    st.title("Generated Profiles")
    
    # Initialize profiles
    if "profiles" not in st.session_state:
        with st.spinner("Generating profiles..."):
            st.session_state.profiles = generate_profiles()
    
    # Two rows with 3 columns each
    for row in range(2):
        cols = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            if idx < len(st.session_state.profiles):
                profile = st.session_state.profiles[idx]
                with cols[col]:
                    # Box effect with markdown
                    st.markdown("""
                        <div style="
                            padding: 25px;
                            border-radius: 15px;
                            border: 2px solid #e0e0e0;
                            margin: 12px 0;
                            background-color: white;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            transition: transform 0.2s ease;
                            &:hover {
                                transform: translateY(-2px);
                                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                            }
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
    
    # Buttons
    if st.button("Generate New Profiles", use_container_width=True):
        with st.spinner("Generating new profiles..."):
            st.session_state.profiles = generate_profiles()
        
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
            'education_level': person.education_profile['education_level'],
            'major': person.education_profile['major_field'],
            'career_pathway': person.career_profile['career_pathway'],
            'career_level': person.career_profile['level'],
            'job_title': person.career_profile['job_title']
        }
        profiles.append(profile)
    return profiles

if __name__ == "__main__":
    main()

