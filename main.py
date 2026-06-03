from cli import (
    DeployCommand,
    UploadCommand,
    CreateTableCommand,
    LoadDataCommand,
    VerifyDataCommand,
    CreateAnalyticalTableCommand,
    DataAnalysisCommand,
    MaintenanceCommand,
    PauseClusterCommand,
    ResumeClusterCommand,
    MenuController,
)
from infra import AWSClientFactory
from services import S3Manager, RedshiftManager, RedshiftClusterManager
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
    cluster_manager = RedshiftClusterManager(client=factory.get_redshift_client())

    commands = [
        DeployCommand(factory=factory),
        UploadCommand(S3Manager=s3_manager),
        CreateTableCommand(redshift_manager=redshift_manager),
        LoadDataCommand(redshift_manager=redshift_manager),
        VerifyDataCommand(redshift_manager=redshift_manager),
        CreateAnalyticalTableCommand(redshift_manager=redshift_manager),
        DataAnalysisCommand(redshift_manager=redshift_manager),
        MaintenanceCommand(redshift_manager=redshift_manager),
        PauseClusterCommand(cluster_manager=cluster_manager),
        ResumeClusterCommand(cluster_manager=cluster_manager),
    ]

    menu = MenuController(commands)
    menu.run()


if __name__ == "__main__":
    main()
