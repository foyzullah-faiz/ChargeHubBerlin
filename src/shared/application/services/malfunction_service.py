import json
import os
from typing import Dict

class MalfunctionService:
    def __init__(self, storage_file: str = "data/malfunctions.json"):
        # We allow changing the file path so we can use a fake file during testing
        self.storage_file = storage_file
        self.malfunctions: Dict[str, str] = self._load_data()

    def _load_data(self) -> Dict[str, str]:
        """Loads existing reports from the JSON file."""
        if not os.path.exists(self.storage_file):
            return {}
        
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_data(self):
        """Saves the current list of reports to the JSON file."""
        # Ensure the directory exists before saving
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        
        with open(self.storage_file, 'w') as f:
            json.dump(self.malfunctions, f, indent=4)

    def report_malfunction(self, station_id: str, reason: str) -> bool:
        """
        Saves a new malfunction report.
        Returns True if successful.
        """
        self.malfunctions[station_id] = reason
        self._save_data()
        return True

    def is_station_broken(self, station_id: str) -> bool:
        """Returns True if the station is currently reported as broken."""
        return station_id in self.malfunctions
    
    def get_malfunction_reason(self, station_id: str) -> str:
        """Returns the reason why a station is broken (or None)."""
        return self.malfunctions.get(station_id, None)