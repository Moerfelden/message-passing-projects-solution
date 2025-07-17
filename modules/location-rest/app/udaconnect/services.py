import json
import logging
import os
import sys
from app.udaconnect.schemas import LocationSchema
from typing import Dict

# Note: the following lines were inserted to avoid the following python 3.12 issue:
# ModuleNotFoundError: No module named 'kafka.vendor.six.moves'
if sys.version_info >= (3, 12, 0):
    import six
    sys.modules["kafka.vendor.six.moves"] = six.moves
from kafka import KafkaProducer

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
