import boto3
import os
from dotenv import load_dotenv
from io import BytesIO
import json
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class DigitalOceanUtils:
    def __init__(self):
        self.SPACES_ACCESS_KEY = os.getenv("SPACES_ACCESS_KEY")
        self.SPACES_SECRET_KEY = os.getenv("SPACES_SECRET_KEY")
        self.SPACE_NAME = os.getenv("SPACE_NAME", "federated-learning")
        self.ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'
        self._s3_client = None

    @property
    def s3_client(self):
        """Lazy initialization of S3 client"""
        if self._s3_client is None:
            self._s3_client = boto3.client(
                's3',
                endpoint_url=self.ENDPOINT_URL,
                aws_access_key_id=self.SPACES_ACCESS_KEY,
                aws_secret_access_key=self.SPACES_SECRET_KEY,
            )
            logger.info("DigitalOcean Spaces client initialized")
        return self._s3_client

    def upload_json_data(self, data, file_name):
        """Upload JSON data to DigitalOcean Space"""
        try:
            transactions_json = json.dumps(data)
            file_object = BytesIO(transactions_json.encode('utf-8'))

            self.s3_client.put_object(
                Bucket=self.SPACE_NAME,
                Key=file_name,
                Body=file_object,
                ContentType='application/json'
            )
            logger.info(f"Data uploaded successfully to {file_name}")
            return True
        except Exception as e:
            logger.error(f"Error uploading data: {e}")
            return False

    def download_json_data(self, file_name):
        """Download JSON data from DigitalOcean Space"""
        try:
            obj = self.s3_client.get_object(Bucket=self.SPACE_NAME, Key=file_name)
            data = json.loads(obj['Body'].read().decode('utf-8'))
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
do_utils = DigitalOceanUtils()