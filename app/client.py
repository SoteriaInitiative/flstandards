import os
import flwr as fl
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import backend as K
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
import logging
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from google_storage_utils import gs_utils

# Custom weighted loss function
def weighted_loss(y_true, y_pred):
    loss = K.binary_crossentropy(y_true, y_pred)  
    fraud_weight = tf.ones_like(y_true) * 1.0  # Shape: (batch_size, 1)
    non_fraud_weight = tf.ones_like(y_true) * 0.01    
    weight = tf.where(tf.equal(y_true, 1), fraud_weight, non_fraud_weight)
    return K.mean(loss * weight)

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Environment variables
BANK_ID = os.getenv("BANK_ID", "1")
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS", "server:8080")
TRANSACTIONS_FILE = f"Bank_{BANK_ID}_transactions.json"

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Load transactions from DigitalOcean Spaces
def load_transactions(file_name):
    try:
        transactions = gs_utils.download_json_data(file_name)
        if transactions is None:
            logger.error("Failed to download transactions (received None)")
            return []
        logger.info(f"Loaded {len(transactions)} transactions from DigitalOcean.")
        return transactions
    except Exception as e:
        logger.error(f"Error loading transactions: {e}")
        return []

# Load data
transactions = load_transactions(TRANSACTIONS_FILE)
if not transactions:
    raise SystemExit("Failed to load transaction data - exiting")

df = pd.json_normalize(transactions, sep="_")

# Define possible party type-role combinations
POSSIBLE_PARTY_COMBINATIONS = [
    ("individual", "UBO"),
    ("entity", "UBO"),
]
party_columns = [f"party_{ptype}_{prole}" for ptype, prole in POSSIBLE_PARTY_COMBINATIONS]

# Function to count occurrences based on predefined values
def count_party_combinations(parties):
    counts = {col: 0 for col in party_columns}
    for party in parties:
        col_name = f"party_{party.get('party_type')}_{party.get('party_role')}"
        if col_name in counts:
            counts[col_name] += 1
    return counts

# Apply function to transactions
party_data = [count_party_combinations(tx.get("Transaction", {}).get("account", {}).get("parties", [])) for tx in transactions]
df_parties = pd.DataFrame(party_data).reindex(columns=party_columns, fill_value=0)
df = pd.concat([df, df_parties], axis=1)

# Define predefined transaction beneficiary values
POSSIBLE_BENEFICIARIES = [f"P{i}" for i in range(1, 11)]

# One-hot encode categorical features
encoder = OneHotEncoder(categories=[POSSIBLE_BENEFICIARIES], drop="first", sparse_output=False, handle_unknown="ignore")

# Prepare features and labels
X = df[[
    "Transaction_transaction_type", 
    "Transaction_currency_amount", 
    "Transaction_account_country_code", 
    "Transaction_transaction_beneficiary_country_code",
    "Transaction_transaction_beneficiary"
] + party_columns]  # Include new party count features

y = df["Transaction_local_label"]

# Create a ColumnTransformer to apply OHE to categorical features
preprocessor = ColumnTransformer(
    transformers=[
        ("transaction_type", encoder, ["Transaction_transaction_type"]),
        ("account_country", encoder, ["Transaction_account_country_code"]),
        ("beneficiary_country", encoder, ["Transaction_transaction_beneficiary_country_code"]),
        ("beneficiary", encoder, ["Transaction_transaction_beneficiary"]),
        ("currency_amount", "passthrough", ["Transaction_currency_amount"]),
        ("party_counts", "passthrough", party_columns),
    ]
)

# Apply the transformer
X_processed = preprocessor.fit_transform(X)

# Split the data
X_train, X_test, y_train_local, y_test_local, train_indices, test_indices = train_test_split(
    X_processed, y, df.index, test_size=0.2, random_state=42, stratify=y
)

# Extract global labels for the test set
y_test_global = df.loc[test_indices, "Transaction_global_label"].values

# Scale currency amount (assuming min-max scaling)
X_train[:, -len(party_columns)-1] = (X_train[:, -len(party_columns)-1] - 10) / (50000 - 10)
X_test[:, -len(party_columns)-1] = (X_test[:, -len(party_columns)-1] - 10) / (50000 - 10)

# Convert to NumPy arrays
X_train = X_train.astype(np.float32)
X_test = X_test.astype(np.float32)
y_train, y_test_local = y_train_local.values, y_test_local.values

# Define model
def create_model(input_dim):
    inputs = tf.keras.layers.Input(shape=(input_dim,))
    hidden = tf.keras.layers.Dense(32, activation="relu")(inputs)
    dropout = tf.keras.layers.Dropout(0.3)(hidden)
    output = tf.keras.layers.Dense(1, activation="sigmoid")(dropout)
    model = tf.keras.Model(inputs=inputs, outputs=output)
    model.compile(optimizer="adam", loss=weighted_loss, metrics=["AUC"])
    logger.info("Model created.")
    return model

model = create_model(X_train.shape[1])

# Define Flower client
class SimpleClient(fl.client.NumPyClient):
    def get_parameters(self, config):
        return model.get_weights()

    def set_parameters(self, parameters):
        model.set_weights(parameters)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        history = model.fit(X_train, y_train, epochs=30, batch_size=64, verbose=0)
        y_train_pred = model.predict(X_train)
        local_train_auc = roc_auc_score(y_train, y_train_pred)
        
        return self.get_parameters(config), len(X_train), {"local_train_auc": local_train_auc}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        y_local_pred = model.predict(X_test)
        local_auc = roc_auc_score(y_test_local, y_local_pred)
        
        # Global evaluation using y_test_global
        y_global_pred = model.predict(X_test)
        global_auc = roc_auc_score(y_test_global, y_global_pred)
        
        return local_auc, len(X_test), {"local_auc": local_auc, "global_auc": global_auc}

if __name__ == "__main__":
    fl.client.start_client(server_address=SERVER_ADDRESS, client=SimpleClient().to_client())
