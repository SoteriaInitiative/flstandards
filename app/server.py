import os
import flwr as fl
from dotenv import load_dotenv
from flwr.server.strategy import FedProx
import numpy as np
import logging

load_dotenv()
# Default to five training rounds if the environment variable is missing
NUM_ROUNDS = int(os.getenv("NUM_ROUNDS", "5"))
MU = 0.01
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS", "localhost:8080")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True,
)
logger = logging.getLogger()

def aggregate_fit_metrics(results):
    """Aggregate AUC metrics from clients during training."""
    logger.info(f"Received training results: {results}")
    auc_list = [metrics["local_train_auc"] for _, metrics in results if "local_train_auc" in metrics]
    avg_local_train_auc = np.mean(auc_list) if auc_list else 0.0
    logger.info(f"Aggregated local training AUC: {avg_local_train_auc}")
    return {"avg_local_train_auc": avg_local_train_auc}

def aggregate_evaluate_metrics(results):
    """Aggregate evaluation AUC metrics from clients after testing."""
    logger.info(f"Received testing results: {results}")
    local_test_auc = [metrics["local_auc"] for _, metrics in results if "local_auc" in metrics]
    global_test_auc = [metrics["global_auc"] for _, metrics in results if "global_auc" in metrics]

    avg_local_test_auc = np.mean(local_test_auc) if local_test_auc else 0.0
    avg_global_test_auc = np.mean(global_test_auc) if global_test_auc else 0.0

    logger.info(f"Aggregated local test AUC: {avg_local_test_auc:.4f}")
    logger.info(f"Aggregated global test AUC: {avg_global_test_auc:.4f}")

    return {
        "avg_local_test_auc": avg_local_test_auc,
        "avg_global_test_auc": avg_global_test_auc,
    }

# FedProx because converging heterogeneous data better
def create_strategy():
    """Create and return the FedProx strategy with AUC aggregation."""
    return FedProx(
        fraction_fit=1.0,
        fraction_evaluate=1.0,
        min_fit_clients=4,
        min_evaluate_clients=4,
        min_available_clients=4,
        proximal_mu=MU,
        fit_metrics_aggregation_fn=aggregate_fit_metrics,
        evaluate_metrics_aggregation_fn=aggregate_evaluate_metrics,
    )

if __name__ == "__main__":
    logger.info(
        f"Starting FedProx server at {SERVER_ADDRESS} with {NUM_ROUNDS} rounds (mu={MU})"
    )
    fl.server.start_server(
        server_address=SERVER_ADDRESS,
        config=fl.server.ServerConfig(num_rounds=NUM_ROUNDS),
        strategy=create_strategy(),
    )
