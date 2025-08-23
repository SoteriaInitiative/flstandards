from google.cloud import storage
import os
from dotenv import load_dotenv
import json
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class GoogleStorageUtils:
    def __init__(self):
        # Google Cloud Storage bucket name
        self.BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "soteria-federated-learning")
        # Collect individual service account fields from environment
        self.SERVICE_ACCOUNT_INFO = self._build_service_account_info()
        # Fallback to path to service account key file
        self.SERVICE_ACCOUNT_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self._storage_client = None

    def _build_service_account_info(self):
        """Gather service-account credentials from environment variables."""
        info = {
            "type": os.getenv("GCP_TYPE", "service_account"),
            "project_id": os.getenv("GCP_PROJECT_ID"),
            "private_key_id": os.getenv("GCP_PRIVATE_KEY_ID"),
            "private_key": os.getenv("GCP_PRIVATE_KEY"),
            "client_email": os.getenv("GCP_CLIENT_EMAIL"),
            "client_id": os.getenv("GCP_CLIENT_ID"),
            "auth_uri": os.getenv(
                "GCP_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"
            ),
            "token_uri": os.getenv(
                "GCP_TOKEN_URI", "https://oauth2.googleapis.com/token"
            ),
            "auth_provider_x509_cert_url": os.getenv(
                "GCP_AUTH_PROVIDER_CERT_URL",
                "https://www.googleapis.com/oauth2/v1/certs",
            ),
            "client_x509_cert_url": os.getenv("GCP_CLIENT_CERT_URL"),
        }

        # Only return the dict if mandatory fields are present
        mandatory = ["project_id", "private_key", "client_email"]
        if all(info.get(field) for field in mandatory):
            info["private_key"] = info["private_key"].replace("\\n", "\n")
            return info
        return None

    @property
    def storage_client(self):
        """Lazy initialization of Google Cloud Storage client"""
        if self._storage_client is None:
            if self.SERVICE_ACCOUNT_INFO:
                # Initialize using service account details provided in env
                self._storage_client = storage.Client.from_service_account_info(
                    self.SERVICE_ACCOUNT_INFO
                )
            elif self.SERVICE_ACCOUNT_KEY:
                # Initialize with service account credentials file
                self._storage_client = storage.Client.from_service_account_json(
                    self.SERVICE_ACCOUNT_KEY
                )
            else:
                # Initialize with default credentials
                self._storage_client = storage.Client()
            logger.info("Google Cloud Storage client initialized")
        return self._storage_client

    def upload_json_data(self, data, file_name):
        """Upload JSON data to Google Cloud Storage"""
        try:
            bucket = self.storage_client.bucket(self.BUCKET_NAME)
            blob = bucket.blob(file_name)
            
            # Upload as JSON string
            blob.upload_from_string(
                data=json.dumps(data),
                content_type='application/json'
            )
            logger.info(f"Data uploaded successfully to {file_name}")
            return True
        except Exception as e:
            logger.error(f"Error uploading data: {e}")
            return False

    def download_json_data(self, file_name):
        """Download JSON data from Google Cloud Storage"""
        try:
            bucket = self.storage_client.bucket(self.BUCKET_NAME)
            blob = bucket.blob(file_name)
            
            # Download as string and parse JSON
            data = json.loads(blob.download_as_text())
            logger.info(f"Successfully downloaded data from {file_name}")
            return data
        except Exception as e:
            logger.error(f"Error downloading file {file_name}: {e}")
            return None

    def get_bank_transactions(self, bank_id):
        """Helper method to get bank transactions by bank ID"""
        file_name = f"Bank_{bank_id}_transactions.json"
        return self.download_json_data(file_name)

# Singleton instance for easy import
gs_utils = GoogleStorageUtils()
