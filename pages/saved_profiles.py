import streamlit as st

def main():
    st.title("Saved Profiles")
    
    # Initialize saved_profiles in session state if not present
    if 'saved_profiles' not in st.session_state:
        st.session_state.saved_profiles = {}
    
    if not st.session_state.saved_profiles:
        st.info("No saved profiles yet. View a profile and click 'Save Profile' to add it here.")
    else:
        # Display saved profiles using the same layout as profile_dashboard
        for profile_uuid, profile in st.session_state.saved_profiles.items():
            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        padding: 20px;
                        border-radius: 15px;
                        border: 2px solid #e0e0e0;
                        margin: 12px 0;
                        background-color: rgba(169,169,169,0.8);
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
                if st.button("View Profile", key=f"view_saved_{profile_uuid}"):
                    st.session_state.selected_profile_uuid = profile_uuid
                    st.switch_page("pages/profile_viewer.py")
                
                if st.button("Remove from Saved", key=f"remove_{profile_uuid}"):
                    del st.session_state.saved_profiles[profile_uuid]
                    st.rerun()
    
    if st.button("Back to Dashboard"):
        st.switch_page("pages/profile_dashboard.py")

if __name__ == "__main__":
    main()