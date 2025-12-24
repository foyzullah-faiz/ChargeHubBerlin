from abc import ABC, abstractmethod
from typing import List
from src.shared.domain.entities.charging_station import ChargingStation

class ChargingStationRepository(ABC):
    @abstractmethod
    def find_by_postal_code(self, postal_code: str) -> List[ChargingStation]:
        """Finds all charging stations within a specific postal code area."""
        pass