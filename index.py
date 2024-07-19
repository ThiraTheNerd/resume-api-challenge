import json
import logging
import boto3


logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    logger.info("#### Lambda API event #### - %s" % event)

    # Get the Http Method from API Request
    http_method = event['requestContext']['http']['method']
    
    # Get the Path details from API Request
    path = event['requestContext']['http']['path']


    if http_method == "GET":
        logger.info('Handling Customer API - Get request')  

        # Get Resume Id from Path Parameter
        resume_id = ""
        if (path.rfind("/") > -1):
            resume_id = path[path.rfind("/") +1: len(path)]
    
        data = dynamodb_client.get_item(
            TableName='Resumes',
            Key={
                'resumeId': {
                  'S': resume_id
                }
            }
         )
         
        if "Item" in data:
            response_body = json.dumps(data['Item'])
        else:
            response_body = json.dumps("Resume not found")
            
        return {
            'statusCode': 200,
            'body': response_body
        }        

    if http_method == "POST":
        logger.info('Handling Resume API - Post request')  
        http_body = event['body']
        print(type(http_body))
        
        data = dynamodb_client.put_item(
            TableName='Resumes',
            Item=json.loads(http_body)
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
