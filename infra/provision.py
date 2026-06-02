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


def provision_services(factory, bucket_name):
    provisioner = InfrastructureProvisioner(factory)
    provisioner.create_s3_bucket(bucket_name)
