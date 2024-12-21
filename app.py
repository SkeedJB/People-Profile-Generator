"""
app.py
---------------
This is the main entry point for the Flask application.
It initializes the Flask app, configures any extensions,
and registers blueprints (in this example, we place all routes
directly in this file for simplicity, but you could factor them
out into separate files and use blueprints if you prefer).
"""

from flask import Flask, render_template, request, redirect, url_for
import uuid
import random
# Generation imports
from generation.gen_person import PersonProfile
from generation.gen_career import CareerGenerator
from generation.gen_education import EducationProfile

# Data imports
from data.person_data import profile_data
from data.country_data import COUNTRIES, COUNTRY_LOCALES
from data.education_data import education_data
from data.career_data import CareerData

app = Flask(__name__)

# In a production app, you'd likely use a database instead of this dictionary.
# For demonstration, we will store data in memory (similar to Streamlit session_state).
PROFILES = {}
SAVED_PROFILES = {}

# ------------------------------------------------------------------------------
# Helper function to generate profiles according to user filters
# (Equivalent to generate_profiles in your original profile_dashboard.py)
# ------------------------------------------------------------------------------
def generate_profiles(num_of_profiles, selected_country="All", selected_gender="All",
                      selected_age_range=(18, 100), selected_education_level="All"):
    """
    Generate a dictionary of profiles keyed by UUID, applying filters if specified.
    """
    profiles = {}
    filters = {}

    # Translate "All" vs. specific filters
    if selected_country != "All":
        filters['country'] = selected_country
    if selected_gender != "All":
        filters['gender'] = selected_gender
    if selected_age_range != (18, 100):
        filters['age_range'] = selected_age_range
    if selected_education_level != "All":
        filters['education_level'] = selected_education_level

    for _ in range(num_of_profiles):
        person = PersonProfile(filters=filters)
        person.generate_person_profile()  # builds out the person's data

        # If the name is in a different alphabet, person generates full_name_romanized
        name_display = person.full_name
        if hasattr(person, 'full_name_romanized') and person.full_name_romanized != person.full_name:
            name_display = f"{person.full_name} \n({person.full_name_romanized})"

        career = person.career_profile.get('career', {})
        profile_uuid = str(uuid.uuid4())  # unique ID

        # Build the final dictionary for a single profile
        profile = {
            'uuid': profile_uuid,
            'parents': [
                {
                    'relation': 'father',
                    'constraints': {'country': person.country, 'min_age_diff': 16, 'child_age': person.age}
                },
                {
                    'relation': 'mother',
                    'constraints': {'country': person.country, 'min_age_diff': 16, 'child_age': person.age}
                }
            ],
            'name': person.full_name,
            'name_display': name_display,
            'name_romanized': person.full_name_romanized,
            'age': person.age,
            'gender': person.gender,
            'country': person.country,
            'address': person.address,
            'education_level': person.education_profile['education_level'],
            'education_history': person.education_profile['education_history'],
            'major': person.education_profile['major_field'],
            'career_history': person.career_profile['career_history'],
            'career': career,
            'job_title': career.get('position', "N/A") if career else "N/A",
            'company': career.get('company', "N/A") if career else "N/A",
            'department': career.get('department', "N/A") if career else "N/A",
            'years_experience': career.get('years_experience', 'N/A') if career else 'N/A',
            # Optional color or style attributes
            'color': "#444"  # as an example
        }
        profiles[profile_uuid] = profile
    return profiles


# ------------------------------------------------------------------------------
# Helper function to generate a profile based on constraints (for parents, etc.)
# (Equivalent to generate_selected_profile in your original code)
# ------------------------------------------------------------------------------
def generate_selected_profile(constraints):
    gender = constraints.get('gender', 'All')
    country = constraints.get('country', 'All')
    min_age_diff = constraints.get('min_age_diff', 0)
    last_name = constraints.get('last_name', 'All')
    child_age = constraints.get('child_age', 25)
    relation = constraints.get('relation', 'parent')

    person = PersonProfile(filters={
        'country': country,
        'gender': gender,
        'last_name': last_name,
        'min_age_diff': min_age_diff,
        'child_age': child_age
    })
    person.generate_person_profile()

    # Adjust age for parent
    generated_age = child_age + min_age_diff + random.randint(1, 10)
    person.age = generated_age

    # Force father/mother based on relation
    if relation == 'father':
        person.gender = 'male'
    elif relation == 'mother':
        person.gender = 'female'

    # Regenerate with updated info
    person.generate_person_profile()

    name_display = person.full_name
    if hasattr(person, 'full_name_romanized') and person.full_name_romanized != person.full_name:
        name_display = f"{person.full_name} \n({person.full_name_romanized})"

    career = person.career_profile.get('career', {})
    profile_uuid = str(uuid.uuid4())

    profile = {
        'uuid': profile_uuid,
        'parents': [
            {
                'relation': 'father',
                'constraints': {
                    'country': person.country,
                    'last_name': person.last_name,
                    'gender': person.gender,
                    'min_age_diff': 16,
                    'child_age': person.age
                }
            },
            {
                'relation': 'mother',
                'constraints': {
                    'country': person.country,
                    'last_name': person.last_name,
                    'gender': person.gender,
                    'min_age_diff': 16,
                    'child_age': person.age
                }
            }
        ],
        'name': person.full_name,
        'name_display': name_display,
        'name_romanized': person.full_name_romanized,
        'age': person.age,
        'gender': person.gender,
        'country': person.country,
        'address': person.address,
        'education_level': person.education_profile['education_level'],
        'education_history': person.education_profile['education_history'],
        'major': person.education_profile['major_field'],
        'career_history': person.career_profile['career_history'],
        'career': career,
        'job_title': career.get('position', "N/A") if career else "N/A",
        'company': career.get('company', "N/A") if career else "N/A",
        'department': career.get('department', "N/A") if career else "N/A",
        'years_experience': career.get('years_experience', 'N/A') if career else 'N/A',
        'color': "#777"
    }
    return profile


# ------------------------------------------------------------------------------
# HOME ROUTE (Replacing home.py functionality)
# ------------------------------------------------------------------------------
@app.route('/')
def home():
    """
    home()
    -----------
    This replaces the Streamlit-based home.py page.
    Renders a simple homepage offering the user to go to the dashboard.
    """
    return render_template('home.html')


# ------------------------------------------------------------------------------
# PROFILE DASHBOARD ROUTE (Replacing profile_dashboard.py functionality)
# ------------------------------------------------------------------------------
@app.route('/dashboard', methods=['GET', 'POST'])
def profile_dashboard():
    """
    profile_dashboard()
    -----------
    Displays filter fields, a form for number of profiles, etc.
    On POST, it generates new profiles and updates the global PROFILES store.
    Then it displays them in a grid (HTML-based).
    """

    # Default values
    selected_country = "All"
    selected_gender = "All"
    selected_age_range = (18, 100)
    selected_education_level = "All"
    num_of_profiles = 6
    columns_per_row = 3

    if request.method == 'POST':
        # Replace Streamlit inputs with form data
        form = request.form
        selected_country = form.get("selected_country", "All")
        selected_gender = form.get("selected_gender", "All")
        age_min = int(form.get("age_min", "18"))
        age_max = int(form.get("age_max", "100"))
        selected_age_range = (age_min, age_max)
        selected_education_level = form.get("selected_education_level", "All")
        num_of_profiles = int(form.get("num_of_profiles", "6"))
        columns_per_row = int(form.get("columns_per_row", "3"))
        

        # Generate new profiles
        new_profiles = generate_profiles(num_of_profiles,
                                         selected_country,
                                         selected_gender,
                                         selected_age_range,
                                         selected_education_level)
        # Update global PROFILES with the newly created ones
        PROFILES.update(new_profiles)

    # Convert PROFILES dict to a list for easier display
    profile_list = list(PROFILES.values())

    # Render template with all needed context
    return render_template(
        'profile_dashboard.html',
        profile_list=profile_list,
        selected_country=selected_country,
        selected_gender=selected_gender,
        age_min=selected_age_range[0],
        age_max=selected_age_range[1],
        selected_education_level=selected_education_level,
        num_of_profiles=num_of_profiles,
        columns_per_row=columns_per_row
    )


# ------------------------------------------------------------------------------
# PROFILE VIEWER ROUTE (Replacing profile_viewer.py functionality)
# Dynamic route: /profile/<profile_uuid>
# ------------------------------------------------------------------------------
@app.route('/profile/<profile_uuid>', methods=['GET', 'POST'])
def profile_viewer(profile_uuid):
    """
    profile_viewer()
    -----------
    Replaces the Streamlit-based detailed profile view.
    Shows personal info, education, career, parents, etc.
    Allows "save profile" and "remove from saved" functionality.
    """

    profile = PROFILES.get(profile_uuid)
    if not profile:
        # If not found, show an error
        return render_template('error.html', message="Profile not found."), 404

    # If user clicked to add or remove from saved, handle that
    if request.method == 'POST':
        if 'save_profile' in request.form:
            SAVED_PROFILES[profile_uuid] = profile
        elif 'remove_saved' in request.form:
            if profile_uuid in SAVED_PROFILES:
                del SAVED_PROFILES[profile_uuid]
        elif 'view_parent' in request.form:
            # figure out which parent was clicked
            parent_index = int(request.form.get('parent_index'))
            parent_metadata = profile['parents'][parent_index]
            # Generate parent profile
            parent_profile = generate_selected_profile(parent_metadata['constraints'])
            # Store new parent profile
            PROFILES[parent_profile['uuid']] = parent_profile
            # Redirect to newly created parent's route
            return redirect(url_for('profile_viewer', profile_uuid=parent_profile['uuid']))
        
        return redirect(url_for('profile_viewer', profile_uuid=profile_uuid))

    # Render the template for GET requests
    return render_template('profile_viewer.html', profile=profile, saved_profiles=SAVED_PROFILES)


# ------------------------------------------------------------------------------
# SAVED PROFILES ROUTE (If needed to replicate pages/saved_profiles.py)
# ------------------------------------------------------------------------------
@app.route('/saved_profiles')
def saved_profiles():
    """
    saved_profiles()
    -----------
    Displays all saved profiles in a style similar to the original Streamlit view.
    """
    return render_template('saved_profiles.html', saved_profiles=SAVED_PROFILES)


# ------------------------------------------------------------------------------
# Error handling or other routes
# ------------------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="Page not found"), 404


# ------------------------------------------------------------------------------
# Run in debug mode
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
