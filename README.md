# gtfs-rt-demo

This is a minimal demo we hacked together during a working session to read vehicle positions from
the MBTA's [GTFS Realtime](https://developers.google.com/transit/gtfs-realtime) feed. GTFS-RT uses 
a binary format called [protobuf](https://developers.google.com/protocol-buffers), which makes it a bit more complicated to work with than other MBTA products. To extract a GTFS-RT feed, you need three
things:

- The URL of the feed itself — e.g. [here](https://www.mbta.com/developers/gtfs-realtime) for the MBTA
- A `.proto` file describing the structure of GTFS-RT to Protobuf — e.g. the one checked into source as here `gtfs-realtime.proto`
- Protobuf's [`protoc`](https://grpc.io/docs/protoc-installation/) command line tool.

You can use `protoc` to unpack and view data from the feed:

```
curl -s https://cdn.mbta.com/realtime/VehiclePositions.pb | protoc gtfs-realtime.proto --decode transit_realtime.FeedMessage
```

Here, `transit_realtime` is the package name provided in `gtfs-realtime.proto`, and `FeedMessage` is a
message entity defined in that file. Running this command prints:

```proto
entity {
  id: "y1777"
  vehicle {
    trip {
      trip_id: "53317138"
      schedule_relationship: SCHEDULED
      route_id: "9"
      direction_id: 1
    }
    position {
      latitude: 42.3514175
      longitude: -71.0705185
      bearing: 162
    }
    current_stop_sequence: 4
    current_status: IN_TRANSIT_TO
    timestamp: 1662592634
    stop_id: "145"
    vehicle {
      id: "y1777"
      label: "1777"
    }
    occupancy_status: FEW_SEATS_AVAILABLE
    10: 40
  }
}
# and hundreds more...
```

This repo also contains a minimal Python script to extract GTFS-RT vehicle positions. We need the
`protobuf` PyPI package, but we also need to generate a Python representation of the `.proto` file,
again using `protoc`:

```
protoc --python_out=. gtfs-realtime.proto
```

This file is checked into source as `gtfs_realtime_pb2.py`. This is a Python module that contains,
among other things, a class for each message type in `gtfs-realtime.proto`:

```
>>> import gtfs_realtime_pb2
>>> dir(gtfs_realtime_pb2)
[..., 'EntitySelector', 'FeedEntity', 'FeedHeader', 'FeedMessage', 'Position', 'TimeRange', 'TranslatedString', 'TripDescriptor', 'TripUpdate', 'VehicleDescriptor', 'VehiclePosition', ...]
```

You can inspect `example.py` to see how to instantiate entities from a feed URL.

## Run it yourself

You'll need [poetry](https://python-poetry.org/) to manage Python dependencies. Then:

```
poetry install
poetry run python example.py
```
