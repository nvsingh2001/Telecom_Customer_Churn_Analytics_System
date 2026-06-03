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


class LoadDataCommand(Command):
    @property
    def name(self) -> str:
        return "Load Data into Redshift Database"

    def __init__(self, redshift_manager: RedshiftManager):
        self.redshift_manager = redshift_manager

    def execute(self) -> None:
        from config import (
            REDSHIFT_CLUSTER_IDENTIFIER,
            REDSHIFT_DBNAME,
            REDSHIFT_MASTER_USERNAME,
            REDSHIFT_ROLE_ARN,
            BUCKET_NAME,
        )

        print("\nAvailable Tables:")
        print("1. customer_churn")
        print("2. zip_population")
        table_choice = input("Select table (1 or 2): ").strip()

        if table_choice == "1":
            table_name = "customer_churn"
        elif table_choice == "2":
            table_name = "zip_population"
        else:
            print("[Error] Invalid table selection.")
            return

        file_name = input(f"Enter the file name in S3 (raw/{table_name}.csv): ").strip()
        if not file_name:
            file_name = f"{table_name}.csv"

        try:
            with open("sql/load_data.sql", "r") as f:
                sql_template = f.read()

            sql_query = sql_template.format(
                table_name=table_name,
                BUCKET_NAME=BUCKET_NAME,
                file_name=file_name,
                REDSHIFT_ROLE_ARN=REDSHIFT_ROLE_ARN,
            )

            print(
                f"\n[Loading] Loading data into {table_name} from s3://{BUCKET_NAME}/raw/{file_name}..."
            )
            response = self.redshift_manager.execute_statement(
                cluster_identifier=REDSHIFT_CLUSTER_IDENTIFIER,
                database_name=REDSHIFT_DBNAME,
                user_name=REDSHIFT_MASTER_USERNAME,
                sql=sql_query,
            )

            statement_id = response["Id"]
            if self.redshift_manager.wait_for_statement(statement_id):
                print("\n[Success] Data load completed successfully!")
            else:
                print("\n[Failure] Data load failed. Check the error message above.")

        except FileNotFoundError:
            print("[Error] SQL template file 'sql/load_data.sql' not found.")
        except Exception as e:
            print(f"[Error] Data load failed: {e}")


class VerifyDataCommand(Command):
    @property
    def name(self) -> str:
        return "Verify Data Loads (Check Row Counts)"

    def __init__(self, redshift_manager: RedshiftManager):
        self.redshift_manager = redshift_manager

    def execute(self) -> None:
        from config import (
            REDSHIFT_CLUSTER_IDENTIFIER,
            REDSHIFT_DBNAME,
            REDSHIFT_MASTER_USERNAME,
        )

        tables = ["customer_churn", "zip_population"]

        for table in tables:
            print(f"\n[Verifying] Checking row count for {table}...")
            sql = f"SELECT COUNT(*) FROM {table};"
            try:
                response = self.redshift_manager.execute_statement(
                    cluster_identifier=REDSHIFT_CLUSTER_IDENTIFIER,
                    database_name=REDSHIFT_DBNAME,
                    user_name=REDSHIFT_MASTER_USERNAME,
                    sql=sql,
                )
                statement_id = response["Id"]
                if self.redshift_manager.wait_for_statement(statement_id):
                    result = self.redshift_manager.get_statement_result(statement_id)
                    if result is None:
                        print(f"\n[Error] Could not verify {table}.")
                        continue
                    count = result["Records"][0][0]["longValue"]
                    print(f"\n[Status] Table '{table}' has {count} records.")
                else:
                    print(f"\n[Error] Could not verify {table}.")
            except Exception as e:
                print(f"[Error] Verification failed for {table}: {e}")
