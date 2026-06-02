from cli import DeployCommand, UploadCommand, MenuController
from infra import AWSClientFactory
from dotenv import load_dotenv
import os

from services import S3Manager


load_dotenv()
REGION = os.getenv("REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")


def main():
    factory = AWSClientFactory(region=REGION)

    s3_manager = S3Manager(s3_client=factory.get_s3_client(), bucket_name=BUCKET_NAME)

    commands = [
        DeployCommand(factory=factory, bucket_name=BUCKET_NAME),
        UploadCommand(S3Manager=s3_manager),
    ]

    menu = MenuController(commands)
    menu.run()


if __name__ == "__main__":
    main()
