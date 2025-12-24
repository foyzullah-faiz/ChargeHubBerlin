import json
import os
from datetime import datetime

class MalfunctionService:
    def __init__(self, data_path="src/maintenance/infrastructure/datasets/malfunctions.json"):
        self.data_path = data_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        # Create folder if missing
        if not os.path.exists(os.path.dirname(self.data_path)):
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        
        # Create file if missing
        if not os.path.exists(self.data_path):
            with open(self.data_path, 'w') as f:
                json.dump([], f)

    def report_malfunction(self, station_id: str, description: str):
        """Adds a new broken report."""
        reports = self.get_all_reports()
        
        new_report = {
            "station_id": station_id,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "status": "Open"
        }
        reports.append(new_report)
        self._save_reports(reports)

    def resolve_malfunction(self, station_id: str):
        """Removes all reports for a station (Fixes it)."""
        reports = self.get_all_reports()
        # Keep only reports that do NOT match this station
        active_reports = [r for r in reports if r["station_id"] != station_id]
        self._save_reports(active_reports)

    def get_all_reports(self):
        """Returns the list of all broken stations."""
        try:
            with open(self.data_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def is_station_broken(self, station_id: str) -> bool:
        """Checks if a station is currently broken."""
        reports = self.get_all_reports()
        for r in reports:
            if r["station_id"] == station_id:
                return True
        return False

    def _save_reports(self, reports):
        with open(self.data_path, 'w') as f:
            json.dump(reports, f, indent=4)