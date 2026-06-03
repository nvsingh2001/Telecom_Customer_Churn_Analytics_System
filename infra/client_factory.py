import boto3


class AWSClientFactory:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AWSClientFactory, cls).__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.region = kwargs["region"]
            self.__session_main = boto3.Session()
            self.__session_secondary = boto3.Session(
                profile_name=kwargs["profile_secondary"]
            )

            self._s3 = self.__session_main.client("s3", region_name=self.region)
            self._redshift = self.__session_secondary.client(
                "redshift", region_name=self.region
            )
            self._redshift_data = self.__session_secondary.client(
                "redshift-data", region_name=self.region
            )

    def get_s3_client(self):
        return self._s3

    def get_redshift_client(self):
        return self._redshift

    def get_redshift_data_client(self):
        return self._redshift_data
