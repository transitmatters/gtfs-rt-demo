import requests

import gtfs_realtime_pb2

r = requests.get("https://cdn.mbta.com/realtime/VehiclePositions.pb")
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(r.content)

for entity in feed.entity:
    vehicle = entity.vehicle
    trip = vehicle.trip
    position = vehicle.position
    print(
        "TRIP",
        trip.trip_id,
        "ON",
        trip.route_id,
        "AT",
        tuple((round(x, 4) for x in (position.latitude, position.longitude))),
    )
