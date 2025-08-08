import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="💰 Budget Tracker (Free)", layout="centered")

# --- Initialize session ---
if "form_date" not in st.session_state:
    st.session_state.form_date = datetime.date.today()

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Note"])

if "t_type" not in st.session_state:
    st.session_state.t_type = "Income"

if "last_categories" not in st.session_state:
    st.session_state.last_categories = {}

# --- Title and instructions ---
st.title("💰 Simple Budget Tracker (Free Version)")

with st.expander("❓ How to Use This App", expanded=False):
    st.markdown("""
**Welcome to your Free Budget Tracker!**

Here’s how to use it:
- ➕ Add your income, expenses, or savings using the form below.
- 📈 View your financial summary at a glance.
- 📋 Scroll down to see your transaction history.

---

### 🔓 Want More Power? Upgrade to Premium for:

- 📈 Income/Expense Trends (Plotly)  
- 🧮 Pie and Bar Breakdown (Income, Expense, Saving)  
- 📋 Filterable Transaction History  
- 🔮 Financial insights with alerts and projection    
- 🎯 Debt tracking (Snowball/Avalanche strategie 
- 📁 CSV, Excel, and PDF export + impor   
    """)

# --- Transaction Type and categories selection ---
t_type = st.selectbox(
    "Transaction Type",
    ["Income", "Expense", "Saving"],
    index=["Income", "Expense", "Saving"].index(st.session_state.t_type)
)
st.session_state.t_type = t_type

categories_map = {
    "Income": ["Salary", "Bonus", "Other"],
    "Expense": ["Food", "Rent/Mortgage", "Bills", "Transport", "Entertainment", "Travel", "Other"],
    "Saving": ["Emergency Fund", "Retirement", "TFSA", "Other"]
}
categories = categories_map.get(t_type, ["Other"])

default_cat = st.session_state.last_categories.get(t_type, categories[0])
if default_cat not in categories:
    default_cat = categories[0]

# --- Date selector outside the form ---
st.session_state.form_date = st.date_input(
    "Select Date",
    value=st.session_state.form_date,
    key="date_input_outside"
)

# --- Transaction Entry Form ---
with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    # Use the date selected above (no date picker inside the form!)
    date = st.session_state.form_date

    category = st.selectbox(
        "Category",
        categories,
        index=categories.index(default_cat),
        key="category_select"
    )
    amount = st.number_input(
        "Amount",
        min_value=0.01,
        step=0.01,
        format="%.2f",
        key="amount_input"
    )
    note = st.text_input("Note (optional)", key="note_input")

    submitted = st.form_submit_button("Add Transaction")
    MAX_ENTRIES_FREE = 20  # max number of transactions allowed in free version

    if submitted:
        if amount <= 0:
            st.error("Amount must be greater than zero.")
        elif len(st.session_state.transactions) >= MAX_ENTRIES_FREE:
            st.warning(f"🚫 Free version limits you to {MAX_ENTRIES_FREE} entries. Upgrade to Premium for unlimited!")
        elif date.month != datetime.date.today().month or date.year != datetime.date.today().year:
            st.warning("🚫 Free version only supports entries for the current month. Upgrade to Premium for all dates!")
        else:
            new_row = {
                "Date": date,
                "Type": t_type,
                "Category": category,
                "Amount": amount,
                "Note": note,
            }
            st.session_state.transactions = pd.concat(
                [st.session_state.transactions, pd.DataFrame([new_row])],
                ignore_index=True,
            )
            st.session_state.last_categories[t_type] = category
            st.success("Transaction added!")

# --- Summary and Transaction Table ---
if not st.session_state.transactions.empty:
    df = st.session_state.transactions.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date", ascending=False)
    df["Type Icon"] = df["Type"].map({"Income": "🟢", "Expense": "🔴", "Saving": "💙"})

    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
    total_saving = df[df["Type"] == "Saving"]["Amount"].sum()
    net_balance = total_income - total_expense
    available_balance = total_income - total_expense - total_saving

    st.markdown("### 💡 Summary")
    cols = st.columns(3)
    with cols[0]:
        st.metric("💰 Income", f"${total_income:,.2f}", help="Total money earned")
    with cols[1]:
        st.metric("💸 Expenses", f"${total_expense:,.2f}", delta=f"-${total_expense:,.2f}", help="Total money spent")
    with cols[2]:
        st.metric("🏦 Savings", f"${total_saving:,.2f}", help="Money set aside")

    cols2 = st.columns(3)
    with cols2[0]:
        st.metric("📈 Net Balance", f"${net_balance:,.2f}", help="Income - Expenses")
    with cols2[1]:
        st.metric("📊 Available", f"${available_balance:,.2f}", help="Income - Expenses - Savings")
    with cols2[2]:
        st.metric("📅 Period", "This Month")

    # --- Explanation of Terms ---
    with st.expander("📘 What Do These Mean?", expanded=True):
        st.markdown("""
- **💰 Income**: Total money earned (e.g. salary, bonus).  
- **💸 Expense**: Money spent (e.g. food, rent, transport).  
- **🏦 Saving**: Money you've set aside and not meant to spend now.  
- **📈 Net Balance**: Income - Expenses (shows overall flow).  
- **📊 Available Balance**: Income - Expenses - Savings (your usable money now).  
        """)

    # --- Transaction History Table ---
    st.markdown("### 📋 Transaction History")
    with st.container():
        st.dataframe(df[["Date", "Type", "Category", "Amount", "Note","Type Icon"]], use_container_width=True)
else:
    st.info("No transactions yet. Add your first one above!")

st.markdown("---")
st.markdown("""

## 🚀 Upgrade to Premium for More Features!

| Feature                         | Free Version ✅                         | Premium Version 🚀               |
|--------------------------------|--------------------------------------|--------------------------------|
| Add income, expenses, savings  | ✅ Limited entries, current month only | ✅ Unlimited, full history      |
| Financial summary dashboard     | ✅                                    | ✅                             |
| Transaction history             | ✅ Basic for current month             | ✅ Filterable & detailed full history |
| Income/Expense Trends           | ❌                                    | ✅ Interactive Plotly charts    |
| Pie and Bar Breakdown           | ❌                                    | ✅                             |
| Financial insights & projections| ❌                                    | ✅                             |
| Debt tracking (Snowball/Avalanche) | ❌                                | ✅                             |
| Export CSV, Excel, PDF          | ❌                                    | ✅                             |
| Import CSV                     | ❌                                    | ✅                             |
| Priority Support               | ❌                                    | ✅                             |

---

### 🔓 Want to unlock unlimited tracking and all features? Upgrade to Premium now or Start Free Trial!

[👉 Click here to Upgrade or Start Free Trial](https://your-upgrade-link.com)
""")
