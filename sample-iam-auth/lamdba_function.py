import os

def lambda_handler(event, context):
    secret_token = os.environ['secret_token']
    print(event)
    
    try: 
        token = event['headers']['authorizationtoken']
    except Exception as e:
        print("Error: ", str(e))
    if token:
        print(token)
    else:
        print("Authorization token not found")
    
    # Perform your authorization logic here, e.g., verify a JWT token
    if token == secret_token:
       response = {
                "isAuthorized": True
            }
    else:
      response = {
                "isAuthorized": True
            }
        
    print(response)
    
    return response
