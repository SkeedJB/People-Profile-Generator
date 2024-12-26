from businesses.metrics_gen import Metrics
from businesses.business_data import business_data_info
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import uuid
from profiles.generation.providers.company_name_provider import CompanyNameProvider
from profiles.generation.global_faker import get_faker
from profiles.generation.gen_career import CareerGenerator
from businesses.business_utils import generate_business_name_and_id, get_business_name_from_uuid

class Business():
    def __init__(self, business_uuid=None, sector=None):
        try:
            self.faker = get_faker()
            self.faker.add_provider(CompanyNameProvider)
            
            self.fig = None
            self.business_id = business_uuid
            
            # If we have a business_uuid, use it to seed ALL random choices
            if business_uuid:
                # Convert UUID to integer for seeding
                seed_int = int(uuid.UUID(business_uuid).int & (2**32-1))
                # Seed all random generators
                random.seed(seed_int)
                self.faker.seed_instance(seed_int)
                np.random.seed(seed_int)
                
                # Get the business name first (this should match what's in the profile)
                self.business_name = get_business_name_from_uuid(business_uuid, sector)
                
                # Now generate other attributes with the same seed
                self.business_tier = random.choice(business_data_info["tier_list"])
                self.business_sector = sector or self._generate_sector()
                self.business_trajectory = random.choice(list(business_data_info["trajectories"].keys()))
                
                # Reset seeds after initialization
                random.seed()
                self.faker.seed_instance()
                np.random.seed()
            else:
                # For new businesses, generate everything fresh
                self.business_name, self.business_id = generate_business_name_and_id(sector or self._generate_sector())
                self.business_sector = sector or self._generate_sector()
                self.business_tier = random.choice(business_data_info["tier_list"])
                self.business_trajectory = random.choice(list(business_data_info["trajectories"].keys()))
            
            # Set trajectory multiplier
            self.business_trajectory_multiplier = business_data_info["trajectories"][self.business_trajectory]
            
            # Initialize dashboard
            self.initialize_dashboard()
            
        except Exception as e:
            print(f"Error in Business initialization: {str(e)}")
            raise

    def _generate_company_name(self):
        """Generate a company name based on sector"""
        return self.faker.company_name(sector=self.business_sector)

    def generate_business_performance(self):
        """Generate business metrics using the business_id as seed"""
        if self.business_id:
            # Re-seed with the same business_id for consistent metrics
            seed_int = int(uuid.UUID(self.business_id).int & (2**32-1))
            random.seed(seed_int)
            np.random.seed(seed_int)
        
        # Create metrics instance
        self.business_instance = Metrics(
            self.business_tier,
            self.business_trajectory,
            self.business_sector
        )
        
        # Generate all metrics
        self.business_instance.generate_base_value()
        self.business_instance.generate_quarterly_data()
        self.business_df = self.business_instance.create_dataframe()
        
        # Reset seeds
        if self.business_id:
            random.seed()
            np.random.seed()

    # Creates initial dashboard with subplots
    def initialize_dashboard(self):
        self.fig = make_subplots(
            rows=3, cols=2,
            specs=[[{"type": "xy"}, {"type": "xy"}],
                [{"type": "xy"}, {"type": "xy"}],
                [{"type": "pie"}, {"type": "xy"}]],
            subplot_titles=(
                "Revenue and Profit Trends",
                "Customer Demographics by Quarter",
                "Productivity Metrics",
                "Revenue Growth Forecast",
                "Budget Distribution",
                "Cost Projections"
            )
        )

    def create_dashboard(self):
        self.generate_business_performance()
        self.plot_all_metrics()
        self.update_layout()
        self.add_stats_annotations()
        return self.fig

    def plot_all_metrics(self):
        self.plot_revenue_profit()
        self.plot_demographics()
        self.plot_productivity()
        self.plot_growth_forecast()
        self.plot_budget_distribution()
        self.plot_cost_projection()

    def update_layout(self):
        self.fig.update_layout(
            height=1200,
            width=1500,
            showlegend=True,
            title_text=f"Business Metrics Dashboard - {self.business_name}<br>Tier: {self.business_tier} | Trajectory: {self.business_trajectory}<br>Sector: {self.business_sector}",
            title_x=0.5,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        self.fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        self.fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    def plot_revenue_profit(self):
        quarterly_data = self.business_df

        # Revenue trace
        self.fig.add_trace(
            go.Scatter(
                x=quarterly_data["Quarter"],
                y=quarterly_data["Revenue"],
                name="Revenue",
                mode="lines+markers",
                line=dict(color="forestgreen", width=2),
                hovertemplate="Quarter: %{x}<br>" +
                            "Revenue: $%{y:,.2f}<br>" +
                            "<extra></extra>"
            ),
            row=1, col=1
        )
        
        # Profit trace
        self.fig.add_trace(
            go.Scatter(
                x=quarterly_data["Quarter"],
                y=quarterly_data["Profit"],
                name="Profit",
                mode="lines+markers",
                line=dict(color="mediumseagreen", width=2, dash="dash"),
                hovertemplate="Quarter: %{x}<br>" +
                            "Profit: $%{y:,.2f}<br>" +
                            "<extra></extra>"
            ),
            row=1, col=1
        )

    def plot_demographics(self):
        quarterly_data = self.business_df
        
        # Young customers
        self.fig.add_trace(
            go.Bar(
                x=quarterly_data["Quarter"],
                y=quarterly_data["Young Customers"],
                name="Young",
                marker_color="lightsteelblue",
                hovertemplate="Quarter: %{x}<br>" +
                            "Young Customers: %{y:,.0f}<br>" +
                            "<extra></extra>"
            ),
            row=1, col=2
        )
        
        # Middle age customers
        self.fig.add_trace(
            go.Bar(
                x=quarterly_data["Quarter"],
                y=quarterly_data["Middle Age Customers"],
                name="Middle Age",
                marker_color="royalblue",
                hovertemplate="Quarter: %{x}<br>" +
                            "Middle Age Customers: %{y:,.0f}<br>" +
                            "<extra></extra>"
            ),
            row=1, col=2
        )
        
        # Senior customers
        self.fig.add_trace(
            go.Bar(
                x=quarterly_data["Quarter"],
                y=quarterly_data["Senior Customers"],
                name="Senior",
                marker_color="darkblue",
                hovertemplate="Quarter: %{x}<br>" +
                            "Senior Customers: %{y:,.0f}<br>" +
                            "<extra></extra>"
            ),
            row=1, col=2
        )

    def plot_productivity(self):
        quarterly_data = self.business_df
        self.fig.add_trace(
            go.Scatter(
                x=quarterly_data["Quarter"],
                y=quarterly_data["Productivity"],
                name="Productivity",
                mode="lines+markers",
                line=dict(color="darkorange", width=2),
                hovertemplate="Quarter: %{x}<br>Productivity: $%{y:,.2f}<br><extra></extra>"
            ),
            row=2, col=1
        )

    def plot_growth_forecast(self):
        quarterly_data = self.business_df
        self.fig.add_trace(
            go.Scatter(
                x=quarterly_data["Quarter"],
                y=quarterly_data["Revenue Growth"],
                name="Growth Rate",
                fill='tozeroy',
                fillcolor='rgba(0, 255, 0, 0.1)',
                line=dict(color="green", width=2),
                hovertemplate="Quarter: %{x}<br>Growth Rate: %{y:.1f}%<br><extra></extra>"
            ),
            row=2, col=2
        )

    def plot_budget_distribution(self):
        latest = self.business_df.iloc[-1]
        self.fig.add_trace(
            go.Pie(
                values=[
                    latest["Operations Budget"],
                    latest["Marketing Budget"],
                    latest["Development Budget"]
                ],
                labels=["Operations", "Marketing", "Development"],
                hole=0.3,
                pull=[0.2, 0, 0],
                marker_colors=["lightblue", "skyblue", "steelblue"],
                hovertemplate="Category: %{label}<br>Budget: %{value:,.2f}<br>Percentage: %{percent}<extra></extra>"
            ),
            row=3, col=1
        )

    def plot_cost_projection(self):
        quarterly_data = self.business_df
        self.fig.add_trace(
            go.Scatter(
                x=quarterly_data["Quarter"],
                y=quarterly_data["Cost Projections"],
                name="Cost Projections",
                mode="lines+markers",
                line=dict(color="indianred", width=2),
                hovertemplate="Quarter: %{x}<br>Projected Cost: %{y:,.2f}<br><extra></extra>"
            ),
            row=3, col=2
        )

    # Formats large numbers with commas
    def format_number(self, value):
        return f"{value:,.0f}" if abs(value) >= 1000 else f"{value:,.2f}"

    # Calculates and Annotates Metrics
    def calculate_stats(self, plot_type):
        if plot_type == "revenue_profit":
            avg_revenue = np.mean(self.business_instance.quarterly_revenues)
            avg_profit = np.mean(self.business_instance.quarterly_profits)
            profit_margin = (avg_profit / avg_revenue) * 100 if avg_revenue > 0 else 0
            return dict(
                avg_revenue=avg_revenue,
                avg_profit=avg_profit,
                profit_margin=profit_margin
            )
        
        elif plot_type == "demographics":
            young = np.mean(self.business_instance.quarterly_young_customers)
            middle = np.mean(self.business_instance.quarterly_middle_customers)
            senior = np.mean(self.business_instance.quarterly_senior_customers)
            total = young + middle + senior
            return dict(
                young_pct=(young/total * 100),
                middle_pct=(middle/total * 100),
                senior_pct=(senior/total * 100)
            )
        
        elif plot_type == "productivity":
            avg_productivity = np.mean(self.business_instance.quarterly_productivity)
            productivity_change = ((self.business_instance.quarterly_productivity[-1] -
                                self.business_instance.quarterly_productivity[0]) /
                                self.business_instance.quarterly_productivity[0] * 100)
            return dict(
                avg_productivity=avg_productivity,
                productivity_change=productivity_change
            )
        
        elif plot_type == "growth_forecast":
            avg_growth = np.mean(self.business_instance.quarterly_revenue_growth)
            latest_growth = self.business_instance.quarterly_revenue_growth[-1]
            return dict(
                avg_growth=avg_growth,
                latest_growth=latest_growth
            )
        
        elif plot_type == "budget":
            total_budget = (self.business_instance.quarterly_operations_budget[-1] +
                        self.business_instance.quarterly_marketing_budget[-1] +
                        self.business_instance.quarterly_development_budget[-1])
            
            ops_percent = (self.business_instance.quarterly_operations_budget[-1] / total_budget * 100)
            marketing_percent = (self.business_instance.quarterly_marketing_budget[-1] / total_budget * 100)
            dev_percent = (self.business_instance.quarterly_development_budget[-1] / total_budget * 100)
            return dict(
                ops_percent=ops_percent,
                marketing_percent=marketing_percent,
                dev_percent=dev_percent
            )
        
        elif plot_type == "costs":
            avg_costs = np.mean(self.business_instance.quarterly_cost_projections)
            cost_trend = ((self.business_instance.quarterly_cost_projections[-1] -
                        self.business_instance.quarterly_cost_projections[0]) /
                        self.business_instance.quarterly_cost_projections[0] * 100)
            return dict(
                avg_costs=avg_costs,
                cost_trend=cost_trend
            )

    def add_stats_annotations(self):
        # Calculate all stats
        stats = {}
        for plot_type in ["revenue_profit", "demographics", "productivity", 
                        "growth_forecast", "budget", "costs"]:
            stats[plot_type] = self.calculate_stats(plot_type)
        
        # Revenue and Profit annotation (row 1, col 1)
        self.fig.add_annotation(
            text=f"Average Revenue: ${self.format_number(stats['revenue_profit']['avg_revenue'])}<br>" +
                f"Average Profit: ${self.format_number(stats['revenue_profit']['avg_profit'])}<br>" +
                f"Profit Margin: {stats['revenue_profit']['profit_margin']:.1f}%",
            xref="paper", yref="paper",
            x=0.16, y=0.72,
            showarrow=False,
            bgcolor="white",
            bordercolor="lightgray",
            borderwidth=1
        )
        
        # Demographics annotation (row 1, col 2)
        self.fig.add_annotation(
            text=f"Average Distribution:<br>" +
                f"Young: {stats['demographics']['young_pct']:.1f}%<br>" +
                f"Middle: {stats['demographics']['middle_pct']:.1f}%<br>" +
                f"Senior: {stats['demographics']['senior_pct']:.1f}%",
            xref="paper", yref="paper",
            x=0.85, y=0.72,
            showarrow=False,
            bgcolor="white",
            bordercolor="lightgray",
            borderwidth=1
        )
        
        # Productivity annotation (row 2, col 1)
        self.fig.add_annotation(
            text=f"Average Productivity (Per Employee): ${self.format_number(stats['productivity']['avg_productivity'])}<br>" +
                f"Productivity Change: {stats['productivity']['productivity_change']:+.1f}%",
            xref="paper", yref="paper",
            x=0.16, y=0.28,
            showarrow=False,
            bgcolor="white",
            bordercolor="lightgray",
            borderwidth=1
        )
        
        # Growth Forecast annotation (row 2, col 2)
        self.fig.add_annotation(
            text=f"Average Growth Rate: {stats['growth_forecast']['avg_growth']:.1f}%<br>" +
                f"Latest Growth Rate: {stats['growth_forecast']['latest_growth']:.1f}%",
            xref="paper", yref="paper",
            x=0.85, y=0.28,
            showarrow=False,
            bgcolor="white",
            bordercolor="lightgray",
            borderwidth=1
        )
        
        # Budget annotation (row 3, col 1)
        self.fig.add_annotation(
            text=f"Operations: {stats['budget']['ops_percent']:.1f}%<br>" +
                f"Marketing: {stats['budget']['marketing_percent']:.1f}%<br>" +
                f"Development: {stats['budget']['dev_percent']:.1f}%",
            xref="paper", yref="paper",
            x=0.16, y=-0.05,
            showarrow=False,
            bgcolor="white",
            bordercolor="lightgray",
            borderwidth=1
        )
        
        # Costs annotation (row 3, col 2)
        self.fig.add_annotation(
            text=f"Average Costs: ${self.format_number(stats['costs']['avg_costs'])}<br>" +
                f"Cost Trend: {stats['costs']['cost_trend']:+.1f}%",
            xref="paper", yref="paper",
            x=0.85, y=-0.05,
            showarrow=False,
            bgcolor="white",
            bordercolor="lightgray",
            borderwidth=1
        )

    def _generate_sector(self):
        """Generate a random business sector if none is provided"""
        sectors = ["Technology", "Healthcare", "Finance", "Retail", "Manufacturing", 
                   "Education", "Legal", "Marketing", "Business Services", "Media", 
                   "Research", "General"]
        return random.choice(sectors)