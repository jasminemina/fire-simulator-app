
# ---- FIRE Calculation Logic ----
def calculate_growth(initial, monthly, rate, inflation, fire_target, adjust_inflation=True):
    balance = initial
    contributions = 0
    history = []
    months = 0
    crossover = None

    while balance < fire_target and months < 1200:  # Max 100 years
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

def fire_number_calc(spending, withdrawal_rate):
    return spending / (withdrawal_rate / 100)

# ---- Streamlit UI ----
st.set_page_config(page_title="FIRE Calculator", layout="centered")
st.title("FIRE (Financial Independence) Simulator")

st.markdown("""
Use this calculator to see how long it might take you to reach **Financial Independence** — the point when your investments can fund your lifestyle forever.
""")

# ---- User Inputs ----
st.header("Your Financial Inputs")

initial = st.number_input(
    "Current Investment Amount ($)", 
    min_value=0, value=55000, step=5000,
    help="Your current total invested savings."
)

monthly = st.number_input(
    "Monthly Contribution ($)", 
    min_value=0, value=2000, step=1000,
    help="How much you're investing each month."
)

spending = st.number_input(
    "Desired Annual Spending in Retirement ($)", 
    min_value=10000, value=100000, step=5000,
    help="How much you want to spend annually once you're financially independent."
)

withdrawal_rate = st.slider(
    "Safe Withdrawal Rate (%)", 2.0, 6.0, 4.0,
    help="Typically between 3-4%. Lower means more conservative."
)

return_rate = st.slider(
    "Expected Annual Return (%)", 0.0, 15.0, 7.0,
    help="Long-term average market return is around 7%."
)

inflation = st.slider(
    "Expected Inflation Rate (%)", 0.0, 10.0, 2.5,
    help="Used to adjust future values into today's dollars."
)

adjust_inflation = st.checkbox("Adjust for Inflation", value=True)

# ---- FIRE Calculations ----
fire_target = fire_number_calc(spending, withdrawal_rate)
history, years_to_fire, crossover = calculate_growth(
    initial, monthly, return_rate / 100, inflation / 100, fire_target, adjust_inflation=adjust_inflation
)

# ---- Results ----
st.header("Results")
st.metric("FIRE Number", f"${fire_target:,.0f}", help="Total invested amount needed to retire safely.")
st.metric("Years to FIRE", f"{years_to_fire:.1f} years")

if crossover:
    st.metric("Compound Interest Crossover", f"{crossover:.1f} years", help="When your growth outpaces your contributions.")

# ---- Chart ----
st.subheader("Investment Growth Over Time")
st.line_chart({ "Portfolio Value": [val for _, val in history] })
