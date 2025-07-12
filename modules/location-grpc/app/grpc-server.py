import grpc
import location_pb2
import location_pb2_grpc
import logging
import os
import time
from concurrent import futures
from datetime import datetime, timedelta
from geoalchemy2.functions import ST_Point
from models import Location
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from typing import Dict, List

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]


Session = sessionmaker()
engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
Session.configure(bind=engine)

logging.basicConfig(level=logging.WARNING)
logging.getLogger("location-grpc")

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Get(self, request, context):
        request_value = {
            "id": int(request.id)
        }

        retrieve_request = location_pb2.RetrieveLocation(**request_value)  		       
        print("The grpc server received the following protobuf message:")
        print(retrieve_request)

        with Session() as session:
            location = (
                session.query(Location)
                .filter(Location.id == request.id)
                .one()
            )

        location_dict = {
            "id": location.id,
            "person_id": location.person_id,
            "creation_time": location.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            "latitude": location.latitude,
            "longitude": location.longitude
        }
        print("Finished retrieving the location from DB:")
        print(location_dict)
   
        return location_pb2.LocationMessage(**location_dict)				


    def Create(self, request, context):
        request_value = {
            "person_id": int(request.person_id),
            "creation_time": str(request.creation_time),
            "latitude": str(request.latitude),
            "longitude": str(request.longitude)
        }

        create_request = location_pb2.LocationMessage(**request_value)       
        print("The grpc server received the following protobuf message:")
        print(create_request)

        #DB prep and commits
        new_location = Location()
        new_location.person_id = request.person_id
        new_location.creation_time = request.creation_time
        new_location.coordinate = ST_Point(request.latitude, request.longitude)
        
        with Session() as session:
            session.add(new_location)
            session.commit()

        print("Finished committing the new location to DB")

        return create_request

# Initialize the grpc server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

print("The grpc server is running on port 5005, nodeport 30004.")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
