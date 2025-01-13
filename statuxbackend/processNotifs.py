from google.cloud import pubsub_v1
import time

PROJECT_ID = 'internshipwebapp'
SUBSCRIPTION_ID = 'email-sub'

def process_message(message):
    print(f"Received message: {message.data.decode('utf-8')}")
    # Add your Gmail-specific processing logic here
    message.ack()

def main():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    print(f"Listening for messages on {subscription_path}...")
    subscriber.subscribe(subscription_path, callback=process_message)

    # Keep the script running
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Shutting down listener...")

if __name__ == '__main__':
    main()
