import gpsd

class GPS:
    def __init__(self):
        gpsd.connect()
        # gpsd.watch()

    # Use this function to get the current GPS data
    def get_gps_data():
        current = gpsd.get_current()

        # response example:

        # return {
        #     "lat": 52.3553194,
        #     "lon": 4.9571569,
        #     "hspeed": 0,
        #     "track": 0,
        #     "mode": 3,
        #     "time": "2024-01-01T00:00:00.000Z",
        #     "error": {
        #         "x": 0.1,
        #         "y": 0.1,
        #         "z": 0.1,
        #     }
        # }

        # Check if nofix
        if current.mode < 2:
            return {"lat": 0, "lon": 0, "speed": 0, "heading": 0,
                    "mode": current.mode, "time": current.time}

        return {
            "lat": current.lat,
            "lon": current.lon,
            "speed": current.hspeed,
            "heading": current.track,
            "mode": current.mode,
            "time": current.time,
            "error": current.error
        }
