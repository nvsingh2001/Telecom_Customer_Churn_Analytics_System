from .base import Command
from infra import provision_services
from services import S3Manager
import os


class DeployCommand(Command):
    @property
    def name(self) -> str:
        return "Deploy Infrastructure"

    def __init__(self, factory, bucket_name):
        self.factory = factory
        self.bucket_name = bucket_name

    def execute(self) -> None:
        print("\n[Provisioning] Starting AWS service deployment...")
        try:
            provision_services(self.factory, self.bucket_name)
            print("[Success] Infrastructure deployed successfully!")
        except Exception as e:
            print(f"[Error] Deployment failed: {e}")


class UploadCommand(Command):
    @property
    def name(self) -> str:
        return "Upload Data to S3 Bucket"

    def __init__(self, S3Manager: S3Manager):
        self.S3Manager = S3Manager

    def execute(self) -> None:
        file_path = input("\nEnter the path to the CSV or JSON file: ").strip()
        if not file_path or not os.path.exists(file_path):
            print(f"[Error] File not found: {file_path}")
            return
        print("\n[Uploading] Starting data upload to S3 bucket...")
        try:
            self.S3Manager.upload_file(file_path)
            print("[Success] Data uploaded successfully!")
        except Exception as e:
            print(f"[Error] Data upload failed: {e}")
