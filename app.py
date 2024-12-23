from flask import Flask, render_template, request, redirect, url_for
import asyncio
import uuid
import random
from datetime import datetime

# Data
from data.country_data import COUNTRIES, COUNTRY_LOCALES
from data.education_data import education_data
# Generation
from generation.gen_person import PersonProfile

app = Flask(__name__)

PROFILES = {}
SAVED_PROFILES = {}

def build_profile_dict(person, color="#444", parents=None):
    """
    Builds a dictionary representation of a PersonProfile.
    """
    if parents is None:
        parents = []

    name_display = person.full_name
    if hasattr(person, 'full_name_romanized') and person.full_name_romanized and person.full_name_romanized != person.full_name:
        name_display = f"{person.full_name}\n({person.full_name_romanized})"

    # Process education history: use years provided by the generated data
    education_history = []
    for entry in person.education_profile.get('education_history', []):
        level_str = entry.get('level', 'Unknown')
        
        # Field should be 'General' for Elementary, Middle, High School, and Associates level
        if level_str in ["Elementary School", "Middle School", "High School", "Associates"]:
            field = "General"
        else:
            field = entry.get('field_of_study', person.education_profile.get('major_field', 'N/A'))

        processed_entry = {
            'level': level_str,
            'field_of_study': field,
            'start_year': entry.get('start_year', 'N/A'),
            'end_year': entry.get('end_year', 'N/A'),
            'duration': entry.get('duration', 0)
        }
        education_history.append(processed_entry)

    # Sort education history by start_year if it's numeric, descending
    education_history.sort(
        key=lambda x: x['start_year'] if isinstance(x['start_year'], int) else 9999,
        reverse=True
    )

    # Process career history: read from person.career_profile
    career_history = []
    for job in person.career_profile.get('career_history', []):
        processed_job = {
            'position': job.get('position', 'Unknown'),
            'company': job.get('company', 'Unknown'),
            'department': job.get('department', 'N/A'),
            'level': job.get('level', 'entry_level'),
            'field': job.get('field', 'N/A'),
            'salary': job.get('salary', 'N/A'),
            'start_year': job.get('start_year', 'N/A'),
            'end_year': job.get('end_year', 'Present'),
            'duration': job.get('duration', 0)
        }
        career_history.append(processed_job)

    # Get current career info
    career = person.career_profile.get('career', {})
    if not career:
        career = {'position': 'N/A', 'company': 'N/A', 'department': 'N/A', 'salary': 'N/A'}

    profile_uuid = str(uuid.uuid4())

    profile = {
        'uuid': profile_uuid,
        'parents': parents,
        'name': person.full_name,
        'name_display': name_display,
        'name_romanized': person.full_name_romanized,
        'age': person.age,
        'birth_year': person.birth_year,
        'birth_date': datetime.strptime(
            f"{person.birth_year}-{random.randint(1, 12)}-{random.randint(1, 28)}",
            "%Y-%m-%d"
        ).strftime("%B %d, %Y"),
        'gender': person.gender,
        'country': person.country,
        'address': person.address,
        'education_level': person.education_profile.get('education_level', 'N/A'),
        'education_history': education_history,
        'major': person.education_profile.get('major_field', 'N/A'),
        'career_history': career_history,
        'career': career,
        'job_title': career.get('position', "N/A"),
        'company': career.get('company', "N/A"),
        'department': career.get('department', "N/A"),
        'years_experience': career.get('years_experience', 'N/A'),
        'salary': career.get('salary', 'N/A'),
        'color': color
    }
    return profile

async def generate_one_profile(filters):
    """
    Creates a single PersonProfile, awaits its asynchronous generation,
    then builds and returns a dictionary of the final data.
    """
    person = PersonProfile(filters=filters)
    await person.generate_person_profile()

    # Optional: define parent placeholders
    parents_info = [
        {
            'relation': 'father',
            'constraints': {
                'country': person.country,
                'min_age_diff': 16,
                'child_age': person.age
            }
        },
        {
            'relation': 'mother',
            'constraints': {
                'country': person.country,
                'min_age_diff': 16,
                'child_age': person.age
            }
        }
    ]

    # Build final dictionary
    return build_profile_dict(person, color="#444", parents=parents_info)

async def generate_profiles_async(num_of_profiles=6,
                                  selected_country="All", 
                                  selected_gender="All",
                                  selected_age_range=(18, 100), 
                                  selected_education_level="All"):
    """
    Generates multiple profiles concurrently. Returns a dictionary keyed by UUID.
    """
    # Build filters based on user input
    filters = {}
    if selected_country and selected_country != "All":
        filters['country'] = selected_country
    if selected_gender and selected_gender != "All":
        filters['gender'] = selected_gender
    if selected_age_range != (18, 100):
        filters['age_range'] = selected_age_range
    if selected_education_level and selected_education_level != "All":
        filters['education_level'] = selected_education_level

    # Make sure num_of_profiles is an integer
    try:
        num_of_profiles = int(num_of_profiles)
        if num_of_profiles < 1:
            num_of_profiles = 6
    except (ValueError, TypeError):
        num_of_profiles = 6

    tasks = []
    for _ in range(num_of_profiles):
        tasks.append(asyncio.create_task(generate_one_profile(filters)))

    # Gather all tasks concurrently
    results_list = await asyncio.gather(*tasks)

    # Convert the list of profiles (dicts) into a uuid-keyed dictionary
    final_profiles_dict = {}
    for p_dict in results_list:
        final_profiles_dict[p_dict['uuid']] = p_dict

    return final_profiles_dict

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def profile_dashboard():
    """
    Profile dashboard route. On POST, triggers generation of new profiles.
    """
    # Defaults
    selected_country = "All"
    selected_gender = "All"
    selected_age_range = (18, 100)
    selected_education_level = "All"
    num_of_profiles = 6
    columns_per_row = 3

    if request.method == 'POST':
        # Handle 'remove profile'
        if 'remove_profile' in request.form:
            profile_uuid = request.form['remove_profile']
            if profile_uuid in PROFILES:
                del PROFILES[profile_uuid]
            return redirect(url_for('profile_dashboard'))

        # Handle 'remove all profiles'
        if 'remove_all_profiles' in request.form:
            PROFILES.clear()
            return redirect(url_for('profile_dashboard'))

        # Get filter values
        form = request.form
        selected_country = form.get("selected_country", "All")
        selected_gender = form.get("selected_gender", "All")
        age_min = int(form.get("age_min", 18))
        age_max = int(form.get("age_max", 100))
        selected_age_range = (age_min, age_max)
        selected_education_level = form.get("selected_education_level", "All")
        num_of_profiles_input = form.get("num_of_profiles", "6").strip()

        # Generate new profiles asynchronously
        new_profiles = asyncio.run(
            generate_profiles_async(
                num_of_profiles=num_of_profiles_input,
                selected_country=selected_country,
                selected_gender=selected_gender,
                selected_age_range=selected_age_range,
                selected_education_level=selected_education_level
            )
        )
        # Update global PROFILES
        PROFILES.update(new_profiles)

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

# Profile viewer route
@app.route('/profile/<profile_uuid>', methods=['GET', 'POST'])
def profile_viewer(profile_uuid):
    """
    Detailed profile view. Also allows saving/removing from saved,
    plus generating parent profiles when a user clicks "view_parent."
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
            parent_index = int(request.form.get('parent_index', 0))
            parent_metadata = profile['parents'][parent_index]
            # "generate_selected_profile" can remain synchronous or asynchronous, as needed.
            return redirect(url_for('profile_dashboard'))

        return redirect(url_for('profile_viewer', profile_uuid=profile_uuid))

    return render_template('profile_viewer.html', profile=profile, saved_profiles=SAVED_PROFILES)

@app.route('/saved_profiles')
def saved_profiles():
    return render_template('saved_profiles.html', saved_profiles=SAVED_PROFILES)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="Page not found"), 404

if __name__ == '__main__':
    app.run(debug=True)
