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
        # Path to service account key file (if using service account auth)
        self.SERVICE_ACCOUNT_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self._storage_client = None

    @property
    def storage_client(self):
        """Lazy initialization of Google Cloud Storage client"""
        if self._storage_client is None:
            if self.SERVICE_ACCOUNT_KEY:
                # Initialize with service account credentials
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