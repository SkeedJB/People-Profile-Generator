from businesses.business_creation import Business
from businesses.business_data import business_data_info

def generate_business_dashboard(business_uuid=None):
    """
    Generates a business dashboard for a given UUID or creates a new random business.
    
    Args:
        business_uuid (str, optional): UUID of existing business. If None, creates new business.
    
    Returns:
        tuple: (Business object, HTML dashboard)
    """
    # Create business instance (either new or existing based on UUID)
    business = Business(business_uuid)
    
    # Generate the dashboard
    dashboard = business.create_dashboard()
    
    # Convert to HTML (without full HTML wrapper, just the plot)
    dashboard_html = dashboard.to_html(
        full_html=False,
        include_plotlyjs=False
    )
    
    return business, dashboard_html

