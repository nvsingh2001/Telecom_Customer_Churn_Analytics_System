class InfrastructureProvisioner:
    def __init__(self, factory):
        self.factory = factory

    def create_s3_bucket(self, bucket_name):
        s3 = self.factory.get_s3_client()
        try:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": self.factory.region},
            )
            print(f"Bucket {bucket_name} created successfully.")
        except s3.exceptions.BucketAlreadyOwnedByYou:
            print(f"Bucket {bucket_name} already exists.")

    def create_redshift_cluster(
        self, cluster_identifier, role_arn, dbname, master_username, master_password
    ):
        redshift = self.factory.get_redshift_client()
        try:
            redshift.create_cluster(
                ClusterIdentifier=cluster_identifier,
                NodeType="ra3.large",
                MasterUsername=master_username,
                MasterUserPassword=master_password,
                DBName=dbname,
                IamRoles=[role_arn],
                ClusterType="single-node",
            )
            print(f"Redshift cluster {cluster_identifier} created successfully.")
        except redshift.exceptions.ClusterAlreadyExistsFault:
            print(f"Redshift cluster {cluster_identifier} already exists.")


def provision_services(factory):
    from config import (
        BUCKET_NAME,
        REDSHIFT_CLUSTER_IDENTIFIER,
        REDSHIFT_ROLE_ARN,
        REDSHIFT_DBNAME,
        REDSHIFT_MASTER_USERNAME,
        REDSHIFT_MASTER_PASSWORD,
    )

    provisioner = InfrastructureProvisioner(factory)
    provisioner.create_s3_bucket(bucket_name=BUCKET_NAME)
    provisioner.create_redshift_cluster(
        cluster_identifier=REDSHIFT_CLUSTER_IDENTIFIER,
        role_arn=REDSHIFT_ROLE_ARN,
        dbname=REDSHIFT_DBNAME,
        master_username=REDSHIFT_MASTER_USERNAME,
        master_password=REDSHIFT_MASTER_PASSWORD,
    )
