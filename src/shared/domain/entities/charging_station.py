from dataclasses import dataclass

@dataclass
class ChargingStation:
    station_id: str
    operator: str  # <--- This was likely missing!
    street: str
    zip_code: str
    lat: float
    lon: float