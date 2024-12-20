import streamlit as st
import home
from pages import profile_dashboard
from pages import profile_viewer

def main():
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'home'

    if st.session_state.current_view == 'home':
        home.main()
    elif st.session_state.current_view == 'profile_dashboard':
        profile_dashboard.main()
    elif st.session_state.current_view == 'profile_viewer':
        profile_viewer.main()
    else:
        st.error("Unknown view selected.")

if __name__ == "__main__":
    main()
