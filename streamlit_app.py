from flask import Flask, render_template, request, jsonify
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get inputs from the user
    initial_investment = float(request.form['initial_investment'])
    monthly_contribution = float(request.form['monthly_contribution'])
    annual_income = float(request.form['annual_income'])
    years = int(request.form['years'])
    inflation_rate = float(request.form['inflation_rate'])
    interest_rate = float(request.form['interest_rate'])

    # Constants
    withdrawal_rate = 0.04
    target_portfolio = annual_income / withdrawal_rate
    monthly_rate = (1 + interest_rate / 100) / (1 + inflation_rate / 100) - 1
    months = years * 12

    # Calculate portfolio value over time
    portfolio_values = []
    required_values = []
    balance = initial_investment
    invested = initial_investment
    for month in range(months + 1):
        balance = balance * (1 + monthly_rate) + (monthly_contribution if month > 0 else 0)
        invested += monthly_contribution
        portfolio_values.append(balance)
        required_values.append(target_portfolio)

    # Calculate the required monthly contribution to meet the target in the desired time
    required_monthly = (target_portfolio - initial_investment * (1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months - 1) / monthly_rate)

    # Create the graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.arange(0, months + 1) / 12, y=portfolio_values, mode='lines', name='Your Portfolio', line=dict(color='blue', width=3)))
    fig.add_trace(go.Scatter(x=np.arange(0, months + 1) / 12, y=required_values, mode='lines', name='Required Portfolio', line=dict(color='green', width=2, dash='dash')))
    
    # Add the goal reached marker
    goal_reached_month = next((i for i, v in enumerate(portfolio_values) if v >= target_portfolio), None)
    if goal_reached_month is not None:
        fig.add_trace(go.Scatter(x=[goal_reached_month / 12], y=[target_portfolio], mode='markers', name='Goal Reached', marker=dict(color='red', size=10)))
    
    # Customize the layout
    fig.update_layout(
        title='FIRE Goal Progression',
        xaxis_title='Years',
        yaxis_title='Portfolio Value ($)',
        showlegend=True
    )

    # Generate graph URL
    graph_html = fig.to_html(full_html=False)

    # Generate summary message
    final_balance = portfolio_values[-1]
    adjustment_message = ''
    if final_balance >= target_portfolio:
        adjustment_message = f"🎉 Great news! You will reach your FIRE goal in approximately {goal_reached_month // 12} years!"
    else:
        adjustment_message = f"🚨 You will be short of your FIRE goal. To reach your goal, you need to increase your monthly contribution to ${required_monthly:.2f}."

    return jsonify({
        'graph_html': graph_html,
        'adjustment_message': adjustment_message
    })

if __name__ == '__main__':
    app.run(debug=True)
