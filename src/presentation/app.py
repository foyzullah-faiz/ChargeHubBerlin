import streamlit as st
import pandas as pd
import pydeck as pdk

# Import your services
from src.shared.infrastructure.repositories.csv_repository import CsvChargingStationRepository
from src.shared.application.services.station_service import StationService
from src.shared.application.services.malfunction_service import MalfunctionService

def main():
    # 1. Page Configuration
    st.set_page_config(page_title="ChargeHub Berlin", layout="wide")
    st.title("⚡ ChargeHub Berlin")
    st.markdown("Find charging stations and report maintenance issues.")

    # ---------------------------------------------------------
    # USE CASE 2: MALFUNCTION REPORTING (Sidebar)
    # ---------------------------------------------------------
    st.sidebar.header("🔧 Report Malfunction")
    st.sidebar.info("See a broken charger? Report it here.")

    # Initialize the Malfunction Service
    malfunction_service = MalfunctionService()

    # Create the Form
    with st.sidebar.form("report_form"):
        station_id_input = st.text_input("Station ID (Copy from table)")
        issue = st.selectbox("Issue Type", 
                           ["Screen Broken", "Cable Damaged", "Card Reader Fail", "No Power", "Other"])
        
        submitted = st.form_submit_button("🚨 Submit Report")
        
        if submitted and station_id_input:
            # Save the report to the JSON file
            malfunction_service.report_malfunction(station_id_input, issue)
            st.sidebar.success(f"✅ Report saved for ID: {station_id_input}")

    st.sidebar.markdown("---")

    # ---------------------------------------------------------
    # USE CASE 1: SEARCH & MAP (Main Area)
    # ---------------------------------------------------------
    
    # Initialize Repository & Service
    repo = CsvChargingStationRepository("data/Ladesaeulenregister.csv")
    service = StationService(repo)

    # Search Input
    st.sidebar.header("🔎 Search Filter")
    zip_code = st.sidebar.text_input("Enter Zip Code (Berlin)", "10115")

    # Get Data
    stations = service.get_stations_for_zip(zip_code)

    # Display Results
    if stations:
        # Convert to DataFrame for Streamlit
        data = [
            {
                "Station ID": s.station_id, 
                "Operator": s.operator, 
                "Street": s.street, 
                "lat": s.lat, 
                "lon": s.lon,
                # Check if it is broken (We will use this for colors later!)
                "Status": "🔴 Broken" if malfunction_service.is_station_broken(s.station_id) else "🟢 Available"
            }
            for s in stations
        ]
        df = pd.DataFrame(data)

        # 1. Metrics
        col1, col2 = st.columns(2)
        col1.metric("Stations Found", len(df))
        col2.metric("Broken Stations", len(df[df["Status"] == "🔴 Broken"]))

        # 2. Map
        st.subheader(f"📍 Map of {zip_code}")
        
        # Define the Map Layer
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position='[lon, lat]',
            get_color='[0, 200, 0, 160]',  # Green color for all (we will upgrade this next!)
            get_radius=100,
            pickable=True
        )

        view_state = pdk.ViewState(
            latitude=df["lat"].mean(),
            longitude=df["lon"].mean(),
            zoom=13,
            pitch=40
        )

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=view_state,
            layers=[layer],
            tooltip={"text": "{Operator}\n{Street}\nStatus: {Status}"}
        ))

        # 3. Data Table
        st.subheader("📋 Station Details")
        st.dataframe(df)

    else:
        st.warning("No stations found for this Zip Code.")

if __name__ == "__main__":
    main()