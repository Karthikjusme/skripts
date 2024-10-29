import boto3

def set_log_group_retention_to_1_day():
    # Create CloudWatch Logs client
    client = boto3.client('logs', region_name='ap-south-1')
    
    # Paginate through all log groups
    paginator = client.get_paginator('describe_log_groups')
    for page in paginator.paginate():
        log_groups = page['logGroups']
        for log_group in log_groups:
            log_group_name = log_group['logGroupName']
            try:
                # Get current retention period
                response = client.describe_log_groups(logGroupNamePrefix=log_group_name)

                current_retention = response['logGroups'][0].get('retentionInDays')
                # Set retention to 1 day if it's not already set
                if current_retention is None:
                    client.put_retention_policy(logGroupName=log_group_name, retentionInDays=1)
                    # print(log_group_name, current_retention)
                    print(f"Set retention for {log_group_name} to 1 day")
                else:
                    continue
                    # print(f"Retention for {log_group_name} is already set to {current_retention} days")
            except Exception as e:
                print(f"Error setting retention for {log_group_name}: {e}")

if __name__ == "__main__":
    set_log_group_retention_to_1_day()
