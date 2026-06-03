# Telecom Customer Churn Analytical System

A comprehensive CLI-based analytical system designed to process and analyze telecom customer churn data using AWS S3 and Amazon Redshift.

## 🚀 Key Features

- **Automated Infrastructure**: Provision S3 buckets and Redshift clusters directly from the CLI.
- **Data Ingestion**: Seamlessly upload CSV/JSON data to S3 and load it into Redshift using the Data API.
- **Robust Schema**: Implements a wide staging schema (38 columns) to capture the full breadth of customer data.
- **Analytical Processing**: Generates a final analytical table by joining customer churn data with regional population datasets.
- **Advanced Analysis**: Built-in reports for churn rates, top churn cities, tenure distribution, and revenue loss.
- **Database Optimization**: Integrated `VACUUM` and `ANALYZE` operations for maintaining peak Redshift performance.
- **Cost Management**: Pause and Resume the Redshift cluster from the CLI to optimize AWS spend.

## 🛠️ Project Structure

- `cli/`: Command-pattern based CLI framework and concrete command implementations.
- `infra/`: AWS client factory and infrastructure provisioning logic.
- `services/`: Specialized managers for S3 and Redshift operations.
- `sql/`: 
    - `create_tables.sql`: Staging and population table schemas.
    - `load_data.sql`: Optimized `COPY` command template.
    - `create_analytical_table.sql`: JOIN logic for final data modeling.
    - `analysis/`: Collection of specialized analytical SQL scripts.
- `utils/`: Display utilities and record formatting.
- `reset_db.py`: Standalone script for quick schema resets.

## 📋 Prerequisites

1. **Python 3.8+**
2. **AWS Credentials**: Configured via profiles or environment variables.
3. **Environment Variables**: Create a `.env` file with the following:
    ```env
    REGION=your-region
    BUCKET_NAME=your-s3-bucket
    MAIN_PROFILE=your-aws-profile
    SECONDARY_PROFILE=your-secondary-profile
    REDSHIFT_CLUSTER_IDENTIFIER=your-cluster-id
    REDSHIFT_ROLE_ARN=arn:aws:iam::...:role/your-redshift-role
    REDSHIFT_DBNAME=dev
    REDSHIFT_MASTER_USERNAME=admin
    REDSHIFT_MASTER_PASSWORD=your-password
    ```

## 🎮 Usage Guide

Run the main application:
```bash
python main.py
```

### Main Menu Options:
1. **Deploy Infrastructure**: Setup your AWS environment.
2. **Upload Data to S3**: Stage your raw CSV files.
3. **Create Redshift Tables**: Establish the base schema.
4. **Load Data into Redshift**: Perform the `COPY` operation from S3.
5. **Verify Data Loads**: Check row counts across all tables.
6. **Create Final Analytical Table**: Perform the JOIN to create the final dataset.
7. **Perform Data Analysis**: Access the sub-menu for deep-dive reports.
8. **Perform Redshift Maintenance**: Run `VACUUM` and `ANALYZE`.
9. **Pause Redshift Cluster**: Stop costs when not in use.
10. **Resume Redshift Cluster**: Start the cluster for new analysis.

## 📈 Analysis Suite
The system provides out-of-the-box insights into:
- Overall Churn Rate
- Top 10 Churn Cities
- Churn Distribution by Tenure (0-5+ years)
- Total Revenue Lost to Churn
- Population vs. Customer Density by Zip Code
