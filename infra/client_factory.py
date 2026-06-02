import boto3


class AWSClientFactory:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AWSClientFactory, cls).__new__(cls)

        return cls._instance

    def __init__(self, region):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.region = region
            self._s3 = boto3.client("s3", region_name=self.region)

    def get_s3_client(self):
        return self._s3
