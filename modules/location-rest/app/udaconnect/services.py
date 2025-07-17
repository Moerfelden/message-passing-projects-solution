import json
import logging
import os
from app.udaconnect.schemas import LocationSchema
from kafka import KafkaProducer
from typing import Dict

TOPIC_LOCATION = os.environ["TOPIC_LOCATION"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

class LocationService:
    @staticmethod
    def create(location: Dict):
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")
 
        kafka_data = json.dumps(location).encode()
        producer.send(TOPIC_LOCATION, kafka_data)
        producer.flush()
