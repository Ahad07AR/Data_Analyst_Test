import pandas as pd
import random
import plotly.express as px
from dash import Dash, dcc, html

# Sample Dataset
data = {
    "Month": pd.date_range(start="2024-01-01", periods=12, freq="ME").strftime("%b-%Y"),
    "Expense Category": ["Operations", "Marketing", "Research", "IT"] * 3,
    "Amount": [random.randint(10000, 50000) for _ in range(12)],
    "Region": ["North", "South", "East", "West"] * 3,
    "Sales": [random.randint(50000, 150000) for _ in range(12)],
    "Type": ["AP", "AR"] * 6,
    "Aging Bucket": ["0-30 days", "31-60 days", "61-90 days", "90+ days"] * 3,
}
# Create DataFrame
df = pd.DataFrame(data)

# Expense Summary
expense_summary = df.groupby("Expense Category")["Amount"].sum().reset_index()

# Sales Summary
sales_summary = df.groupby("Region")["Sales"].sum().reset_index()

# AP and AR Aging Summary
ap_ar_summary = df.groupby(["Type", "Aging Bucket"])["Amount"].sum().reset_index()

# ----------------------
# 2. Build Dashboard
# ----------------------
# Initialize the Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("CFO Dashboard", style={"textAlign": "center", "color": "#2c3e50"}),

    # Expense Summary Section
    html.Div([
        html.H3("Expense Summary"),
        dcc.Graph(
            id="expense-chart",
            figure=px.bar(
                expense_summary,
                x="Expense Category",
                y="Amount",
                title="Total Expenses by Category",
                color="Expense Category",
                text_auto=True
            ).update_layout(xaxis_title="Category", yaxis_title="Amount ($)")
        )
    ], style={"width": "48%", "display": "inline-block", "padding": "10px"}),

    # Sales Summary Section
    html.Div([
        html.H3("Sales Summary"),
        dcc.Graph(
            id="sales-chart",
            figure=px.pie(
                sales_summary,
                names="Region",
                values="Sales",
                title="Sales by Region",
                hole=0.4
            )
        )
    ], style={"width": "48%", "display": "inline-block", "padding": "10px"}),

    # AP and AR Aging Summary Section
    html.Div([
        html.H3("AP and AR Aging Summary"),
        dcc.Graph(
            id="ap-ar-chart",
            figure=px.bar(
                ap_ar_summary,
                x="Aging Bucket",
                y="Amount",
                color="Type",
                title="AP and AR Aging Overview",
                barmode="group",
                text_auto=True
            ).update_layout(xaxis_title="Aging Bucket", yaxis_title="Amount ($)")
        )
    ], style={"width": "98%", "padding": "10px", "margin-top": "20px"})
])

# ----------------------
# 3. Run the App
# ----------------------
if __name__ == "__main__":
    app.run_server(debug=True)

[[ports]]
localPort = 8050
externalPort = 80