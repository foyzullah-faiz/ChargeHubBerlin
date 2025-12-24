import pytest
import os
from src.shared.application.services.malfunction_service import MalfunctionService

TEST_DB_FILE = "tests/test_malfunctions.json"

@pytest.fixture
def service():
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
    svc = MalfunctionService(storage_file=TEST_DB_FILE)
    yield svc
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

def test_report_station_malfunction(service):
    station_id = "1234"
    reason = "Cable broken"
    success = service.report_malfunction(station_id, reason)
    assert success is True
    assert service.is_station_broken(station_id) is True

def test_healthy_station_is_not_broken(service):
    assert service.is_station_broken("9999") is False