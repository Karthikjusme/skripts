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

    # Replace 'YOUR_WEBHOOK_URL' with your actual Slack webhook URL

    # Message to be sent


# def lambda_handler(event, context):
def lambda_handler(event, context):
    
    ACCOUNT_ID = os.environ['ACCOUNT_ID']
    ACCOUNT_ID_2 = os.environ['ACCOUNT_ID_2']

    client = boto3.client('ce')
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
        Filter = {
            "And": [{
                "Dimensions": {
                    "Key": "LINKED_ACCOUNT",
                    "Values": [ACCOUNT_ID, ACCOUNT_ID_2]

                }
            }, {
                "Not": {
                    "Dimensions": {
                        "Key": "RECORD_TYPE",
                        "Values": ["Credit", "Refund"]
                    }
                }
        }]
        },
        Metrics = ["NetUnblendedCost"],
        GroupBy = [
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }
        ]
    )

    # print(result)
    # keys = []
    # amount = []
    notification_message = "AWS Daily Cost Report for the day: " + str(yesterday_date)
    for group in result["ResultsByTime"][0]["Groups"]:
        # keys.append(group["Keys"][0])
        # amount.append(group["Metrics"]["NetUnblendedCost"]["Amount"])
        key = group["Keys"][0]
        amount = group["Metrics"]["NetUnblendedCost"]["Amount"]
        notification_message += "\n"
        notification_message += str(key) + ": $" + str(amount) 

    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

        # notification_message = "AWS CloudFront Prod Account Usage Cost: ", str(total_amount) + "$"
    send_slack_notification(slack_webhook_url, notification_message)

    # for group in result["ResultsByTime"][0]["Groups"]:
    #     amount_str = group["Metrics"]["NetUnblendedCost"]["Amount"]
    #     amount = float(amount_str)
    #     total_amount += amount        

    # Send the notification
    

lambda_handler(1, 1)