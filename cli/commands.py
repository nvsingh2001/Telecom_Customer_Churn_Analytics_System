from .base import Command
from infra import provision_services
from services import S3Manager, RedshiftManager
import os


class DeployCommand(Command):
    @property
    def name(self) -> str:
        return "Deploy Infrastructure"

    def __init__(self, factory):
        self.factory = factory

    def execute(self) -> None:
        print("\n[Provisioning] Starting AWS service deployment...")
        try:
            provision_services(self.factory)
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


class CreateTableCommand(Command):
    @property
    def name(self) -> str:
        return "Create Redshift Database Tables"

    def __init__(self, redshift_manager: RedshiftManager):
        self.redshift_manager = redshift_manager

    def execute(self) -> None:
        from config import (
            REDSHIFT_CLUSTER_IDENTIFIER,
            REDSHIFT_DBNAME,
            REDSHIFT_MASTER_USERNAME,
        )

        sql_file_path = "sql/create_tables.sql"
        print(f"\n[Creating] Starting table creation from {sql_file_path}...")
        try:
            self.redshift_manager.execute_sql_file(
                cluster_identifier=REDSHIFT_CLUSTER_IDENTIFIER,
                database_name=REDSHIFT_DBNAME,
                user_name=REDSHIFT_MASTER_USERNAME,
                file_path=sql_file_path,
            )
            print("[Success] SQL execution completed (check Redshift for status)!")
        except Exception as e:
            print(f"[Error] Table creation failed: {e}")
