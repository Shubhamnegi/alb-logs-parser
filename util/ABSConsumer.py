import boto3
import os 
import time
import threading 


import logging
# Configure the AWS credentials and region
aws_access_key_id =  os.getenv('AWS_ACCESS_KEY')
aws_secret_access_key = os.getenv('AWS_SECRET_KEY')
aws_region = os.getenv('AWS_REGION')


# Create an SQS client
sqs = boto3.client('sqs',
                   aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key,
                   region_name=aws_region)


class ABSConsumer():
    def __init__(self,queue_url):
        self.queue_url = queue_url                
        self.enabled = False
        if queue_url== "" or queue_url == None:
            raise Exception("queue_url is required") 
        logging.info(f"registering consumer for {self.queue_url}")

    def start(self):
        logging.info(f"starting consumer for {self.queue_url}")
        self.t = threading.Thread(target=self.consume)
        self.enabled= True
        self.t.start()
        return self.t

    def stop(self):
        logging.info(f'stopping consumer for {self.queue_url}')    
        self.enabled = False        

    def handle_message(self,payload):
        raise Exception('handle_message not implemented')

    def consume(self):        
        # Continuously poll the SQS queue for messages
        while self.enabled:
            # Receive messages from the queue
            response = sqs.receive_message(
                QueueUrl=self.queue_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20  # Long polling
            )

            if self.enabled == False:
                logging.info('Consumer stopped')
                return
            
            # Check if there are any messages
            if 'Messages' in response:
                for message in response['Messages']:
                    # Process the received message
                    logging.info(f"Received message: {message['Body']}")                
                    self.handle_message(message['Body'])

                    # Delete the message from the queue
                    sqs.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )                    
            else:
                # No messages received
                logging.info('No messages available.')
                time.sleep(60) # sleep for 60s
                        

