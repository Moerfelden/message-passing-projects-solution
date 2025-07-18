import json
import logging
import os
from concurrent import futures
from geoalchemy2.functions import ST_Point
from kafka import KafkaConsumer
from models import Location
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from typing import Dict, List

TOPIC_LOCATION = os.environ["TOPIC_LOCATION"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]
consumer = KafkaConsumer(TOPIC_LOCATION, bootstrap_servers=[KAFKA_SERVER])

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]


Session = sessionmaker()
engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
Session.configure(bind=engine)

logging.basicConfig(level=logging.WARNING)
logging.getLogger("location-consumer")

def create_location(location)
    request_value = {
        "person_id": int(location["person_id"]),
        "creation_time": str(location["creation_time"]),
        "latitude": str(location["latitude"]),
        "longitude": str(location["longitude"])
    }
     
    print("The location-consumer received the following create location message:")
    print(request_value)

    #DB prep and commits
    new_location = Location()
    new_location.person_id = location["person_id"]
    new_location.creation_time = location["creation_time"]
    new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        
    with Session() as session:
        session.add(new_location)
        session.commit()

    print("Finished committing the new location to DB")


def consume_message():
    for message in consumer:
        decoded_message = message.value.decode("utf-8")
        location = json.loads(decoded_message)
        create_location(location)


if __name__ == "__main__":
    consume_message()
