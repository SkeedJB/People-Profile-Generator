import sys
import streamlit as st

sys.path.append(".")  # Add the project root to Python path
from generation.gen_person import PersonProfile

st.set_page_config(layout="wide")

def display_profile(profile):
    st.title(f"Profile: {profile['name']}")

    st.header("Personal Information")
    st.write(f"Age: {profile['age']}")
    st.write(f"Gender: {profile['gender']}")
    st.write(f"Location: {profile['location']}")
    st.write(f"Birth Year: {profile['birth_year']}")
    
    st.header("Education")
    st.write(f"Education Level: {profile['education_level']}")
    st.write(f"Major: {profile['major']}")

    st.header("Career")
    st.write(f"Career Pathway: {profile['career_pathway']}")
    st.write(f"Career Level: {profile['career_level']}")
    st.write(f"Job Title: {profile['job_title']}")

    if st.button("Back to Dashboard"):
        st.switch_page("pages/profile_dashboard.py")

    if st.button("Back to Home"):
        st.switch_page("home.py")

def main():
    if ("selected_profile_idx" not in st.session_state or 
        "profiles" not in st.session_state or 
        st.session_state.selected_profile_idx >= len(st.session_state.profiles) or
        st.session_state.profiles[st.session_state.selected_profile_idx] is None):
        
        st.error("No profile selected or profile data is invalid. Please select a profile from the home page.")
        if st.button("Back to Home"):
            st.switch_page("home.py")
    else:
        display_profile(st.session_state.profiles[st.session_state.selected_profile_idx])

if __name__ == "__main__":
    main()

