from src.shared.infrastructure.repositories.csv_repository import CsvChargingStationRepository
from src.shared.application.services.station_service import StationService

def test_search_real_berlin_data():
    # 1. Setup the Real Repository (reading the actual CSV file)
    real_repo = CsvChargingStationRepository()
    
    # 2. Setup the Real Service
    service = StationService(real_repo)
    
    # 3. Execute: Search for a known Berlin Zip Code (e.g., 10117 or 10115)
    #    (We assume your CSV contains 10115 based on standard Berlin data)
    results = service.get_stations_for_zip("10115")
    
    # 4. Assert: We should find at least one station
    print(f"Found {len(results)} stations in 10115")
    assert len(results) > 0
    
    # Optional: Check if the data looks correct
    first_station = results[0]
    assert first_station.postal_code == "10115"
    assert first_station.station_id is not None