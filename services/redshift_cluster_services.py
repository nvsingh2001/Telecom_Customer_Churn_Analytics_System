from botocore.exceptions import ClientError


class RedshiftClusterManager:
    def __init__(self, client):
        self.client = client

    def pause_cluster(self, cluster_identifier):
        """
        Pauses the Redshift cluster to stop compute costs.
        """
        try:
            print(f"[Action] Pausing cluster {cluster_identifier}...")
            response = self.client.pause_cluster(ClusterIdentifier=cluster_identifier)
            return response
        except ClientError as e:
            print(f"[Error] Failed to pause cluster: {e}")
            raise e

    def resume_cluster(self, cluster_identifier):
        """
        Resumes the Redshift cluster.
        """
        try:
            print(f"[Action] Resuming cluster {cluster_identifier}...")
            response = self.client.resume_cluster(ClusterIdentifier=cluster_identifier)
            return response
        except ClientError as e:
            print(f"[Error] Failed to resume cluster: {e}")
            raise e

    def get_cluster_status(self, cluster_identifier):
        """
        Checks the current status of the cluster.
        """
        try:
            response = self.client.describe_clusters(
                ClusterIdentifier=cluster_identifier
            )
            status = response["Clusters"][0]["ClusterStatus"]
            return status
        except ClientError as e:
            print(f"[Error] Failed to get cluster status: {e}")
            return "UNKNOWN"
