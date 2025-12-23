import csv
import sys
from pathlib import Path
from typing import List, Optional
from src.shared.domain.entities.charging_station import ChargingStation

# Increase field limit for large files
csv.field_size_limit(sys.maxsize)

class CsvChargingStationRepository:
    """
    Repository for accessing charging station data from CSV files.
    Implements the reading logic for the Berlin Ladesaeulenregister.
    """
    
    def __init__(self, file_path: Optional[str] = None):
        if file_path:
             self.file_path = Path(file_path)
        else:
             self.file_path = Path("src/shared/infrastructure/datasets/berlin_postleitzahlen/Ladesaeulenregister.csv")

    def find_by_postal_code(self, search_zip: str) -> List[ChargingStation]:
        found_stations: List[ChargingStation] = []
        
        try:
            # 'utf-8-sig' handles the hidden BOM character in some Windows CSVs
            with open(self.file_path, mode='r', encoding='utf-8-sig', errors='replace') as csvfile:
                
                reader = csv.DictReader(csvfile, delimiter=';')
                
                for row in reader:
                    clean_row = {k.strip(): v for k, v in row.items() if k}
                    
                    row_zip = clean_row.get('Postleitzahl') or clean_row.get('PLZ')
                    
                    if row_zip == search_zip:
                        # Try common German column names for the Operator/ID
                        station_id = (
                            clean_row.get('Betreiber') or 
                            clean_row.get('Ladesäule_ID') or 
                            clean_row.get('Anzeigename') or 
                            clean_row.get('Name') or 
                            clean_row.get('Einrichtung') or
                            'Unknown'
                        )

                        try:
                            lat_str = clean_row.get('Breitengrad', '0').replace(',', '.')
                            lon_str = clean_row.get('Längengrad', '0').replace(',', '.')
                            lat = float(lat_str)
                            lon = float(lon_str)
                        except ValueError:
                            lat, lon = 0.0, 0.0

                        station = ChargingStation(station_id, row_zip, lat, lon)
                        found_stations.append(station)
                        
        except FileNotFoundError:
            print(f"Error: Could not find file at {self.file_path}")
            
        return found_stations