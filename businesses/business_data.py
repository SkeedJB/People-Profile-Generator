business_data_info = {
    # Business Reference data
    "tier_list": ["LOW", "MID", "HIGH"],

    # Contains ranges for all tiers within each type of data
    "metrics": {
        "financial": {
            "monthly_revenue": {
                "LOW": (10000, 50000),
                "MID": (50000, 200000),
                "HIGH": (200000, 1000000)
            },
            "profit_margin": {
                "LOW": (5, 15),
                "MID": (10, 25),
                "HIGH": (15, 35)
            }},
        "customer_demographics": {
            "young": {
                "LOW": (20, 40),
                "MID": (25, 45),
                "HIGH": (30, 50)
            },
            "middle": {
                "LOW": (40, 60),
                "MID": (35, 55),
                "HIGH": (30, 50)
            },
            "senior": {
                "LOW": (10, 30),
                "MID": (15, 35),
                "HIGH": (20, 40)
            }},
        "operations": {

            "employees": {
                "LOW": (10, 25),
                "MID": (20, 50),
                "HIGH":(45, 100)
            },
            "operations_budget": {
                "LOW": (50, 70),
                "MID": (40, 60),
                "HIGH": (30, 50)
            },
            "marketing_budget": {
                "LOW": (10, 20),
                "MID": (15, 25),
                "HIGH": (20, 35)
            },
            "development_budget": {
                "LOW": (20, 30),
                "MID": (25, 35),
                "HIGH": (30, 45)
            }},
        "growth_projection": {
            "revenue_growth": {
                "LOW": (2, 10),
                "MID": (5, 15),
                "HIGH": (10, 25)
            },
            "cost_projection": {
                "LOW": (0.5, 2),
                "MID": (1, 3),
                "HIGH": (2, 5)
            }}},

    # Add the missing sector_demographics data
    "sector_demographics": {
        "Technology": {"young": 40, "middle": 45, "senior": 15},
        "Healthcare": {"young": 25, "middle": 45, "senior": 30},
        "Finance": {"young": 30, "middle": 50, "senior": 20},
        "Retail": {"young": 45, "middle": 35, "senior": 20},
        "Manufacturing": {"young": 35, "middle": 45, "senior": 20},
        "Education": {"young": 30, "middle": 45, "senior": 25},
        "Legal": {"young": 25, "middle": 50, "senior": 25},
        "Marketing": {"young": 40, "middle": 45, "senior": 15},
        "Business Services": {"young": 35, "middle": 45, "senior": 20},
        "Media": {"young": 45, "middle": 40, "senior": 15},
        "Research": {"young": 35, "middle": 45, "senior": 20},
        "General": {"young": 35, "middle": 45, "senior": 20}  # Default distribution
    },

    # Value is a static multiplier that affect base ranges     
    "trajectories": {
        "THRIVING": 1.5,
        "GROWING": 1.2,
        "STABLE": 1.0,
        "DECLINING": 0.8,
        "FAILING": 0.5
    }
}