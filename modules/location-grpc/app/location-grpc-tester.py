import logging
import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a writer that can be used to send protobuf messages to the gRPC server.
"""

def retrieve_location():
    with grpc.insecure_channel("localhost:30004") as channel:
        stub = location_pb2_grpc.LocationServiceStub(channel)

        request = location_pb2.RetrieveLocation(id=30)
        response = stub.Get(request)
        print("Location retrieved. Response:")
        print(response)


def create_location():
    with grpc.insecure_channel("localhost:30004") as channel:
        stub = location_pb2_grpc.LocationServiceStub(channel)
        
        request = location_pb2.LocationMessage(
           person_id=5,
           creation_time="2025-07-03 20:36:57",
           latitude="29.938632",
           longitude="-90.119941"
        )

        response = stub.Create(request)    
        print("Location created. Response:")
        print(response)


if __name__ == "__main__":
    logging.basicConfig()
    print("The grpc client is sending sample payload to retrieve an existing location")
    retrieve_location()
    print("The grpc client is sending sample payload to create a new location")
    create_location()

# If no 'id' value is provided in the protobuf message for a new location, 
# then the 'id' value will be set automatically by database sequence 'location_id_seq'.
# If no 'creation_time' value is provided in the protobuf message for a new location, 
# then the 'creation_time' value will be set automatically to the current UTC time in the database.
