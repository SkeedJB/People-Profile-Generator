import streamlit as st
from generation.gen_person import PersonProfile
st.set_page_config(layout="wide")

def main():
    # Initialize session state if not already done
    if 'profiles' not in st.session_state:
        st.session_state.profiles = {}
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'home'
    if 'selected_profile_uuid' not in st.session_state:
        st.session_state.selected_profile_uuid = None

    # Header
    st.markdown("""
        <h1 style='text-align: center; color: #2e6c80;'>
            Person Profile Generator
        </h1>
    """, unsafe_allow_html=True)

    # Welcome message
    st.markdown("""
        ### Welcome to the Profile Generator!
        
        This tool creates realistic fictional profiles for various purposes including:
        - User testing scenarios
        - Sample data generation
        - Character development
        - Demographics research
        
        Each generated profile includes:
        - Personal information (name, age, gender)
        - Educational background
        - Career details
        - Location data
        
        Click the button below to generate a set of diverse profiles!
    """)

    st.markdown("<br>", unsafe_allow_html=True)
    
    button_container = st.container()
    with button_container:
        if st.button("Go to Dashboard", use_container_width=True):
            st.switch_page("pages/profile_dashboard.py")

if __name__ == "__main__":
    main()
