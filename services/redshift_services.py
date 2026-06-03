from botocore.exceptions import ClientError


class RedshiftManager:
    def __init__(self, client):
        self.client = client

    def list_databases(self, cluster_identifier, database_name, database_user):
        """
        Lists databases in a cluster.

        :param cluster_identifier: The cluster identifier.
        :param database_name: The database name.
        :param database_user: The database user.
        :return: The list of databases.
        """
        try:
            paginator = self.client.get_paginator("list_databases")
            databases = []
            for page in paginator.paginate(
                ClusterIdentifier=cluster_identifier,
                Database=database_name,
                DbUser=database_user,
            ):
                databases.extend(page["Databases"])

            return databases
        except ClientError as err:
            print(f"[Error] Failed to list databases: {err}")

    def execute_statement(
        self, cluster_identifier, database_name, user_name, sql, parameter_list=None
    ):
        """
        Executes a SQL statement.

        :param cluster_identifier: The cluster identifier.
        :param database_name: The database name.
        :param user_name: The user's name.
        :param sql: The SQL statement.
        :param parameter_list: The optional SQL statement parameters.
        :return: The SQL statement result.
        """

        try:
            kwargs = {
                "ClusterIdentifier": cluster_identifier,
                "Database": database_name,
                "DbUser": user_name,
                "Sql": sql,
            }
            if parameter_list:
                kwargs["Parameters"] = parameter_list
            response = self.client.execute_statement(**kwargs)
            return response
        except ClientError as err:
            print(f"[Error] Failed to execute statement: {err}")
            raise err

    def describe_statement(self, statement_id):
        """
        Describes a SQL statement.

        :param statement_id: The SQL statement identifier.
        :return: The SQL statement result.
        """
        try:
            response = self.client.describe_statement(Id=statement_id)
            return response
        except ClientError as err:
            print(f"[Error] Failed to describe statement: {err}")

    def get_statement_result(self, statement_id):
        """
        Gets the result of a SQL statement.

        :param statement_id: The SQL statement identifier.
        :return: The SQL statement result.
        """
        try:
            result = {
                "Records": [],
            }
            paginator = self.client.get_paginator("get_statement_result")
            for page in paginator.paginate(Id=statement_id):
                if "ColumnMetadata" not in result:
                    result["ColumnMetadata"] = page["ColumnMetadata"]
                result["Records"].extend(page["Records"])
            return result
        except ClientError as err:
            print(f"[Error] Failed to get statement result: {err}")

    def wait_for_statement(self, statement_id):
        """
        Polls for the completion of a statement.

        :param statement_id: The statement identifier.
        :return: True if finished, False if failed/aborted.
        """
        import time

        while True:
            desc = self.describe_statement(statement_id)
            if desc is None:
                return False
            status = desc["Status"]
            if status == "FINISHED":
                return True
            elif status in ["FAILED", "ABORTED"]:
                error_msg = desc.get("Error", "No error message provided.")
                print(f"\n[Error] Query {status}: {error_msg}")
                return False

            print(".", end="", flush=True)
            time.sleep(2)

    def execute_sql_file(self, cluster_identifier, database_name, user_name, file_path):
        """
        Reads a SQL file and executes each statement separately.

        :param cluster_identifier: The cluster identifier.
        :param database_name: The database name.
        :param user_name: The user's name.
        :param file_path: The path to the SQL file.
        """
        try:
            with open(file_path, "r") as f:
                sql_content = f.read()

            statements = [s.strip() for s in sql_content.split(";") if s.strip()]

            for sql in statements:
                print(f"[Executing SQL] {sql[:50]}...")
                self.execute_statement(
                    cluster_identifier=cluster_identifier,
                    database_name=database_name,
                    user_name=user_name,
                    sql=sql,
                )
        except Exception as e:
            print(f"[Error] Failed to execute SQL file: {e}")
            raise e
