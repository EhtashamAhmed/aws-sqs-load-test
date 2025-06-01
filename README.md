# SQS Message Flooder

This Python script is designed to run as an AWS Lambda function to flood a specified number of messages to an Amazon SQS queue at a controlled rate. It is intended for load testing purposes to verify the robustness of a system that triggers a Lambda function to send push notifications to client devices, ensuring no notifications are missed under high message volumes.

## Prerequisites

- An AWS account with permissions to:
  - Execute Lambda functions.
  - Send messages to the specified SQS queue.
- The `boto3` library (pre-installed in the AWS Lambda Python runtime).
- An SQS queue and a downstream Lambda function configured to process the messages and send push notifications.

## Configuration

Before deploying and running the script, configure the following environment variables in the AWS Lambda console:

- `NUM_MESSAGES`: The number of messages to send to the SQS queue. Default is `1`.
- `RATE_PER_SECOND`: The rate at which messages are sent, in messages per second. Default is `1`.
- `SUB`: The subscription ID to include in the message body. It is required to identify the client(test user), to recieve the push notification.

Additionally, update the `queue_url` variable in the script (`QUEUE_URL`) to the URL of your target SQS queue.

## Usage

1. Deploy the script as an AWS Lambda function:
   - Create a new Lambda function in the AWS Management Console.
   - Use the Python runtime (e.g., Python 3.9 or later).
   - Copy the script into the Lambda function code editor or upload it as a `.zip` file.
2. Set the environment variables in the Lambda configuration.
3. Trigger the Lambda function manually (e.g., via a test event) or through an event source like API Gateway or CloudWatch Events.

The script will execute and send the specified number of messages to the SQS queue at the defined rate.

## Script Details

The script performs the following actions:

1. Initializes an SQS client using `boto3`.
2. Retrieves configuration from environment variables: number of messages (`NUM_MESSAGES`), rate per second (`RATE_PER_SECOND`), and subscription ID (`SUB`).
3. Calculates the delay between messages based on the specified rate.
4. Constructs a JSON message body with a test title, message, and the subscription ID.
5. Sends the specified number of messages to the SQS queue with delays to maintain the rate.
6. Returns a success response with the number of messages sent and the rate.

## Notes

- **AWS Rate Limits**: Ensure your SQS queue and Lambda function can handle the specified rate and volume without exceeding AWS quotas.
- **Costs**: Sending a large number of messages may incur SQS and Lambda usage costs.
- **Timeout**: The Lambda function’s timeout must be sufficient to send all messages (e.g., for 100 messages at 10 messages/sec, set timeout > 10 seconds).
- **Testing**: Verify the downstream Lambda function correctly processes messages and sends push notifications to the set test client.