from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import LocationService
from datetime import datetime
from flask_accepts import accepts
from flask_restx import Namespace, Resource
from flask import request, Response
from typing import Optional, List

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-rest")

# TODO: This needs better exception handling

@api.route("/locations")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    def post(self):
        if request.method == 'POST':
            try:
                payload = request.get_json()
                logger.info(f"{datetime.now()} A new location is sent to the Kafka broker: {payload}")     
                LocationService.create(payload)
                return Response(status=202)
            except Exception as e:
                logger.error(f"{datetime.now()} An issue occurred sending this new location to the Kafka broker: {payload}, Error: {e}")     
                return Response(status=400)
        else:
            raise Exception('Unsupported HTTP request type.')
