import numpy as np
import pandas as pd
import random
from businesses.business_data import business_data_info

class Metrics():
    def __init__(self, tier, trajectory, business_sector):
        self.tier = tier
        self.trajectory = trajectory
        self.trajectory_multiplier = business_data_info["trajectories"][trajectory]
        self.business_sector = business_sector

    def generate_base_value(self):
        # Get sector demographics with fallback to "General"
        sector_dist = business_data_info["sector_demographics"].get(
            self.business_sector, 
            business_data_info["sector_demographics"]["General"]
        )
        
        # Finance values
        revenue_range = business_data_info["metrics"]["financial"]["monthly_revenue"][self.tier]
        profit_range = business_data_info["metrics"]["financial"]["profit_margin"][self.tier]
        
        # Customer Demographics
        young_customers = business_data_info["metrics"]["customer_demographics"]["young"][self.tier]
        middle_customers = business_data_info["metrics"]["customer_demographics"]["middle"][self.tier]
        senior_customers = business_data_info["metrics"]["customer_demographics"]["senior"][self.tier]

        total_customer_range = (
            young_customers[0] + middle_customers[0] + senior_customers[0], 
            young_customers[1] + middle_customers[1] + senior_customers[1]
        )
        base_total = random.uniform(*total_customer_range) * self.trajectory_multiplier
        
        # Use sector-specific distribution
        self.base_young_customers = base_total * (sector_dist["young"]/100) * random.uniform(0.95, 1.05)
        self.base_middle_customers = base_total * (sector_dist["middle"]/100) * random.uniform(0.95, 1.05)
        self.base_senior_customers = base_total * (sector_dist["senior"]/100) * random.uniform(0.95, 1.05)
        
        # Operational values
        operations_budget_range = business_data_info["metrics"]["operations"]["operations_budget"][self.tier]
        marketing_budget_range = business_data_info["metrics"]["operations"]["marketing_budget"][self.tier]
        development_budget = business_data_info["metrics"]["operations"]["development_budget"][self.tier]
        # Growth projection values
        revenue_growth_range = business_data_info["metrics"]["growth_projection"]["revenue_growth"][self.tier]
        cost_projection_range = business_data_info["metrics"]["growth_projection"]["cost_projection"][self.tier]

        # Generates base values by multiplying random num from range with trajectory
        self.base_revenue = random.uniform(*revenue_range) * self.trajectory_multiplier
        self.base_profit = random.uniform(*profit_range) * self.trajectory_multiplier
        self.base_employees = random.uniform(*business_data_info["metrics"]["operations"]["employees"][self.tier]) * self.trajectory_multiplier
        self.base_operations_budget = random.uniform(*operations_budget_range) * self.trajectory_multiplier
        self.base_marketing_budget = random.uniform(*marketing_budget_range) * self.trajectory_multiplier
        self.base_development_budget = random.uniform(*development_budget) * self.trajectory_multiplier
        self.base_revenue_growth = random.uniform(*revenue_growth_range) * self.trajectory_multiplier
        self.base_cost_projection = random.uniform(*cost_projection_range) * self.trajectory_multiplier

    def generate_quarterly_data(self):
        self.quarters = ["Q1", "Q2", "Q3", "Q4"]
        # Establishes trend factor using trajectory
        base_trend = {
            "THRIVING": 0.45,
            "GROWING": 0.25,
            "STABLE": 0.2,
            "DECLINING": -0.35,
            "FAILING": -0.55
        }[self.trajectory]

        self.quarterly_revenues = []
        self.quarterly_profits = []
        self.quarterly_young_customers = []
        self.quarterly_middle_customers = []
        self.quarterly_senior_customers = []
        self.quarterly_productivity = []
        self.quarterly_employees = []
        self.quarterly_operations_budget = []
        self.quarterly_marketing_budget = []
        self.quarterly_development_budget = []
        self.quarterly_revenue_growth = []
        self.quarterly_cost_projections = []

        # Appends every list to have an num from the range with a variation for randomness
        current_revenue = self.base_revenue
        current_profit = self.base_profit
        current_young = self.base_young_customers
        current_middle = self.base_middle_customers
        current_senior = self.base_senior_customers
        current_employees = self.base_employees
        current_ops = self.base_operations_budget
        current_marketing = self.base_marketing_budget
        current_dev = self.base_development_budget
        current_rev_growth = self.base_revenue_growth
        current_cost_projections = self.base_cost_projection

        for quarter in range(4):
            revenue_adjustment = base_trend * random.uniform(-0.5, 0.6)
            current_revenue *= (1 + revenue_adjustment)
            self.quarterly_revenues.append(current_revenue)

            current_profit = self.calculate_profit_margin(current_revenue)
            self.quarterly_profits.append(current_profit)

            demographic_adjustment = (base_trend/2) + random.uniform(-0.01, 0.01)
            current_young *= (1 + demographic_adjustment)
            current_middle *= (1 + demographic_adjustment)
            current_senior *= (1 + demographic_adjustment)
            self.quarterly_young_customers.append(current_young)
            self.quarterly_middle_customers.append(current_middle)
            self.quarterly_senior_customers.append(current_senior)


            employee_adjustment = base_trend * random.uniform(-0.2, 0.3)
            current_employees *= (1 + employee_adjustment)
            self.quarterly_employees.append(round(current_employees))

            # Calculates productivity based on num of employees and revenue
            current_productivity = self.calculate_productivity(
                self.quarterly_revenues[quarter],
                self.quarterly_employees[quarter]
            )
            self.quarterly_productivity.append(current_productivity)

            budget_adjustment = base_trend + random.uniform(-0.01, 0.01)
            current_ops *= (1 + budget_adjustment)
            current_marketing *= (1 + budget_adjustment)
            current_dev *= (1 + budget_adjustment)
            self.quarterly_operations_budget.append(current_ops)
            self.quarterly_marketing_budget.append(current_marketing)
            self.quarterly_development_budget.append(current_dev)

            current_rev_growth = self.calculate_growth_forecast()
            self.quarterly_revenue_growth.append(current_rev_growth)

            if quarter > 0:
                employee_change = (self.quarterly_employees[quarter] - self.quarterly_employees[quarter-1]) / self.quarterly_employees[quarter-1]
                revenue_change = (self.quarterly_revenues[quarter] - self.quarterly_revenues[quarter-1]) / self.quarterly_revenues[quarter-1]
            else:
                employee_change = 0
                revenue_change = 0

            cost_adjustments = self.calculate_cost_adjustments(
                employee_change=employee_change,
                revenue_change=revenue_change,
                current_quarter=quarter
            )

            current_cost_projections = self.base_cost_projection * (1 + cost_adjustments)
            self.quarterly_cost_projections.append(current_cost_projections)

    # Uses Pandas to create a dataframe using all above data
    def create_dataframe(self):
        df = pd.DataFrame({
            "Quarter": self.quarters,
            "Revenue": self.quarterly_revenues,
            "Profit": self.quarterly_profits,
            "Young Customers": self.quarterly_young_customers,
            "Middle Age Customers": self.quarterly_middle_customers,
            "Senior Customers": self.quarterly_senior_customers,
            "Employees": self.quarterly_employees,
            "Productivity": self.quarterly_productivity,
            "Operations Budget": self.quarterly_operations_budget,
            "Marketing Budget": self.quarterly_marketing_budget,
            "Development Budget": self.quarterly_development_budget,
            "Revenue Growth": self.quarterly_revenue_growth,
            "Cost Projections": self.quarterly_cost_projections
        })
        return df

    def calculate_profit_margin(self, revenue=None):
        revenue = revenue if revenue is not None else self.base_revenue

        base_margin_range = business_data_info["metrics"]["financial"]["profit_margin"][self.tier]

        revenue_range = business_data_info["metrics"]["financial"]["monthly_revenue"][self.tier]
        revenue_position = (self.base_revenue - revenue_range[0]) / (revenue_range[1] - revenue_range[0])

        # Scale impact varies by tier
        scale_impact = {
            "LOW": revenue_position * 0.03 - 0.02, 
            "MID": revenue_position * 0.03 - 0.01,
            "HIGH": revenue_position * 0.03
        }[self.tier]

        adjusted_margin = random.uniform(*base_margin_range) + scale_impact
        return revenue * (adjusted_margin / 100)

    # Older people will spend more money on average over all businesses
    def calculate_demographic_impact(self, young=None, middle=None, senior=None):
            young = young if young is not None else self.base_young_customers
            middle = middle if middle is not None else self.base_middle_customers
            senior = senior if senior is not None else self.base_senior_customers

            SPENDING_FACTORS = {
               "young": 0.8,
               "middle": 1.0,
               "senior": 1.2
            }

            demographic_multiplier = (
                (young * SPENDING_FACTORS["young"]) +
                (middle * SPENDING_FACTORS["middle"]) +
                (senior * SPENDING_FACTORS["senior"])
            ) / 100
            return demographic_multiplier

    # Adjusts base productivity with how much budget is allocated to operations
    def calculate_productivity(self, revenue, employees):
        if employees <= 0:
            return 0

        base_productivity = revenue / employees

        # Multipliers for return per employee based on sector
        industry_multipliers = {
        "IT": 1.5,
        "Manufacturing": 0.8,
        "Finance": 1.3,
        "Healthcare": 1.1,
        "Construction": 0.9,
        "Entertainment": 1.0,
        "Transport": 0.85,
        "Mining": 1.2,
        "News": 0.95
        }

        sector = self.business_sector
        multiplier = industry_multipliers.get(sector, 1.0)
        base_productivity *= multiplier
        return base_productivity


    # Calculates growth revenue based on current revenue and starting revenue 
    def calculate_growth_forecast(self, recent_revenue=None):
        growth_range = business_data_info["metrics"]["growth_projection"]["revenue_growth"][self.tier]
        base_growth = random.uniform(*growth_range) * self.trajectory_multiplier

        if recent_revenue and self.base_revenue:
            performance_factor = recent_revenue / self.base_revenue
            return base_growth * (0.5 + performance_factor/2)
        return base_growth

    def calculate_cost_adjustments(self, employee_change, revenue_change, current_quarter):
        
        # Better trajectory, less costs
        trajectory_cost_factors = {
            "THRIVING": -0.1,
            "GROWING": -0.05,
            "STABLE": 0,
            "DECLINING": 0.1,
            "FAILING": 0.2
        }

        # Higher the tier, more efficient cost management
        tier_efficiency = {
            "LOW": 1.2,
            "MID": 1.0,
            "HIGH": 0.8
        }

        employee_cost_impact = employee_change * 0.8
        revenue_impact = revenue_change * 0.3
        trajectory_impact = trajectory_cost_factors[self.trajectory]
        tier_impact = tier_efficiency[self.tier]
        market_fluctuation = random.uniform(-0.05, 0.05)

        total_adjustment = (
            (employee_cost_impact + revenue_impact) * tier_impact + trajectory_impact + market_fluctuation)
        return total_adjustment