from typing import List
from src.shared.domain.entities.charging_station import ChargingStation
from src.shared.domain.repositories.charging_station_repository import ChargingStationRepository

class StationService:
    def __init__(self, repository: ChargingStationRepository):
        self.repository = repository

    def get_stations_for_zip(self, zip_code: str) -> List[ChargingStation]:
        # Call the corrected method name
        return self.repository.find_by_postal_code(zip_code)