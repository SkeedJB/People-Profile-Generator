import sys
import streamlit as st
from faker import Faker
import random
from generation.gen_person import PersonProfile
from pages.profile_dashboard import generate_selected_profile  # Import the parent profile generator

def display_profile(profile):
    fake = Faker()
    st.title(f"Profile: {profile.get('name', 'N/A')}")

    st.header("Personal Information")
    st.write(f"Name: {profile.get('name_display', 'N/A')}")
    st.write(f"Age: {profile.get('age', 'N/A')}")
    st.write(f"Gender: {profile.get('gender', 'N/A')}")
    st.write(f"Country: {profile.get('country', 'N/A')}")
    st.write(f"Address: {profile.get('address', 'N/A')}")

    # Education Information
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

    # Career Information
    st.header("Current Career:")
    current_career = profile.get('career', None)
    if current_career:
        st.write(f"Position: {current_career.get('position', 'N/A')}")
        st.write(f"Company: {current_career.get('company', 'N/A')}")
        st.write(f"Department: {current_career.get('department', 'N/A')}")
        st.write(f"Years Experience: {current_career.get('years_experience', 'N/A')}")
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

    # Display Parents
    st.header("Parents")
    parent_metadata_list = profile.get('parents', [])
    if parent_metadata_list:
        for idx, parent_metadata in enumerate(parent_metadata_list):
            relation = parent_metadata.get('relation', 'Parent')
            st.markdown(f"### {relation.capitalize()}")
            
            # Button to view parent profile
            if st.button(f"View {relation.capitalize()}", key=f"view_parent_{profile['uuid']}_{idx}"):
                # Generate parent profile based on constraints
                parent_profile = generate_selected_profile(parent_metadata['constraints'])
                # Store the parent profile in session state
                st.session_state.profiles[parent_profile['uuid']] = parent_profile
                # Set the newly generated parent as selected
                st.session_state.selected_profile_uuid = parent_profile['uuid']
                st.rerun()  # Refresh the page to display the new profile
    else:
        st.write("No parents assigned.")

    # Save Profile Button
    st.header("Save Profile")
    if profile['uuid'] in st.session_state.get('saved_profiles', {}):
        st.success("Profile saved!")
        if st.button("Remove from Saved"):
            del st.session_state.saved_profiles[profile['uuid']]
            st.success("Profile removed from saved!")
    else:
        if st.button("Save Profile"):
            if 'saved_profiles' not in st.session_state:
                st.session_state.saved_profiles = {}
            st.session_state.saved_profiles[profile['uuid']] = profile
            st.success("Profile saved!")

    # Navigation Buttons
    st.header("Navigation")
    if st.button("Back to Dashboard"):
        st.switch_page("pages/profile_dashboard.py")

    if st.button("Back to Home"):
        st.switch_page("home.py")

def main():
    # Ensure profiles are initialized
    if 'profiles' not in st.session_state:
        st.session_state.profiles = {}
    
    # Check if a profile is selected
    if "selected_profile_uuid" not in st.session_state or not st.session_state.selected_profile_uuid:
        st.error("No profile selected. Please navigate from the dashboard.")
        if st.button("Back to Dashboard"):
            st.switch_page("pages/profile_dashboard.py")
        return
    
    selected_uuid = st.session_state.selected_profile_uuid
    profiles = st.session_state.profiles
    
    # Check if the selected profile exists
    if selected_uuid in profiles:
        profile = profiles[selected_uuid]
        display_profile(profile)
    else:
        st.error("Selected profile does not exist.")
        if st.button("Back to Dashboard"):
            st.switch_page("pages/profile_dashboard.py")

if __name__ == "__main__":
    main()

