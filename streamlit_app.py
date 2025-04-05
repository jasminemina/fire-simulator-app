import streamlit as st

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

# --- UI setup ---
st.set_page_config(page_title="FIRE Calculator", layout="centered")
st.title("FIRE (Financial Independence) Simulator")

st.markdown("""
This tool helps you estimate how long it will take to reach **financial independence** based on your savings, investment returns, and desired lifestyle.

You'll see how your money grows over time and when you can start safely withdrawing from your portfolio.
""")

# --- Inputs ---
st.header("Your Inputs")

initial = st.number_input(
    "Current Investment Amount ($)", 
    value=55000, 
    step=5000, 
    help="How much you've already saved or invested."
)

monthly = st.number_input(
    "Monthly Contribution ($)", 
    value=2000, 
    step=1000, 
    help="How much you're adding to your investments each month."
)

annual_return = st.slider(
    "Expected Annual Return (%)", 
    0.0, 15.0, 7.0, 
    help="Average annual investment return (e.g. stock market ~7%)."
)

inflation = st.slider(
    "Expected Inflation Rate (%)", 
    0.0, 10.0, 2.5, 
    help="Used to adjust future value to today's dollars."
)

spend = st.number_input(
    "Your Desired Annual Spending in Retirement ($)", 
    value=100000, 
    step=5000,
    help="How much you want to live on each year after reaching FIRE."
)

withdraw_rate = st.slider(
    "Safe Withdrawal Rate (%)", 
    2.0, 6.0, 4.0, 
    help="The percentage you can safely withdraw from your portfolio annually."
)

adjust = st.checkbox("Adjust for Inflation", value=True)

# --- Calculations ---
fire_number = fire_number_calc(spend, withdraw_rate)
history, years, crossover = calculate_growth(
    initial, monthly, annual_return/100, inflation/100, fire_number, adjust_inflation=adjust
)

# --- Output ---
st.header("Your Results")

st.metric("FIRE Number", f"${fire_number:,.0f}", help="This is the total amount you need invested to safely withdraw your desired annual income.")
st.metric("Years to Reach FIRE", f"{years:.1f}", help="How long it will take to reach your FIRE number.")
if crossover:
    st.metric("When Compound Interest > Contributions", f"{crossover:.1f} years", help="When your portfolio starts growing faster than you're contributing.")

st.markdown("### Investment Growth Over Time")
st.line_chart({ "Portfolio Value": [val for _, val in history] })
