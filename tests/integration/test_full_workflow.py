import pytest
import os
from src.shared.application.services.station_service import StationService
from src.shared.application.services.malfunction_service import MalfunctionService
from src.shared.infrastructure.repositories.csv_repository import CsvChargingStationRepository

# 1. Setup paths for temporary test data
TEST_CSV = "tests/integration/temp_stations.csv"
TEST_JSON = "tests/integration/temp_malfunctions.json"

@pytest.fixture
def setup_integration():
    # A. Create a fake CSV with 1 station
    os.makedirs("tests/integration", exist_ok=True)
    with open(TEST_CSV, "w") as f:
        f.write("Betreiber;Strasse;Hausnummer;Postleitzahl;Ort;Bundesland;Kreis;Breitengrad;Laengengrad;Nennleistung Ladeeinrichtung [kW];Art der Ladeeinrichung;Anzahl Ladepunkte\n")
        f.write("Vattenfall;Musterstrasse;1;10115;Berlin;Berlin;Berlin;52.5;13.4;22;Normal;2\n")

    # B. Ensure JSON is clean
    if os.path.exists(TEST_JSON):
        os.remove(TEST_JSON)

    yield

    # C. Cleanup after test
    if os.path.exists(TEST_CSV):
        os.remove(TEST_CSV)
    if os.path.exists(TEST_JSON):
        os.remove(TEST_JSON)

def test_search_and_report_workflow(setup_integration):
    # --- PHASE 1: DISCOVERY (Use Case 1) ---
    # Initialize the Station Service
    repo = CsvChargingStationRepository(TEST_CSV)
    station_service = StationService(repo)
    
    # User searches for Zip "10115"
    stations = station_service.get_stations_for_zip("10115")
    
    # Assert we found the station
    assert len(stations) == 1
    target_station = stations[0]
    station_id = target_station.station_id  # This identifies the station

    # --- PHASE 2: REPORTING (Use Case 2) ---
    # Initialize the Malfunction Service
    malfunction_service = MalfunctionService(storage_file=TEST_JSON)
    
    # User reports THIS specific station as broken
    malfunction_service.report_malfunction(station_id, "Screen Broken")

    # --- PHASE 3: VERIFICATION (Integration) ---
    # Check if the system knows it is broken
    is_broken = malfunction_service.is_station_broken(station_id)
    
    # Assertions
    assert is_broken is True
    assert malfunction_service.get_malfunction_reason(station_id) == "Screen Broken"