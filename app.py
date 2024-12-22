from flask import Flask, render_template, request, redirect, url_for
from data.country_data import COUNTRIES, COUNTRY_LOCALES
from data.education_data import *
import uuid
import random
from datetime import datetime
# Generation imports
from generation.gen_person import PersonProfile

app = Flask(__name__)

PROFILES = {}
SAVED_PROFILES = {}

def build_profile_dict(person, color="#444", parents=None):
    """
    Builds the profile dictionary for a given PersonProfile object.
    """
    if parents is None:
        parents = []

    name_display = person.full_name
    if hasattr(person, 'full_name_romanized') and person.full_name_romanized != person.full_name:
        name_display = f"{person.full_name} \n({person.full_name_romanized})"

    career = person.career_profile.get('career', {})
    profile_uuid = str(uuid.uuid4())

    profile = {
        'uuid': profile_uuid,
        'parents': parents,
        'name': person.full_name,
        'name_display': name_display,
        'name_romanized': person.full_name_romanized,
        'age': person.age,
        'birth_year': person.birth_year,
        'birth_date': datetime.strptime(f"{person.birth_year}-{random.randint(1, 12)}-{random.randint(1, 28)}", "%Y-%m-%d").strftime("%B %d, %Y"),
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
        'salary': career.get('salary', 'N/A') if career else 'N/A',
        'color': color
    }
    return profile

# ------------------------------------------------------------------------------
# Helper function to generate profiles according to user filters
# ------------------------------------------------------------------------------
def generate_profiles(num_of_profiles, selected_country="All", selected_gender="All",
                      selected_age_range=(18, 100), selected_education_level="All"):
    """
    Generate a dictionary of profiles keyed by UUID, applying filters if specified.
    """
    profiles = {}
    filters = {}

    # Ensure num_of_profiles is an integer
    if isinstance(num_of_profiles, str):
        try:
            num_of_profiles = int(num_of_profiles)
        except (ValueError, TypeError):
            num_of_profiles = 6

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
        person.generate_person_profile()

        parents_info = [
            {
                'relation': 'father',
                'constraints': {'country': person.country, 'min_age_diff': 16, 'child_age': person.age}
            },
            {
                'relation': 'mother',
                'constraints': {'country': person.country, 'min_age_diff': 16, 'child_age': person.age}
            }
        ]

        profile = build_profile_dict(person, color="#444", parents=parents_info)
        profiles[profile['uuid']] = profile

    return profiles

# ------------------------------------------------------------------------------
# Helper function to generate a profile based on constraints if selected (for parents, etc.)
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

    parents_info = [
        {
            'relation': 'father',
            'constraints': {
                'country': person.country,
                'last_name': person.last_name,
                'gender': person.gender,
                'age': generated_age,
                'child_age': person.age
            }
        },
        {
            'relation': 'mother',
            'constraints': {
                'country': person.country,
                'last_name': person.last_name,
                'gender': person.gender,
                'age': generated_age,
                'child_age': person.age
            }
        }
    ]

    profile = build_profile_dict(person, color="#777", parents=parents_info)
    return profile

# ------------------------------------------------------------------------------
# HOME ROUTE
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
# PROFILE DASHBOARD ROUTE
# ------------------------------------------------------------------------------
@app.route('/dashboard', methods=['GET', 'POST'])
def profile_dashboard():
    """
    profile_dashboard()
    -----------
    Displays filter fields, a form for number of profiles, etc.
    On POST (when user clicks "Generate Profiles"), it generates new profiles and updates the global PROFILES store.
    Then it displays them in a grid (HTML-based).
    """
    # Default values
    selected_country = "All"
    selected_gender = "All"
    selected_age_range = (18, 100)
    selected_education_level = "All"
    num_of_profiles = 6  # Default value
    columns_per_row = 3  # Default value

    if request.method == 'POST':
        # Handle profile removal
        if 'remove_profile' in request.form:
            profile_uuid = request.form['remove_profile']
            if profile_uuid in PROFILES:
                del PROFILES[profile_uuid]
            return redirect(url_for('profile_dashboard'))
        if 'remove_all_profiles' in request.form:
            PROFILES.clear()
            return redirect(url_for('profile_dashboard'))

        # Get filter values from form
        form = request.form
        selected_country = form.get("selected_country", "All")
        selected_gender = form.get("selected_gender", "All")
        age_min = int(form.get("age_min", "18"))
        age_max = int(form.get("age_max", "100"))
        selected_age_range = (age_min, age_max)
        selected_education_level = form.get("selected_education_level", "All")

        # Get number of profiles to generate (fallback to 6 if blank, invalid, or < 1)
        num_of_profiles_str = form.get("num_of_profiles", "").strip()
        try:
            num_of_profiles = int(num_of_profiles_str)
            if num_of_profiles < 1:
                num_of_profiles = 6
        except (ValueError, TypeError):
            num_of_profiles = num_of_profiles_str

        # Generate new profiles with current filters
        new_profiles = generate_profiles(
            num_of_profiles,
            selected_country,
            selected_gender,
            selected_age_range,
            selected_education_level
        )
        PROFILES.update(new_profiles)

    # Convert PROFILES dict to a list for display
    profile_list = list(PROFILES.values())

    return render_template(
        'profile_dashboard.html',
        profile_list=profile_list,
        selected_country=selected_country,
        selected_gender=selected_gender,
        age_min=selected_age_range[0],
        age_max=selected_age_range[1],
        selected_education_level=selected_education_level,
        num_of_profiles=num_of_profiles,
        columns_per_row=columns_per_row,
        country_data=COUNTRY_LOCALES,
        education_levels=education_data["education_systems"]["education_levels"]
    )

# ------------------------------------------------------------------------------
# PROFILE VIEWER ROUTE
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
        return render_template('error.html', message="Profile not found."), 404

    if request.method == 'POST':
        if 'save_profile' in request.form:
            SAVED_PROFILES[profile_uuid] = profile
        elif 'remove_saved' in request.form:
            if profile_uuid in SAVED_PROFILES:
                del SAVED_PROFILES[profile_uuid]
        elif 'view_parent' in request.form:
            parent_index = int(request.form.get('parent_index'))
            parent_metadata = profile['parents'][parent_index]
            parent_profile = generate_selected_profile(parent_metadata['constraints'])
            PROFILES[parent_profile['uuid']] = parent_profile
            return redirect(url_for('profile_viewer', profile_uuid=parent_profile['uuid']))

        return redirect(url_for('profile_viewer', profile_uuid=profile_uuid))

    return render_template('profile_viewer.html', profile=profile, saved_profiles=SAVED_PROFILES)

# ------------------------------------------------------------------------------
# Filter Profiles
# ------------------------------------------------------------------------------
@app.route('/filter', methods=['GET', 'POST'])
def filter_data():
    selected_country = request.form.get('selected_country', 'All')
    selected_gender = request.form.get('selected_gender', 'All')
    age_min = int(request.form.get('age_min', '18'))
    age_max = int(request.form.get('age_max', '100'))
    selected_education_level = request.form.get('selected_education_level', 'All')
    sorted_countries = sorted(COUNTRIES, key=lambda x: x.lower)
    sorted_education_levels = sorted(education_data["education_systems"]["education_levels"])
    try:
        num_of_profiles = int(request.form.get('num_of_profiles', '6'))
    except (ValueError, TypeError):
        num_of_profiles = 6
    columns_per_row = int(request.form.get('columns_per_row', '3'))
    return render_template('filter.html', COUNTRIES=sorted_countries, education_levels=sorted_education_levels, selected_country=selected_country, selected_gender=selected_gender, age_min=age_min, age_max=age_max, selected_education_level=selected_education_level, 
                           num_of_profiles=num_of_profiles, columns_per_row=columns_per_row)

# ------------------------------------------------------------------------------
# SAVED PROFILES ROUTE
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
