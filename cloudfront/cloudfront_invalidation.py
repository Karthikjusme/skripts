import json
import urllib.parse
import boto3
import os
import time

DISTRIBUTION_NAME=os.environ['DISTRIBUTION_NAME']

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    s3 = boto3.client('s3')
    client = boto3.client('sts')
    timestamp = time.time()
    
    response_iam = client.assume_role(
    ExternalId='prod-aws-eka-care',
    RoleArn=os.getenv('ROLE_ARN'),
    RoleSessionName='lambdacfinvalidation'
    )
    ACCESS_KEY=response_iam['Credentials']['AccessKeyId']
    SECRET_KEY=response_iam['Credentials']['SecretAccessKey']
    SESSION_TOKEN=response_iam['Credentials']['SessionToken']

    print(response_iam)    

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response_s3 = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response_s3['ContentType'])
        print(event['Records'][0]['s3']['object']['key'])
        invalidation_path=event['Records'][0]['s3']['object']['key']
        print("invalidating /" + invalidation_path)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
                  
    cloudfront_client = boto3.client('cloudfront', region_name='ap-south-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, aws_session_token=SESSION_TOKEN,)
    try: 
        response_cloudfront = cloudfront_client.create_invalidation(
            DistributionId=DISTRIBUTION_NAME,
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': [
                        "/" + invalidation_path,
                    ]
                },
                'CallerReference'
                : 'lambda invalidating /' + invalidation_path +  " at " + str(timestamp)
            }
        )
        print(response_cloudfront)

    except Exception as e:
        print(e)
        raise e
    


