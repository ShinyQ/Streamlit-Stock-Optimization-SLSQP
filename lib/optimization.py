from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value
from constant.stocks import TECH_STOCKS, OIL_GAS_STOCKS
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from scipy.optimize import minimize
import numpy as np

def linear_programming(
    total_investment,
    returns,
    proportion,
    tech_stocks,
    non_tech_stocks,
    oil_gas_stocks,
):
    st.subheader("Hasil Linear Programming")
    st.dataframe(returns)
    stocks = returns.keys()
    selected_tech_stock = [stock for stock in TECH_STOCKS if stock in stocks]
    selected_oil_gas_stock = [stock for stock in OIL_GAS_STOCKS if stock in stocks]

    # Initialize Linear Programming Problem
    model = LpProblem(name="portfolio_allocation", sense=LpMaximize)

    # Define Decision Variables
    allocation = {
        asset: LpVariable(name=f"{asset}_allocation", lowBound=0, cat="Continuous")
        for asset in returns.keys()
    }

    # Objective Function to Maximize Total Return
    model += lpSum(allocation[asset] * returns[asset][-1] for asset in returns.keys())

    # Constraints
    if tech_stocks > 0:
        model += (
            lpSum(allocation[asset] for asset in selected_tech_stock)
            == (tech_stocks / 100) * total_investment,
            "Tech_Stock_Allocation_Constraint",
        )

    if non_tech_stocks > 0:
        model += (
            lpSum(
                allocation[asset]
                for asset in allocation
                if asset not in selected_tech_stock
            )
            == (non_tech_stocks / 100) * total_investment,
            "Non_Tech_Stock_Allocation_Constraint",
        )

    # Specific Oil & Gas Stock Constraints
    if oil_gas_stocks > 0:
        model += (
            lpSum(allocation[asset] for asset in selected_oil_gas_stock)
            <= (oil_gas_stocks / 100) * total_investment,
            "Oil_Gas_Stock_Allocation_Constraint",
        )

    if proportion > 0:
        for asset in returns.keys():
            model += (
                allocation[asset] >= (proportion / 100) * total_investment,
                f"{asset}_Min_Constraint",
            )

    # Ensure Total Investment Sum Constraint
    model += (
        lpSum(allocation.values()) == total_investment,
        "Total_Investment_Constraint",
    )

    model.solve()

    if model.status == 1:
        total_return = value(model.objective)
        # Perbaikan di sini: pastikan round diterapkan dengan benar
        st.write(f'Total prediksi return bulanan: ${round(total_return / 100, 2)}')
        assets = list(returns.keys())

        # List of allocations
        allocation_values = [allocation[asset].varValue for asset in assets]
        
        # Prepare the data for the table
        allocation_df = pd.DataFrame({
            "Asset": assets,
            "Jumlah Alokasi ($)": allocation_values
        })

        # Show the table using st.table
        st.table(allocation_df)
        
        # Create a bar chart
        fig = go.Figure(data=[go.Bar(
            x=assets,  # asset names
            y=allocation_values,  # allocation values
            text=np.round(allocation_values, 2),  # display values on bars
            textposition='auto'  # position the text
        )])

        # Add title and labels
        fig.update_layout(
            margin=dict(t=5, b=10, l=0, r=0),
            xaxis_title="Saham",
            yaxis_title="Jumlah Alokasi ($)",
            template="plotly_dark"  # Optional: change theme to dark
        )

        st.plotly_chart(fig)

        return total_return
    else:
        st.error("Optimisasi Linear Programming gagal dilakukan.")
        return None

def slsqp_optimization(
    total_investment,
    returns,
    proportion,
    tech_stocks,
    non_tech_stocks,
    oil_gas_stocks,
):
    st.subheader("Hasil Optimisasi SLSQP")
    st.dataframe(returns)
    stocks = list(returns.keys())
    selected_tech_stock = [stock for stock in TECH_STOCKS if stock in stocks]
    selected_oil_gas_stock = [stock for stock in OIL_GAS_STOCKS if stock in stocks]

    # Objective Function: Negative Total Return (since we minimize)
    def objective(x):
        return -np.dot(x, [returns[asset][-1] for asset in stocks])

    # Constraints
    constraints = []

    # Total Investment Constraint
    constraints.append({
        'type': 'eq',
        'fun': lambda x: np.sum(x) - total_investment
    })

    # Tech Stocks Allocation Constraint
    if tech_stocks > 0:
        constraints.append({
            'type': 'eq',
            'fun': lambda x: np.sum([x[i] for i, asset in enumerate(stocks) if asset in selected_tech_stock]) - (tech_stocks / 100) * total_investment
        })

    # Non-Tech Stocks Allocation Constraint
    if non_tech_stocks > 0:
        constraints.append({
            'type': 'eq',
            'fun': lambda x: np.sum([x[i] for i, asset in enumerate(stocks) if asset not in selected_tech_stock]) - (non_tech_stocks / 100) * total_investment
        })

    # Oil & Gas Stocks Allocation Constraint
    if oil_gas_stocks > 0:
        constraints.append({
            'type': 'ineq',
            'fun': lambda x: (oil_gas_stocks / 100) * total_investment - np.sum([x[i] for i, asset in enumerate(stocks) if asset in selected_oil_gas_stock])
        })

    # Proportion Constraints
    if proportion > 0:
        for i in range(len(stocks)):
            constraints.append({
                'type': 'ineq',
                'fun': lambda x, i=i: x[i] - (proportion / 100) * total_investment
            })

    # Bounds for each asset allocation
    bounds = [(0, total_investment) for _ in stocks]

    # Initial Guess (equal distribution)
    initial_guess = [total_investment / len(stocks) for _ in stocks]

    # Perform Optimization
    result = minimize(
        objective,
        initial_guess,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    if result.success:
        allocation_values = result.x
        total_return = -result.fun

        # Perbaikan di sini: pastikan round diterapkan dengan benar
        st.write(f'Total prediksi return bulanan: ${round(total_return / 100, 2)}')

        # Prepare the data for the table
        allocation_df = pd.DataFrame({
            "Asset": stocks,
            "Jumlah Alokasi ($)": allocation_values
        })

        # Show the table using st.table
        st.table(allocation_df)
        
        # Create a bar chart
        fig = go.Figure(data=[go.Bar(
            x=stocks,  # asset names
            y=allocation_values,  # allocation values
            text=np.round(allocation_values, 2),  # display values on bars
            textposition='auto'  # position the text
        )])

        # Add title and labels
        fig.update_layout(
            margin=dict(t=5, b=10, l=0, r=0),
            xaxis_title="Saham",
            yaxis_title="Jumlah Alokasi ($)",
            template="plotly_dark"  # Optional: change theme to dark
        )

        st.plotly_chart(fig)

        return total_return
    else:
        st.error("Optimisasi SLSQP gagal dilakukan.")
        return None
