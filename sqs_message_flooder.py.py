import json
import boto3
import time
import os

def lambda_handler(event, context):
    # Initialize SQS client
    sqs = boto3.client('sqs')

    # Define the queue URL
    queue_url = 'QUEUE_URL'

    # Fetch parameters from environment variables
    num_messages = int(os.environ.get('NUM_MESSAGES', 1))
    rate_per_second = int(os.environ.get('RATE_PER_SECOND', 1))
    sub_value = os.environ.get('SUB', 'SUB_ID')  


    # Calculate delay between messages based on rate
    delay_between_messages = 1 / rate_per_second

    # Construct JSON message body
    message_body = {
        "title": "MTronic contact sensor alert TEST",
        "message": "cs sensor opened detected. TEST",
        "sub": sub_value
    }

    # Sample JSON message attributes
    message_attributes = {
        'MessageBody': json.dumps(message_body),
        'QueueUrl': queue_url
    }
    print("message:", message_attributes)
    # Send specified number of JSON messages to SQS
    for i in range(num_messages):
        # Send JSON message to SQS
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_attributes['MessageBody'],
        )
        
        # Print response
        print(response)

        # Delay between messages
        if i < num_messages - 1:
            time.sleep(delay_between_messages)

    return {
        'statusCode': 200,
        'body': json.dumps(f'{num_messages} message(s) sent to SQS successfully at {rate_per_second} messages per second')
    }