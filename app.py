import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

st.set_page_config(page_title="💰 Budget Tracker", layout="centered")

# Optional CSS styling
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # No custom CSS provided

load_css("styles.css")  # Optional custom CSS file


st.title("💰 Simple Budget Tracker")

with st.expander("❓ How to Use This App", expanded=False):
    st.markdown("""
- Add your Income, Expenses, and Savings transactions using the form below.  
- View your financial summary and insights in real time.  
- Use the download button to save your data as a CSV backup.  
- Click “Reset” if you want to start over fresh.  

**✨ Premium features include:**
- 📊 Pie Chart for Expense Breakdown  
- 📤 Upload CSV to restore data  
- 📋 Full Transaction History with filters  
- 💰 Saving & Salary Breakdown  
- 🎯 Financial Goals Tracker  
- ☁️ Backup and Trend Analysis *(coming soon)*   
- 🔄 Recurring Entries *(coming soon)*  


""")


# Select transaction type
t_type = st.selectbox("Transaction Type", ["Income", "Expense", "Saving"])

# Categories based on type
if t_type == "Income":
    categories = ["Salary", "Bonus", "Other"]
elif t_type == "Expense":
    categories = ["Food", "Rent/Mortgage", "Bills", "Transport", "Entertainment", "Travel", "Other"]
else:  # Saving
    categories = ["Emergency Fund", "Retirement", "TFSA", "Other"]

# --- Form for input ---
with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    date = col1.date_input("Date", datetime.date.today())
    category = col2.selectbox("Category", categories)
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    note = st.text_input("Note (optional)")
    
    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        if 'transactions' not in st.session_state:
            st.session_state.transactions = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Note"])
        
        new_row = {
            "Date": date,
            "Type": t_type,
            "Category": category,
            "Amount": amount,
            "Note": note
        }
        st.session_state.transactions = pd.concat(
            [st.session_state.transactions, pd.DataFrame([new_row])],
            ignore_index=True
        )
        st.success("Transaction added!")

# --- Show Summary & Charts ---
if 'transactions' in st.session_state and not st.session_state.transactions.empty:
    df = st.session_state.transactions.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date", ascending=False)

    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
    total_saving = df[df["Type"] == "Saving"]["Amount"].sum()
    net_balance = total_income - total_expense

    # 💡 Summary display
    st.markdown("### 💡 Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Income", f"${total_income:,.2f}")
        st.metric("Saving", f"${total_saving:,.2f}")
    with col2:
        st.metric("Expense", f"${total_expense:,.2f}")
        st.metric("Net Balance", f"${net_balance:,.2f}")

  
    # 📥 CSV download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="transactions.csv",
        mime="text/csv"
    )

    # 🔄 Reset data
    if st.button("🔄 Reset All Data"):
        del st.session_state.transactions
        st.success("All data has been reset.")

else:
    st.info("No transactions yet. Add your first one above!")