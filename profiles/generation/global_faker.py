from faker import Faker
from profiles.data.country_data import COUNTRY_LOCALES
GLOBAL_FAKER_INSTANCES = {}

def get_faker(locale=list(COUNTRY_LOCALES.values())[0]):
    if locale not in GLOBAL_FAKER_INSTANCES:
        GLOBAL_FAKER_INSTANCES[locale] = Faker(locale=locale)
    return GLOBAL_FAKER_INSTANCES[locale]
