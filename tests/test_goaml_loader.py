import os
import sys
import pandas as pd
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)
sys.path.append(os.path.join(ROOT, "app"))
os.environ["GCS_BUCKET_NAME"] = "soteria-core-data"

from app.data_generator import generate_transaction
from app.goaml_loader import load_goaml_transactions
from app.google_storage_utils import gs_utils


def test_goaml_structure_matches_json():
    if gs_utils.storage_client is None:
        pytest.skip("Google Cloud credentials not configured")
    # generate a single synthetic transaction to capture expected columns
    synthetic = generate_transaction(n_samples=1, bank_id=1)
    df_syn = pd.json_normalize(synthetic, sep="_")

    # load a single XML file worth of transactions
    xml_transactions = load_goaml_transactions(bank_id="1", prefix="20250823_191247", cache_dir="test_xml_cache", limit=1)
    assert xml_transactions, "No XML transactions loaded"
    df_xml = pd.json_normalize(xml_transactions, sep="_")

    expected_cols = {
        "Transaction_transaction_type",
        "Transaction_currency_amount",
        "Transaction_account_country_code",
        "Transaction_transaction_beneficiary_country_code",
        "Transaction_transaction_beneficiary",
    }

    assert expected_cols.issubset(df_syn.columns)
    assert expected_cols.issubset(df_xml.columns)
