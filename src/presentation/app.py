import streamlit as st
import pandas as pd
import pydeck as pdk
import os
import random

# Import Services
from src.shared.infrastructure.repositories.csv_repository import CsvChargingStationRepository
from src.shared.application.services.station_service import StationService
from src.shared.application.services.malfunction_service import MalfunctionService

def main():
    st.set_page_config(page_title="ChargeHub Berlin", layout="wide")
    st.title("⚡ ChargeHub Berlin")

    # --- CONFIGURATION ---
    CSV_PATH = "src/maintenance/infrastructure/datasets/Ladesaeulenregister.csv" 
    
    if not os.path.exists(CSV_PATH):
        st.error(f"❌ Data file not found at: {CSV_PATH}")
        return

    # --- INITIALIZE SERVICES ---
    repo = CsvChargingStationRepository(CSV_PATH)
    station_service = StationService(repo)
    malfunction_service = MalfunctionService()

    # --- HANDLING SUCCESS MESSAGES ---
    if 'success_msg' in st.session_state:
        st.success(st.session_state['success_msg'])
        del st.session_state['success_msg']

    # ==========================================
    # 👤 SIDEBAR: USER ROLE
    # ==========================================
    st.sidebar.title("👤 User Role")
    role = st.sidebar.radio("Select Mode", ["🚗 Driver (Public)", "👮 Operator (Admin)"])
    st.sidebar.markdown("---")

    # ==========================================
    # 🚀 SEARCH & FILTER AREA
    # ==========================================
    st.sidebar.header("🔎 Search & Filter")
    
    # 1. ZIP CODE SEARCH
    zip_code = st.sidebar.text_input("Enter Zip Code", "10557")
    
    # Fetch stations first based on Zip Code
    all_stations = []
    if zip_code and (not zip_code.isdigit() or len(zip_code) != 5):
        st.sidebar.warning("⚠️ Please enter a valid 5-digit Zip Code.")
    else:
        all_stations = station_service.get_stations_for_zip(zip_code)

    # 2. OPERATOR FILTER (New Feature)
    selected_operators = []
    if all_stations:
        # Get unique operators from the fetched stations and sort them
        unique_operators = sorted(list({s.operator for s in all_stations}))
        
        selected_operators = st.sidebar.multiselect(
            "Filter by Operator",
            options=unique_operators,
            default=[] # Default empty means "Show All"
        )
        
        # Apply Filter
        if selected_operators:
            stations = [s for s in all_stations if s.operator in selected_operators]
        else:
            stations = all_stations
    else:
        stations = []

    valid_station_ids = {s.station_id for s in stations} if stations else set()

    # ==========================================
    # 🔧 DRIVER MODE
    # ==========================================
    if role == "🚗 Driver (Public)":
        st.sidebar.header("🔧 Report Issue")
        
        # MOVED SELECTBOX OUTSIDE FORM (For instant "Other" updates)
        issue_type = st.sidebar.selectbox("Issue Type", ["Screen Broken", "No Power", "Cable Damaged", "Other"])

        with st.sidebar.form("report_form", clear_on_submit=True):
            station_id_input = st.text_input("Station ID (Copy from table)")
            
            other_description = ""
            if issue_type == "Other":
                other_description = st.text_input("Description (Required)")

            submitted = st.form_submit_button("🚨 Submit Report")
            
            if submitted:
                clean_id = station_id_input.strip()
                
                # Check against ALL loaded stations for the zip code, not just filtered ones
                # (Users might want to report a station they know exists even if hidden by filter)
                valid_ids_in_zip = {s.station_id for s in all_stations}

                if clean_id not in valid_ids_in_zip:
                    st.error(f"❌ Invalid ID: '{clean_id}' (Must be in Zip {zip_code})")
                elif issue_type == "Other" and not other_description:
                    st.error("❌ You selected 'Other'. Please write a description.")
                else:
                    final_issue = issue_type if issue_type != "Other" else f"Other: {other_description}"
                    malfunction_service.report_malfunction(clean_id, final_issue)
                    st.session_state['success_msg'] = f"✅ Reported '{clean_id}'"
                    st.rerun()

        st.sidebar.markdown("---")
        
        # --- MAP ---
        st.markdown("### 🗺️ Public Map View")
        
        if stations:
            # Show count of filtered vs total
            if selected_operators:
                st.success(f"✅ Showing {len(stations)} of {len(all_stations)} stations in {zip_code}")
            else:
                st.success(f"✅ Found {len(stations)} stations in {zip_code}")

            data_list = []
            for i, s in enumerate(stations):
                is_broken = malfunction_service.is_station_broken(s.station_id)
                
                if is_broken:
                    status_text = "🔴 Not Available"
                    color = [200, 0, 0, 255] # Red (Solid)
                else:
                    status_text = "🟢 Available"
                    color = [0, 200, 0, 200] # Light Green (Bright)

                # JITTER (Visibility Fix)
                lat_jitter = s.lat + random.uniform(-0.0005, 0.0005)
                lon_jitter = s.lon + random.uniform(-0.0005, 0.0005)

                data_list.append({
                    "No": i + 1,
                    "Station ID": s.station_id,
                    "Operator": s.operator,
                    "Street": s.street,
                    "Status": status_text,
                    "lat": lat_jitter,
                    "lon": lon_jitter,
                    "color": color,
                    "radius": 80,
                    "border": [0, 0, 0]
                })
            
            df = pd.DataFrame(data_list)
            
            # --- LAYERS ---
            scatter_layer = pdk.Layer(
                'ScatterplotLayer', 
                data=df, 
                get_position='[lon, lat]',
                get_fill_color='color',
                get_line_color=[0, 0, 0],
                get_line_width=5,
                get_radius='radius',
                pickable=True,
                filled=True,
                stroked=True
            )

            text_layer = pdk.Layer(
                "TextLayer",
                data=df,
                get_position='[lon, lat]',
                get_text="No",
                get_color=[255, 255, 255],
                get_size=25,
                get_alignment_baseline="'middle'",
                get_text_anchor="'middle'",
                pickable=True
            )

            midpoint = [df["lon"].mean(), df["lat"].mean()]
            view_state = pdk.ViewState(
                latitude=midpoint[1], 
                longitude=midpoint[0], 
                zoom=12,
                pitch=0
            )

            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/streets-v11',
                initial_view_state=view_state,
                layers=[scatter_layer, text_layer],
                tooltip={"text": "No: {No}\n{Operator}\n{Status}\nID: {Station ID}"}
            ))
            
            st.dataframe(df.drop(columns=["color", "radius", "lat", "lon", "border"]).set_index("No"))
        else:
            if zip_code:
                if all_stations and selected_operators:
                    st.warning(f"No stations found for the selected operators in {zip_code}.")
                else:
                    st.warning(f"No stations found for Zip Code: {zip_code}")

    # ==========================================
    # 👮 OPERATOR MODE
    # ==========================================
    else:
        st.markdown("### 👮 Operator Dashboard")
        st.warning("🔒 Restricted Access")

        reports = malfunction_service.get_all_reports()
        
        if reports:
            st.metric("Open Tickets", len(reports))
            df_reports = pd.DataFrame(reports)
            st.dataframe(df_reports)

            col1, col2 = st.columns([3, 1])
            with col1:
                station_to_fix = st.selectbox("Select Station to Fix", df_reports["station_id"].unique())
            with col2:
                st.write("") 
                st.write("") 
                if st.button("✅ Mark Fixed"):
                    malfunction_service.resolve_malfunction(station_to_fix)
                    st.session_state['success_msg'] = f"✅ Station {station_to_fix} Fixed"
                    st.rerun()
        else:
            st.success("✅ No active malfunctions.")

if __name__ == "__main__":
    main()