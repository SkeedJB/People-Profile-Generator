import sys
import streamlit as st
from faker import Faker
sys.path.append(".")  # Add the project root to Python path
from generation.gen_person import PersonProfile

st.set_page_config(layout="wide")

def display_profile(profile):
    fake = Faker()
    st.title(f"Profile: {profile.get('name', 'N/A')}")

    st.header("Personal Information")
    st.write(f"Name: {profile.get('name_display', 'N/A')}")
    st.write(f"Age: {profile.get('age', 'N/A')}")
    st.write(f"Gender: {profile.get('gender', 'N/A')}")
    st.write(f"Country: {profile.get('country', 'N/A')}")
    st.write(f"Address: {profile.get('address', 'N/A')}")
    
    st.header("Education")
    education_history = profile.get('education_history', [])
    if education_history:
        for entry in education_history:
            with st.expander(f"{entry.get('level', 'N/A')} ({entry.get('start_year', 'N/A')} - {entry.get('end_year', 'N/A')})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Major: {entry.get('major', 'N/A')}")
                with col2:
                    st.write(f"Duration: {entry.get('duration', 'N/A')} years")
    else:
        st.write("No education history available")

    st.header("Current Career:")
    current_career = profile.get('career', None)
    if current_career:
        st.write(f"Position: {current_career['position']}")
        st.write(f"Company: {current_career['company']}")
        st.write(f"Department: {current_career['department']}")
        st.write(f"Location: {current_career['location']}")
        st.write(f"Years Experience: {current_career['duration']}")
    else:
        st.write("Unemployed or no career history.")
    
    st.header("Career History")
    if profile.get('career_history'):
        for job in profile['career_history']:
            with st.expander(f"{job.get('position', 'N/A')} at {job.get('company', 'N/A')} ({job.get('start_year', 'N/A')} - {job.get('end_year', 'N/A')})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Position Details:**")
                    st.write(f"- Level: {job.get('level', 'N/A').replace('_', ' ').title()}")
                    st.write(f"- Department: {job.get('department', 'N/A')}")
                    st.write(f"- Field: {job.get('field', 'N/A')}")
                with col2:
                    st.write("**Company Details:**")
                    st.write(f"- Duration: {job.get('duration', 'N/A')} years")
                    st.write(f"- Location: {job.get('location', 'N/A')}")
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

