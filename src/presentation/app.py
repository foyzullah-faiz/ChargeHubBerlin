import streamlit as st
import sys
import os

# --- 1. PATH FIX ---
# We need to tell Python where the 'src' folder is.
# app.py is in: src/presentation/
# We go up 2 levels to get to the Project Root: src/presentation/ -> src/ -> Root/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
sys.path.insert(0, project_root)

# --- 2. IMPORTS ---
from src.shared.infrastructure.repositories.csv_repository import CsvChargingStationRepository
from src.shared.application.services.station_service import StationService

# --- 3. SETUP BACKEND ---
# Initialize the Repository and Service (Dependency Injection)
repo = CsvChargingStationRepository()
service = StationService(repo)

# --- 4. BUILD UI ---
st.set_page_config(page_title="Berlin Charging Hub", page_icon="⚡", layout="wide")

st.title("Berlin Charging Hub ⚡")
st.markdown("### Search for Charging Stations by Zip Code")

# Sidebar for Search
with st.sidebar:
    st.header("Search Settings")
    search_zip = st.text_input("Enter Postal Code (e.g., 10115):", value="10115")
    search_button = st.button("Search Stations")

# Main Content Area
if search_button:
    if search_zip:
        # Call the Application Service
        stations = service.get_stations_for_zip(search_zip)
        
        if stations:
            st.success(f"Found {len(stations)} charging stations in {search_zip}.")
            
            # --- MAP SECTION ---
            st.subheader(f"📍 Map of Stations in {search_zip}")
            
            # Prepare data for Map (Streamlit requires 'lat' and 'lon' columns)
            map_data = [
                {'lat': s.lat, 'lon': s.lon} 
                for s in stations 
                if s.lat != 0 and s.lon != 0
            ]
            
            if map_data:
                st.map(map_data)
            else:
                st.warning("No GPS coordinates available for these stations.")

            # --- TABLE SECTION ---
            st.subheader("📋 Station Details")
            
            # Prepare data for Table (Displaying Operator/ID clearly)
            table_data = [
                {
                    "Operator / ID": s.station_id, 
                    "Postal Code": s.postal_code,
                    "Latitude": s.lat,
                    "Longitude": s.lon
                } 
                for s in stations
            ]
            st.table(table_data)
                
        else:
            st.error(f"No stations found for postal code: {search_zip}.")
    else:
        st.warning("Please enter a zip code to search.")
else:
    st.info("👈 Enter a zip code in the sidebar to start searching.")