import os

def create_perfect_scaffold():
    """
    Creates the project structure EXACTLY matching the screenshot.
    - Fixes the 'FileNotFoundError' for root files.
    - Places CSVs in shared/infrastructure/datasets correctly.
    - Enforces PascalCase for Python classes.
    """
    
    # ==========================================
    # 1. DIRECTORIES (Folders)
    # ==========================================
    directories = [
        # --- Root ---
        "src",
        "tests",

        # --- Contexts (src/*) ---
        "src/charging",      # Discovery (Your TDD Focus)
        "src/community",     # Professor's Example
        "src/feedback",      # Empty context from screenshot
        "src/presentation",  # Empty context from screenshot
        "src/shared",        # Shared Kernel
        "src/maintenance",   # Your extra context (Malfunction)

        # --- Community Internal Structure (The Blueprint) ---
        "src/community/application/services",
        "src/community/domain/aggregates",
        "src/community/domain/entities",
        "src/community/domain/events",
        "src/community/domain/value_objects",
        "src/community/infrastructure/repositories",

        # --- Charging Internal Structure (Mirrors Community) ---
        "src/charging/application/services",
        "src/charging/domain/aggregates",
        "src/charging/domain/entities",
        "src/charging/domain/events",
        "src/charging/domain/value_objects",
        "src/charging/infrastructure/repositories",

        # --- Maintenance Internal Structure (Mirrors Community) ---
        "src/maintenance/application/services",
        "src/maintenance/domain/aggregates",
        "src/maintenance/domain/events",
        "src/maintenance/domain/value_objects",
        "src/maintenance/infrastructure/repositories",

        # --- Shared Structure (The Datasets) ---
        "src/shared/application",
        "src/shared/domain/value_objects",
        "src/shared/infrastructure/datasets/berlin_bezirke",       # Folder shown in screenshot
        "src/shared/infrastructure/datasets/berlin_postleitzahlen", # Folder shown in screenshot

        # --- Test Structure (From Screenshot) ---
        "tests/charging",
        "tests/community",
        "tests/feedback",
        "tests/shared",
        "tests/maintenance",
    ]

    # ==========================================
    # 2. FILES (Content)
    # ==========================================
    files = {
        # --- Root Files ---
        "README.md": "# Charging Hub Berlin\n",
        "requirements.txt": "pytest\npandas\n",
        "src/config.py": "# Global Config\n",
        "src/main.py": "# Entry Point\n",
        "src/__init__.py": "",

        # --- SHARED INFRASTRUCTURE (The "Datasets" mismatch you noticed) ---
        "src/shared/infrastructure/datasets/__init__.py": "",
        "src/shared/infrastructure/datasets/geodata_berlin_dis.csv": "",
        "src/shared/infrastructure/datasets/geodata_berlin_plz.csv": "",
        "src/shared/infrastructure/datasets/Ladesaeulenregister.csv": "",
        "src/shared/infrastructure/datasets/link_list.txt": "",       
        "src/shared/infrastructure/datasets/plz_einwohner.csv": "",   
        "src/shared/infrastructure/datasets/Verkehrsaufkommen.csv": "", 

        # --- COMMUNITY CONTEXT (Exact Screenshot Match) ---
        "src/community/application/services/UserService.py": "class UserService:\n    pass\n",
        "src/community/domain/aggregates/UserAggregate.py": "class UserAggregate:\n    pass\n",
        "src/community/domain/entities/User.py": "class User:\n    pass\n",
        "src/community/domain/value_objects/Address.py": "class Address:\n    pass\n",
        "src/community/domain/value_objects/UserRole.py": "class UserRole:\n    pass\n",
        "src/community/domain/events/BadgeAwardedEvent.py": "class BadgeAwardedEvent:\n    pass\n",
        "src/community/domain/events/PointsAddedEvent.py": "class PointsAddedEvent:\n    pass\n",
        "src/community/domain/events/ReviewAddedEvent.py": "class ReviewAddedEvent:\n    pass\n",
        "src/community/domain/events/UserCreatedEvent.py": "class UserCreatedEvent:\n    pass\n",
        "src/community/domain/events/UserUpdatedEvent.py": "class UserUpdatedEvent:\n    pass\n",
        "src/community/infrastructure/repositories/InMemoryUserRepository.py": "class InMemoryUserRepository:\n    pass\n",
        "src/community/infrastructure/repositories/UserRepository.py": "class UserRepository:\n    pass\n",
        "src/community/infrastructure/repositories/UserRepositoryInterface.py": "class UserRepositoryInterface:\n    pass\n",

        # --- CHARGING CONTEXT (Discovery Use Case) ---
        "src/charging/application/services/ChargingStationService.py": 
            "class ChargingStationService:\n    pass\n",
        
        "src/charging/domain/aggregates/ChargingStationAggregate.py": 
            "class ChargingStationAggregate:\n    pass\n",

        "src/charging/domain/events/StationDisabledEvent.py": 
            "class StationDisabledEvent:\n    pass\n",

        "src/charging/infrastructure/repositories/InMemoryChargingStationRepository.py": 
            "class InMemoryChargingStationRepository:\n    pass\n",

        # --- MAINTENANCE CONTEXT (Malfunction Use Case) ---
        "src/maintenance/application/services/MalfunctionService.py": 
            "class MalfunctionService:\n    pass\n",
        
        "src/maintenance/domain/aggregates/MalfunctionReportAggregate.py": 
            "class MalfunctionReportAggregate:\n    pass\n",

        "src/maintenance/domain/value_objects/ReportStatus.py": "class ReportStatus:\n    pass\n",
        "src/maintenance/domain/value_objects/PhotoEvidence.py": "class PhotoEvidence:\n    pass\n",
        "src/maintenance/domain/events/MalfunctionReportedEvent.py": "class MalfunctionReportedEvent:\n    pass\n",
        "src/maintenance/infrastructure/repositories/InMemoryMalfunctionRepository.py": "class InMemoryMalfunctionRepository:\n    pass\n",

        # --- SHARED DOMAIN ---
        "src/shared/domain/value_objects/PostalCode.py": "class PostalCode:\n    pass\n",
        "src/shared/domain/value_objects/StationId.py": "class StationId:\n    pass\n",

        # --- TESTS (The Red Test) ---
        "tests/charging/test_station_search.py": 
            "import pytest\n"
            "from src.charging.application.services.ChargingStationService import ChargingStationService\n"
            "from src.charging.infrastructure.repositories.InMemoryChargingStationRepository import InMemoryChargingStationRepository\n"
            "from src.shared.domain.value_objects.PostalCode import PostalCode\n\n"
            "def test_search_stations_by_valid_zip_code():\n"
            "    # Arrange\n"
            "    repository = InMemoryChargingStationRepository()\n"
            "    service = ChargingStationService(repository)\n"
            "    valid_zip = PostalCode('10117')\n\n"
            "    # Act\n"
            "    stations = service.find_stations_by_zip(valid_zip)\n\n"
            "    # Assert\n"
            "    assert isinstance(stations, list)\n",
        
        "tests/maintenance/test_malfunction_reporting.py": "",
        "tests/community/__init__.py": "",
        "tests/feedback/__init__.py": "",
        "tests/shared/__init__.py": ""
    }

    print("🚀 Generating PERFECT Professor-Aligned Scaffold...")

    # 1. Create Directories & __init__.py files
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # Add __init__.py to every directory (Matches visual requirement)
        init_file = os.path.join(directory, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                pass 

    # 2. Create Files
    for file_path, content in files.items():
        # FIX: Check if parent_dir exists (avoid crash on root files like README.md)
        parent_dir = os.path.dirname(file_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
            
        # Write content
        with open(file_path, "w") as f:
            f.write(content)

    print("✅ Done! Files created successfully.")
    print("👉 Run: 'python -m pytest tests/charging/test_station_search.py'")

if __name__ == "__main__":
    create_perfect_scaffold()