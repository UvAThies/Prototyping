import gpsd

class GPS:
    def __init__(self):
        """Class to handle GPS data retrieval from connected GPS devices.
        """        
        gpsd.connect()

    def get_gps_data(self):
        """
        Retrieves GPS data from the connected GPS device.

        Returns:
            dict: A dictionary containing the structured GPS data.
        """
        current = gpsd.get_current()

        # Check if no fix
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
