from cli import (
    DeployCommand,
    UploadCommand,
    CreateTableCommand,
    LoadDataCommand,
    VerifyDataCommand,
    CreateAnalyticalTableCommand,
    DataAnalysisCommand,
    MenuController,
)
from infra import AWSClientFactory
from services import S3Manager, RedshiftManager
from config import (
    REGION,
    BUCKET_NAME,
    PROFILE_MAIN,
    PROFILE_SECONDARY,
)


def main():
    factory = AWSClientFactory(
        **{
            "region": REGION,
            "profile_main": PROFILE_MAIN,
            "profile_secondary": PROFILE_SECONDARY,
        }
    )

    s3_manager = S3Manager(s3_client=factory.get_s3_client(), bucket_name=BUCKET_NAME)
    redshift_manager = RedshiftManager(client=factory.get_redshift_data_client())

    commands = [
        DeployCommand(factory=factory),
        UploadCommand(S3Manager=s3_manager),
        CreateTableCommand(redshift_manager=redshift_manager),
        LoadDataCommand(redshift_manager=redshift_manager),
        VerifyDataCommand(redshift_manager=redshift_manager),
        CreateAnalyticalTableCommand(redshift_manager=redshift_manager),
        DataAnalysisCommand(redshift_manager=redshift_manager),
    ]

    menu = MenuController(commands)
    menu.run()


if __name__ == "__main__":
    main()
