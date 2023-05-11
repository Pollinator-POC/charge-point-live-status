from time import sleep

import boto3
from confluent_kafka import Consumer, KafkaError, KafkaException
import os
import logging

from heartbeat_request_handler import HeartbeatRequestHandler
from heartbeat_request_writer import HeartbeatRequestWriter
from status_notification_request_handler import StatusNotificationRequestHandler
from status_notification_request_writer import StatusNotificationRequestWriter
from generic_handler import GenericHandler
from router import Router

delay = os.environ.get("DELAY_START_SECONDS", 240)
sleep(int(delay))

group_id = os.environ.get("CONSUMER_GROUP_ID")
storage_host = os.environ.get("STORAGE_HOST")
storage_port = os.environ.get("STORAGE_PORT")


dynamodb_client = boto3.client(
    'dynamodb',
    region_name='local',
    endpoint_url=f"http://{storage_host}:{storage_port}",
    aws_access_key_id="X",
    aws_secret_access_key="X"
)

heartbeat_request_writer = HeartbeatRequestWriter(client=dynamodb_client)
status_notification_request_writer = StatusNotificationRequestWriter(client=dynamodb_client)
heartbeat_request_handler = HeartbeatRequestHandler(writer=heartbeat_request_writer)
status_notification_request_handler = StatusNotificationRequestHandler(writer=status_notification_request_writer)
generic_handler = GenericHandler()
router = Router(heartbeat_request_handler=heartbeat_request_handler, status_notification_request_handler=status_notification_request_handler, generic_handler=generic_handler)
conf = {
    'bootstrap.servers': os.environ.get("BOOTSTRAP_SERVERS", "localhost:9092"),
    'broker.address.family': 'v4',
    'group.id': group_id,
    'auto.offset.reset': 'smallest'
}

consumer = Consumer(conf)

running = True

def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logging.info('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                decoded_message = msg.value().decode("utf-8")
                handler = router.get_handler(decoded_message)
                handler(decoded_message)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def shutdown():
    running = False


topics_to_consume = os.environ.get("TOPICS_TO_CONSUME", "").split(",")
basic_consume_loop(consumer, topics_to_consume)