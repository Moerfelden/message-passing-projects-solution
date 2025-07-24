import logging
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import LocationService
from datetime import datetime
from flask_accepts import accepts
from flask_restx import Namespace, Resource
from flask import request, Response
from typing import Optional, List

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

# TODO: This needs better exception handling

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-rest")

@api.route("/locations", methods=['POST'])
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    def post(self):
        if request.method == 'POST':
            try:
                payload = request.get_json()
                logger.info(f"{datetime.now()} A new location is sent to the Kafka broker: {payload}")     
                LocationService.create(payload)
            except:
                logger.error(f"{datetime.now()} An issue occurred sending this new location to the Kafka broker: {payload}")     
                Response(status=400)
            else: return Response(status=202)
        else:
            raise Exception('Unsupported HTTP request type.')

