import sys
import streamlit as st

sys.path.append(".")  # Add the project root to Python path
from generation.gen_person import PersonProfile

st.set_page_config(layout="wide")

def display_profile(profile):
    st.title(f"Profile: {profile['name']}")

    st.header("Personal Information")
    st.write(f"Name: {profile['name_display']}")
    st.write(f"Age: {profile['age']}")
    st.write(f"Gender: {profile['gender']}")
    st.write(f"Country: {profile['country']}")
    st.write(f"Address: {profile['address']}")
    
    st.header("Education")
    st.write(f"Education Level: {profile['education_level']}")
    st.write(f"Major: {profile['major']}")

    st.header("Career")
    st.write(f"Job Title: {profile['job_title']}")
    st.write(f"Company: {profile['company']}")
    st.write(f"Department: {profile['department']}")
    st.write(f"Years of Experience: {profile['years_experience']}")
    
    st.header("Career History")
    if profile['career_history']:
        for job in profile['career_history']:
            with st.expander(f"{job['position']} at {job['company']} ({job['start_year']} - {job['end_year']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Position Details:**")
                    st.write(f"- Level: {job['level'].replace('_', ' ').title()}")
                    st.write(f"- Department: {job['department']}")
                    st.write(f"- Field: {job['field']}")
                with col2:
                    st.write("**Company Details:**")
                    st.write(f"- Duration: {job['duration']} years")
                    st.write(f"- Location: {job['location']}")
    else:
        st.write("No career history available")

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

