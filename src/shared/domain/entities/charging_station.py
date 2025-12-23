class ChargingStation:
    def __init__(self, station_id: str, postal_code: str, lat: float = 0.0, lon: float = 0.0):
        self.station_id = station_id
        self.postal_code = postal_code
        self.lat = lat
        self.lon = lon