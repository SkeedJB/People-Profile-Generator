import streamlit as st
from generation.gen_person import PersonProfile

st.set_page_config(layout="wide")

def main():
    st.title("Person Profile Generator")
    
    if st.button("Generate Profiles", use_container_width=True):
        st.switch_page("pages/profile_dashboard.py")

if __name__ == "__main__":
    main()
