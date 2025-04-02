import boto3
import json
import pandas as pd
import streamlit as st
from google_storage_utils import gs_utils
from datetime import datetime


@st.cache_data
def fetch_data_from_space(bank_id):
    return gs_utils.get_bank_transactions(bank_id)

# Convert JSON data into pandas DataFrame
def to_dataframe(data):
    transactions = []

    for record in data:
        transaction_data = record.get("Transaction", {})
        transactions.append(transaction_data)
    
    transactions_df = pd.json_normalize(transactions, errors='ignore')

    # Convert from milliseconds to datetime (unit='ms')
    transactions_df['timestamp'] = pd.to_datetime(transactions_df['timestamp'], unit='ms', errors='coerce', utc=True)

    # Format the timestamp into a readable string (date only)
    transactions_df['date'] = transactions_df['timestamp'].dt.date

    # Round currency_amount to 2 decimal places
    transactions_df['currency_amount'] = transactions_df['currency_amount'].apply(lambda x: round(float(x), 2))


    # Add missing columns transaction_beneficiary and transaction_beneficiary_country_code
    transactions_df['transaction_beneficiary'] = transactions_df['transaction_beneficiary'].fillna('Unknown')
    transactions_df['transaction_beneficiary_country_code'] = transactions_df['transaction_beneficiary_country_code'].fillna('Unknown')

    return transactions_df

# Paginate the DataFrame
def paginate_dataframe(df, page_size=10):
    total_rows = len(df)
    total_pages = (total_rows // page_size) + (1 if total_rows % page_size > 0 else 0)

    page_number = st.selectbox("Select Page", range(1, total_pages + 1), index=0)
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size

    return df[start_idx:end_idx], total_pages, page_number

# Highlight row based on label
def highlight_row(row):
    # You can customize this logic based on your labels
    if row['local_label'] == 1:
        return ['background-color: red'] * len(row)  # Red highlight for local_label = 1
    elif row['global_label'] == 1:
        return ['background-color: yellow'] * len(row)  # Yellow highlight for global_label = 1
    else:
        return [''] * len(row)  # No highlight for other cases

# Display bank data in Streamlit
def display_bank_data(bank_id):
    # Fetch data from the Space
    data = fetch_data_from_space(bank_id)
    
    # Extract the transactions
    transactions = to_dataframe(data)

    # Display the transactions data in a paginated table
    if not transactions.empty:
        # Paginate the DataFrame
        paginated_transactions, total_pages, current_page = paginate_dataframe(transactions)

        # Display all columns for processing but use only the important ones for display
        
        important_columns = [
            'transaction_id', 
            'date', 
            'transaction_originator',
            'currency_amount', 
            'currency_code',
            'transaction_type',
            'transaction_beneficiary', 
            'transaction_beneficiary_country_code',
            'local_label',
            'global_label'
        ]

        # Display transactions with row highlight
        st.dataframe(paginated_transactions[important_columns].style.apply(highlight_row, axis=1))

        # Page navigation
        st.write(f"Page {current_page} of {total_pages}")

        # Allow for the expansion of a single transaction
        selected_transaction_id = st.selectbox("Select a transaction to expand", paginated_transactions['transaction_id'].tolist())

        # Find the row for the selected transaction
        selected_transaction = paginated_transactions[paginated_transactions['transaction_id'] == selected_transaction_id].iloc[0]

        # Create an expandable section for the selected transaction
        with st.expander(f"Transaction ID: {selected_transaction['transaction_id']}"):
            st.write("Transaction Originator:", selected_transaction.get('transaction_originator', 'N/A'))
            st.write("Amount:", selected_transaction.get('currency_amount', 'N/A'))
            st.write("Currency Code:", selected_transaction.get('currency_code', 'N/A'))
            st.write("Timestamp:", selected_transaction.get('timestamp', 'N/A'))
            st.write("Account ID:", selected_transaction.get('account.account_id', 'N/A'))
            st.write("Account Balance Before:", selected_transaction.get('account.balance_before', 'N/A'))
            st.write("Account Balance After:", selected_transaction.get('account.balance_after', 'N/A'))
            st.write("Account Party:", selected_transaction.get('account.parties', 'N/A'))

            # Display labels
            st.write("Local Label:", selected_transaction.get('local_label', 'N/A'))
            st.write("Global Label:", selected_transaction.get('global_label', 'N/A'))

    else:
        st.warning("No transactions data found!")

# Streamlit UI
st.set_page_config(page_title="Federated Learning Dashboard", layout="wide")
st.title("📊 Federated Learning Monitoring Dashboard")
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Bank 1", "Bank 2", "Bank 3", "Bank 4"])

# Overview
if page == "Overview":
    st.header("🔍 Overview of the System")
    st.write("Welcome to the Federated Learning Monitoring Dashboard!")
    st.write("This system tracks the transaction data generated across different banks.")
    st.write("The dashboard displays transaction data for four banks, where each bank runs its own model to detect suspicious transactions. The labels represent different scenarios detected by each bank.")
    st.write("### Label Explanation:")
    st.write("🔴 **Local Label (Red)**: The scenario detected by the bank itself. This indicates that a suspicious transaction was flagged by the bank.")
    st.write("🟡 **Global Label (Yellow)**: A scenario that was detected by other banks but missed by the bank itself.")

# Bank 1
elif page == "Bank 1":
    st.header("🏦 Transactions Data Bank 1")
    st.write("**Scenario for Bank 1**: Bank 1 detects **Large Cash Deposits**. Transactions above $20,000 and received in cash will trigger a local label of 1 for this scenario.")
    display_bank_data(1)

# Bank 2
elif page == "Bank 2":
    st.header("🏦 Transactions Data Bank 2")
    st.write("**Scenario for Bank 2**: Bank 2 detects **Russian Transactions**. Transactions originating from Russia are flagged as suspicious, leading to a local label of 1.")
    display_bank_data(2)

# Bank 3
elif page == "Bank 3":
    st.header("🏦 Transactions Data Bank 3")
    st.write("**Scenario for Bank 3**: Bank 3 detects **Multiple UBOs**. Transactions involving more than two UBOs are flagged, resulting in a local label of 1.")
    display_bank_data(3)

# Bank 4
elif page == "Bank 4":
    st.header("🏦 Transactions Data Bank 4")
    st.write("**Scenario for Bank 4**: Bank 4 detects **Watchlisted Entities**. If the transaction beneficiary is on the watchlist, it triggers a local label of 1. In this case, we detect P3, P9, and P10 as the watchlisted entities.")
    display_bank_data(4)
