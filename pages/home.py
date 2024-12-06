import sys
import streamlit as st

sys.path.append(".")  # Add the project root to Python path
from generation.gen_person import PersonProfile

st.title("Person Profile Generator")

if st.button("Generate Profile"):
    try:
        person_profile = PersonProfile().create_dataframe()
        st.dataframe(
            person_profile,
            column_config={
                "Category": st.column_config.TextColumn("Category", width="medium"),
                "Value": st.column_config.TextColumn("Value", width="large")
            },
            hide_index=True
        )
    except Exception as e:
        st.error(f"Error generating profile: {str(e)}")
        st.exception(e)
