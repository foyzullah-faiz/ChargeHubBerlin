import pytest
from unittest.mock import MagicMock
from src.shared.domain.entities.charging_station import ChargingStation
# We are importing the Service we haven't created yet (This causes the Failure)
from src.shared.application.services.station_service import StationService

def test_search_stations_by_zip():
    # Arrange: Create a "fake" repository
    # We don't want to read the real CSV in this test (that's the repository's job)
    mock_repo = MagicMock()
    
    # We tell the fake repo: "When someone asks for '10115', return this specific station"
    fake_station = ChargingStation("ID-123", "10115")
    mock_repo.find_by_postal_code.return_value = [fake_station]

    # Initialize the Service with our fake repo
    service = StationService(mock_repo)

    # Act: Call the service method
    result = service.get_stations_for_zip("10115")

    # Assert: Check if the service returned what the repo gave it
    assert len(result) == 1
    assert result[0].station_id == "ID-123"
    
    # Verify the service actually called the repository
    mock_repo.find_by_postal_code.assert_called_once_with("10115")