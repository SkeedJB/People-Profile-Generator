import uuid
from profiles.generation.providers.company_name_provider import CompanyNameProvider
from profiles.generation.global_faker import get_faker

def generate_business_name_and_id(sector: str = "General") -> tuple:
    """Generate a consistent company name and ID pair"""
    faker = get_faker()
    faker.add_provider(CompanyNameProvider)
    
    # First generate a UUID
    business_id = str(uuid.uuid4())
    
    # Use that UUID to seed the faker
    seed_int = int(uuid.UUID(business_id).int & (2**32-1))
    faker.seed_instance(seed_int)
    
    # Generate company name based on sector with seeded faker
    company_name = faker.company_name(sector=sector)
    
    # Reset the faker seed
    faker.seed_instance()
    
    return company_name, business_id

def get_business_name_from_uuid(business_uuid: str, sector: str = "General") -> str:
    """
    Get a consistent business name for a given UUID and sector.
    This ensures the same UUID always generates the same name.
    """
    faker = get_faker()
    faker.add_provider(CompanyNameProvider)
    
    # Seed the faker with the UUID
    seed_int = int(uuid.UUID(business_uuid).int & (2**32-1))
    faker.seed_instance(seed_int)
    
    # Generate the name
    company_name = faker.company_name(sector=sector)
    
    # Reset the faker seed
    faker.seed_instance()
    
    return company_name 