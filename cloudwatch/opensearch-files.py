import boto3
import os
cloudwatch_client = boto3.client('cloudwatch', region_name='ap-south-1')



os.environ['AWS_REGION'] = 'ap-south-1'
ACCOUNT_ID = os.environ['ACCOUNT_ID']
response = cloudwatch_client.put_metric_alarm(
    AlarmName='opensearch-files-node-issue',
    AlarmDescription='opensearch-files-node-issue',
    ActionsEnabled=True,
    AlarmActions=[
        'arn:aws:sns:ap-south-1:xx:devops-slack-alerts',
    ],
    MetricName='Nodes',
    Namespace='AWS/ES',
    Statistic='Average',
    Dimensions=[
        {
            'Name': 'DomainName',
            'Value': 'files'
        },
        {
            'Name': 'ClientId',
            'Value': ACCOUNT_ID
        }
    ],
    Period=60,
    EvaluationPeriods=1,
    Threshold=5,
    ComparisonOperator='LessThanThreshold',
    Tags=[
        {
            'Key': 'Application',
            'Value': 'vault'
        },
    ]
)

print(response)


