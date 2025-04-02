import numpy as np
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import logging
from google_storage_utils import gs_utils

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
WATCHLIST_ENTITIES = ["P3", "P9", "P10"]  # Watchlist entities
PROBA_SCNR_RUSSIA = 1.0
PROBA_MANY_UBOs = 1.0
PROBA_SCNR_LARGE_CASH_DEPOSIT = 1.0
THR_UBOS = 4
COUNTRIES = ["US", "FR", "UK", "HK", "RU", "DE", "CN", "IN", "BR", "JP"]
TRANSACTION_TYPES = ["CASH", "202", "SWIFT", "SEPA"]
NETWORKS = ["SWIFT", "ACH", "SEPA", "CME"]
SETTLEMENT_TYPES = ["SWIFT", "ACH", "SEPA"]
ACCOUNT_TYPES = ["credit", "debit", "investment", "trade"]
ACCOUNT_ROLES = ["sending", "receiving"]
STATUSES = ["completed", "pending", "failed"]

def generate_transaction(n_samples: int = 5000, bank_id: int = 1) -> list:
    """Generate synthetic transaction data for a specific bank."""
    transactions = []
    now = datetime.now()

    # Determine which scenario the bank will focus on for the local label
    scenario_config = {
        1: ("Large Cash Deposit", lambda tx: tx['type'] == "CASH" and tx['role'] == "receiving" and tx['amount'] > 20000),
        2: ("Russian Transactions", lambda tx: tx['beneficiary_country'] == "RU"),
        3: ("Many UBOs", lambda tx: tx['num_ubos'] > THR_UBOS),
        4: ("Watchlist Entities", lambda tx: tx['beneficiary'] in WATCHLIST_ENTITIES)
    }

    for i in range(n_samples):
        # Generate transaction basics
        amount = round(np.random.uniform(10, 50000), 2)
        country = random.choice(COUNTRIES)
        tx_type = random.choice(TRANSACTION_TYPES)
        role = random.choice(ACCOUNT_ROLES)
        
        # Generate account details
        balance_before = round(np.random.uniform(10000, 100000), 2)
        balance_after = balance_before - amount if role == "sending" else balance_before + amount

        # Generate UBOs
        num_ubos = max(int(np.round(np.random.lognormal(np.log(2), 1.0))), 1)
        parties = [
            {
                "party_id": f"P{random.randint(1, 10)}",
                "as_of_date": int(datetime.now().timestamp() * 1000),
                "party_type": random.choice(["individual", "entity"]),
                "party_role": "UBO"
            } for _ in range(num_ubos)
        ]

        # Generate beneficiary details
        beneficiary = f"P{random.randint(1, 10)}"
        beneficiary_country = random.choice(COUNTRIES)
        
        # Generate timestamp (within last week)
        timestamp = int((now - timedelta(seconds=random.randint(0, 7*24*60*60))).timestamp() * 1000)

        # Risk detection logic
        tx_context = {
            'type': tx_type,
            'role': role,
            'amount': amount,
            'beneficiary_country': beneficiary_country,
            'num_ubos': num_ubos,
            'beneficiary': beneficiary
        }

        global_label = int(
            (tx_type == "CASH" and role == "receiving" and amount > 20000) or
            (beneficiary_country == "RU") or
            (num_ubos > THR_UBOS) or
            (beneficiary in WATCHLIST_ENTITIES)
        )

        local_label = 1 if bank_id in scenario_config and scenario_config[bank_id][1](tx_context) else 0

        # Build transaction object
        transaction = {
            "Transaction": {
                "transaction_id": f"T{i+1}",
                "transaction_originator": f"Trader_{random.randint(1, 10)}",
                "transaction_type": tx_type,
                "transaction_network": "CASH" if tx_type == "CASH" else random.choice(NETWORKS),
                "transaction_unit_type": "currency",
                "transaction_units": amount,
                "currency_amount": amount,
                "currency_code": "USD",
                "timestamp": timestamp,
                "settlement": {
                    "settlement_id": f"S{i+1}",
                    "settlement_type": "CASH" if tx_type == "CASH" else random.choice(SETTLEMENT_TYPES),
                    "amount": amount,
                    "currency_code": "USD",
                    "status": random.choice(STATUSES)
                },
                "exchange_rate": {
                    "base_currency": "USD",
                    "quote_currency": "USD",
                    "exchange_rate": 1.000,
                    "timestamp": int(datetime.now().timestamp() * 1000)
                },
                "account": {
                    "account_id": f"A{random.randint(1, 5)}",
                    "bic": f"BIC{random.randint(1, 5)}",
                    "swift": f"SWIFT{random.randint(1, 5)}",
                    "iban": f"IBAN{random.randint(1, 5)}",
                    "account_type": random.choice(ACCOUNT_TYPES),
                    "transaction_role": role,
                    "balance_before": balance_before,
                    "balance_after": balance_after,
                    "country_code": country,
                    "parties": parties
                },
                "transaction_beneficiary": beneficiary,
                "transaction_beneficiary_country_code": beneficiary_country,
                "local_label": local_label,
                "global_label": global_label
            }
        }
        transactions.append(transaction)
    
    logger.info(f"Generated {len(transactions)} transactions for Bank {bank_id}")
    return transactions

def main():
    """Main function to generate and upload transaction data for all banks."""
    load_dotenv()
    
    NUM_BANKS = 4
    for bank_id in range(1, NUM_BANKS + 1):
        bank_name = f"Bank_{bank_id}"
        try:
            transactions = generate_transaction(bank_id=bank_id)
            success = gs_utils.upload_json_data(transactions, f"{bank_name}_transactions.json")
            if success:
                logger.info(f"Successfully uploaded transactions for {bank_name}")
            else:
                logger.error(f"Failed to upload transactions for {bank_name}")
        except Exception as e:
            logger.error(f"Error processing bank {bank_id}: {str(e)}")

if __name__ == "__main__":
    main()