import boto3
import requests
import json
import os

from datetime import datetime, timedelta

#Define Slack notification Function

def send_slack_notification(webhook_url, message):
    print(message)
    mess = str(message)
    payload = {
        "text": mess
    }

    headers = {
        "Content-Type": "application/json"
    }    

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print("Notification sent successfully to Slack!")
    else:
        print(f"Failed to send notification to Slack. Status code: {response.status_code}, Response: {response.text}")

#     # Replace 'YOUR_WEBHOOK_URL' with your actual Slack webhook URL

#     # Message to be sent

def lambda_handler(event, context):

# def lambda_handler():
    client = boto3.client('sts')
    
    response_iam = client.assume_role(
    ExternalId=os.getenv('EXTERNAL_ID'),
    RoleArn=os.getenv('ROLE_ARN'),
    RoleSessionName='lambdacfinvalidation11'
    )
    ACCESS_KEY=response_iam['Credentials']['AccessKeyId']
    SECRET_KEY=response_iam['Credentials']['SecretAccessKey']
    SESSION_TOKEN=response_iam['Credentials']['SessionToken']
    print(response_iam)

    # print(response_iam)        
    client = boto3.client('ce', region_name='ap-south-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, aws_session_token=SESSION_TOKEN,)
    # Get today's date
    today_date = datetime.now().strftime('%Y-%m-%d')

    # Get yesterday's date
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # print("Today's date:", today_date)
    # print("Yesterday's date:", yesterday_date)

    result = client.get_cost_and_usage(
        TimePeriod = {
            'Start': yesterday_date,
            'End': today_date
        },
        Granularity = 'DAILY',

        Metrics = ["AmortizedCost"],
        GroupBy = [
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }
        ]
    )

    print(result)

    total_amount = 0.0
    # print(total_amount)
    for group in result["ResultsByTime"][0]["Groups"]:
        amount_str = group["Metrics"]["AmortizedCost"]["Amount"]
        amount = float(amount_str)
        total_amount += amount

    print("Total Cost: {:.2f} USD".format(total_amount))
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    notification_message = "AWS CloudFront UniCloud Account Usage Cost: ", str(total_amount) + "$"
    # Send the notification
    send_slack_notification(slack_webhook_url, notification_message)

