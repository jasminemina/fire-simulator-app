import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# --- FIRE logic ---
def calculate_growth(initial, monthly, rate, inflation, target, adjust_inflation=True):
    balance = initial
    contributions = 0
    history = []
    months = 0
    crossover = None

    while balance < target and months < 1200:
        balance *= (1 + rate / 12)
        balance += monthly
        contributions += monthly
        if adjust_inflation:
            balance /= (1 + inflation / 12)
        history.append((months / 12, balance))
        if crossover is None and balance - initial > contributions:
            crossover = months / 12
        months += 1

    return history, months / 12, crossover

def fire_number_calc(spend, rate):
    return spend / (rate / 100)

# --- UI ---
st.set_page_config(page_title="FIRE Calculator", layout="centered")

st.title("FIRE Simulator")

st.header("Inputs")
initial = st.number_input("Initial Investment ($)", value=55000, step=1000)
monthly = st.number_input("Monthly Contribution ($)", value=2000, step=100)
annual_return = st.slider("Annual Return (%)", 0.0, 15.0, 7.0)
inflation = st.slider("Inflation Rate (%)", 0.0, 10.0, 2.5)
target = st.number_input("Target FIRE Amount ($)", value=3000000, step=100000)
withdraw_rate = st.slider("Withdrawal Rate (%)", 2.0, 6.0, 4.0)
spend = st.number_input("Your Desired Annual Spending ($)", value=100000)
adjust = st.checkbox("Adjust for Inflation", value=True)

# --- Calculate ---
fire_number = fire_number_calc(spend, withdraw_rate)
history, years, crossover = calculate_growth(
    initial, monthly, annual_return/100, inflation/100, target, adjust_inflation=adjust
)

# --- Output ---
st.header("Results")
st.metric("Your FIRE Number", f"${fire_number:,.0f}")
st.metric("Years to Reach Target", f"{years:.1f}")
if crossover:
    st.metric("Compound > Contributions After", f"{crossover:.1f} years")

st.line_chart({ "Portfolio Value": [val for _, val in history] })