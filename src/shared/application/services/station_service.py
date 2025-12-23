from typing import List
from src.shared.domain.entities.charging_station import ChargingStation
from src.shared.infrastructure.repositories.csv_repository import CsvChargingStationRepository

class StationService:
    """
    Application Service that orchestrates the search for charging stations.
    It acts as the bridge between the UI (Streamlit) and the Data Layer (CSV).
    """
    
    def __init__(self, repository: CsvChargingStationRepository):
        """
        Initialize the service with a specific data repository.
        
        Args:
            repository (CsvChargingStationRepository): The data access object.
        """
        self.repository = repository

    def get_stations_for_zip(self, postal_code: str) -> List[ChargingStation]:
        """
        Retrieve all charging stations for a given postal code.
        
        Args:
            postal_code (str): The zip code to search for (e.g. "10115").
            
        Returns:
            List[ChargingStation]: A list of found stations.
        """
        # We can add extra business logic here later (e.g., logging, validation)
        return self.repository.find_by_postal_code(postal_code)