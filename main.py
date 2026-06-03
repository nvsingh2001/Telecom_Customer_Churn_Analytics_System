from cli import DeployCommand, UploadCommand, MenuController
from infra import AWSClientFactory
from services import S3Manager
from config import REGION, BUCKET_NAME, PROFILE_MAIN, PROFILE_SECONDARY


def main():
    factory = AWSClientFactory(
        **{
            "region": REGION,
            "profile_main": PROFILE_MAIN,
            "profile_secondary": PROFILE_SECONDARY,
        }
    )

    s3_manager = S3Manager(s3_client=factory.get_s3_client(), bucket_name=BUCKET_NAME)

    commands = [
        DeployCommand(factory=factory),
        UploadCommand(S3Manager=s3_manager),
    ]

    menu = MenuController(commands)
    menu.run()


if __name__ == "__main__":
    main()
