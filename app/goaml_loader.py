import os
import xml.etree.ElementTree as ET
from typing import List
import logging

from google_storage_utils import gs_utils

logger = logging.getLogger(__name__)

# Default cache directory inside the app folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "xml_cache")

def download_and_cache_xml(bank_id: str,
                           prefix: str,
                           cache_dir: str = CACHE_DIR,
                           limit: int | None = None) -> List[str]:
    """Download XML files for a bank, caching them locally."""
    os.makedirs(cache_dir, exist_ok=True)
    storage_client = gs_utils.storage_client
    if storage_client is None:
        logger.warning("Google Cloud Storage client unavailable; skipping XML download")
        return []
    blobs = storage_client.list_blobs(gs_utils.BUCKET_NAME, prefix=prefix)
    paths: List[str] = []
    for blob in blobs:
        if f"Bank_{bank_id}_" not in blob.name or not blob.name.endswith(".xml"):
            continue
        local_path = os.path.join(cache_dir, os.path.basename(blob.name))
        if not os.path.exists(local_path):
            blob.download_to_filename(local_path)
            logger.info("Downloaded %s", blob.name)
        else:
            logger.info("Using cached file %s", local_path)
        paths.append(local_path)
        if limit and len(paths) >= limit:
            break
    return paths


def parse_goaml_xml(files: List[str]) -> List[dict]:
    """Parse goAML XML files into transaction dicts compatible with JSON generator."""
    transactions: List[dict] = []
    for path in files:
        tree = ET.parse(path)
        root = tree.getroot()
        for tx in root.findall("transaction"):
            tx_type = tx.findtext("transaction_type_code", default="")
            if tx_type == "CASHT":
                tx_type = "CASH"
            amount = float(tx.findtext("amount_local", "0"))
            from_country = tx.find("t_from_my_client").findtext("from_country", default="")
            to_country = tx.find("t_to_my_client").findtext("to_country", default="")
            beneficiary_node = tx.find(
                "t_to_my_client/to_account/related_entities/account_related_entity/entity/name"
            )
            beneficiary = beneficiary_node.text if beneficiary_node is not None else ""
            entity_count = len(
                tx.findall("t_to_my_client/to_account/related_entities/account_related_entity")
            )
            person_count = len(
                tx.findall("t_to_my_client/to_account/related_persons/account_related_person")
            )
            comments = tx.findtext("comments", default="")
            labels = dict(
                part.split("=") for part in comments.split(";") if "=" in part
            )
            local_label = int(labels.get("local_label", 0))
            global_label = int(labels.get("global_label", 0))
            parties = (
                [{"party_type": "entity", "party_role": "UBO"}] * entity_count
                + [{"party_type": "individual", "party_role": "UBO"}] * person_count
            )
            transactions.append(
                {
                    "Transaction": {
                        "transaction_type": tx_type,
                        "currency_amount": amount,
                        "account": {"country_code": from_country, "parties": parties},
                        "transaction_beneficiary_country_code": to_country,
                        "transaction_beneficiary": beneficiary,
                        "local_label": local_label,
                        "global_label": global_label,
                    }
                }
            )
    return transactions


def load_goaml_transactions(bank_id: str,
                            prefix: str | None = None,
                            cache_dir: str = CACHE_DIR,
                            limit: int | None = None) -> List[dict]:
    """Convenience wrapper to download and parse goAML XML files."""
    if prefix is None:
        prefix = os.getenv("GOAML_PREFIX", "20250924_214145")
    if limit is None:
        env_limit = os.getenv("GOAML_LIMIT")
        limit = int(env_limit) if env_limit else None
    files = download_and_cache_xml(bank_id, prefix, cache_dir=cache_dir, limit=limit)
    if not files:
        logger.error(f"No XML files found for bank {bank_id} on bucket '{gs_utils.BUCKET_NAME}' in folder '{prefix}'")
        return []
    return parse_goaml_xml(files)
