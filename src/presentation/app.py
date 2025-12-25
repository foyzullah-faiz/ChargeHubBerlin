import sys
import os
import streamlit as st
import pandas as pd
import pydeck as pdk
import random

# ==========================================
# 🚨 PATH & DATA SETUP
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

CSV_PATH = os.path.join(project_root, "src", "maintenance", "infrastructure", "datasets", "Ladesaeulenregister.csv")

try:
    from src.shared.infrastructure.repositories.csv_repository import CsvChargingStationRepository
    from src.shared.application.services.station_service import StationService
    from src.shared.application.services.malfunction_service import MalfunctionService
except ImportError:
    st.error("❌ System Error: Internal modules not found.")
    st.stop()

@st.cache_data
def get_berlin_data(_path):
    try:
        df = pd.read_csv(_path, sep=';', encoding='utf-8', low_memory=False)
        df.columns = df.columns.str.strip()
        
        data = []
        zip_counters = {} 
        
        for i, row in df.iterrows():
            lat_str = str(row.get('Breitengrad', '0')).replace(',', '.').strip(' .')
            lon_str = str(row.get('Längengrad', '0')).replace(',', '.').strip(' .')
            
            try:
                lat, lon = float(lat_str), float(lon_str)
                # Filter for Berlin Bounding Box
                if 52.3 <= lat <= 52.7 and 13.0 <= lon <= 13.8:
                    zip_val = str(row.get('Postleitzahl', '')).split('.')[0].zfill(5) if pd.notna(row.get('Postleitzahl')) else "00000"
                    
                    # Sequential Serial Number Logic: BER-PLZ-Serial
                    zip_counters[zip_val] = zip_counters.get(zip_val, 0) + 1
                    serial_no = zip_counters[zip_val]
                    station_id = f"BER-{zip_val}-{serial_no}"
                    
                    data.append({
                        "lat": lat, 
                        "lon": lon,
                        "operator": str(row.get('Betreiber', 'Unknown')).strip(),
                        "station_id": station_id,
                        "zip": zip_val,
                        "street": str(row.get('Straße', 'Unknown')).strip()
                    })
            except: continue
        return data
    except Exception as e:
        st.error(f"Error loading CSV data: {e}")
        return []

def main():
    st.set_page_config(page_title="ChargeHub Berlin", layout="wide")
    st.title("⚡ ChargeHub Berlin")

    malfunction_service = MalfunctionService()
    all_data = get_berlin_data(CSV_PATH)

    # --- 📢 SUCCESS MESSAGE HANDLER ---
    if 'success_msg' in st.session_state:
        st.success(st.session_state['success_msg'])
        del st.session_state['success_msg']

    st.sidebar.title("User Role")
    role = st.sidebar.radio("Select Access Mode:", ["🚗 Driver (Public)", "👮 Operator (Admin)"])
    st.sidebar.markdown("---")

    display_list = [] 

    # --- 🔎 SEARCH & FILTER ---
    st.sidebar.header("1. Search Area")
    zip_input = st.sidebar.text_input("Enter 5-digit Berlin Zip Code", "")
    view_all = st.sidebar.checkbox("View All Berlin Stations")

    if view_all:
        display_list = all_data
    elif zip_input.isdigit() and len(zip_input) == 5:
        display_list = [s for s in all_data if zip_input in s['zip']]

    if display_list:
        st.sidebar.markdown("---")
        st.sidebar.header("2. Status Filter")
        status_filter = st.sidebar.multiselect("Availability:", ["Available", "Not Available"], default=["Available", "Not Available"])
        
        temp_list = []
        for s in display_list:
            is_broken = malfunction_service.is_station_broken(s['station_id'])
            status = "Not Available" if is_broken else "Available"
            if status in status_filter:
                s_copy = s.copy()
                s_copy['status'] = status
                temp_list.append(s_copy)
        display_list = temp_list

    if display_list:
        st.sidebar.header("3. Company Filter")
        ops = sorted(list({s['operator'] for s in display_list}))
        selected_ops = st.sidebar.multiselect("Select Operators:", ops, default=ops)
        display_list = [s for s in display_list if s['operator'] in selected_ops]

    # --- 🗺️ MAP RENDER ---
    view_state = pdk.ViewState(latitude=52.5200, longitude=13.4050, zoom=10)
    layers = []

    if display_list:
        plot_df = pd.DataFrame([{
            "lat": s['lat'] + random.uniform(-0.0002, 0.0002),
            "lon": s['lon'] + random.uniform(-0.0002, 0.0002),
            "color": [220, 20, 60] if s['status'] == "Not Available" else [34, 139, 34],
            "ID": s['station_id'], "Operator": s['operator'], "Status": s['status']
        } for s in display_list])

        layers.append(pdk.Layer(
            "ScatterplotLayer", data=plot_df, get_position="[lon, lat]",
            get_fill_color="color", get_radius=80, pickable=True,
            stroked=True, get_line_color=[0, 0, 0], line_width_min_pixels=1
        ))

    st.pydeck_chart(pdk.Deck(
        map_style='https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
        initial_view_state=view_state, layers=layers,
        tooltip={"html": "<b>ID:</b> {ID}<br/><b>Operator:</b> {Operator}<br/><b>Status:</b> {Status}", "style": {"color": "white"}}
    ))

    # --- 📊 STATION TABLE ---
    if display_list:
        st.markdown("### 📋 Station Details")
        table_df = pd.DataFrame([{
            "ID": s['station_id'], "Operator": s['operator'],
            "Street": s['street'], "Zip": s['zip'], "Status": s['status']
        } for s in display_list])
        
        def color_status(val):
            color = '#2ecc71' if val == 'Available' else '#e74c3c'
            return f'color: {color}; font-weight: bold'

        st.dataframe(table_df.style.applymap(color_status, subset=['Status']), use_container_width=True)

    # --- 🚦 ROLE TOOLS ---
    if role == "🚗 Driver (Public)":
        if not display_list and not view_all and not zip_input:
            st.info("💡 Map is blank. Please search a Zip Code to find chargers.")
        
        st.sidebar.markdown("---")
        st.sidebar.header("🔧 Report Issue")
        issue_type = st.sidebar.selectbox("Issue Type", ["Screen Broken", "No Power", "Cable Damaged", "Other"])

        with st.sidebar.form("report_form", clear_on_submit=True):
            station_id_input = st.text_input("Station ID")
            other_desc = st.text_input("Description (Required)") if issue_type == "Other" else ""

            if st.form_submit_button("🚨 Submit Report"):
                clean_id = station_id_input.strip()
                valid_ids = {s['station_id'] for s in all_data}
                
                if clean_id not in valid_ids:
                    st.error("❌ Invalid ID. Please check the table or map.")
                elif issue_type == "Other" and not other_desc:
                    st.error("❌ Please provide a description for 'Other'.")
                else:
                    final_issue = issue_type if issue_type != "Other" else f"Other: {other_desc}"
                    malfunction_service.report_malfunction(clean_id, final_issue)
                    # Use session state for persistent success message
                    st.session_state['success_msg'] = f"✅ Success! Issue for {clean_id} has been reported."
                    st.rerun()

    else: # OPERATOR MODE
        st.sidebar.warning("🔒 Admin Access Enabled")
        st.markdown("---")
        st.subheader("🛠️ Maintenance Dashboard")
        reports = malfunction_service.get_all_reports()
        if reports:
            report_df = pd.DataFrame(reports)
            if 'status' not in report_df.columns:
                report_df['status'] = 'Open' # Default for active reports
            
            # 🛠️ COLOR "OPEN" AS RED FOR OPERATOR
            def color_open(val):
                return 'color: #e74c3c; font-weight: bold' if val == 'Open' else ''

            st.dataframe(report_df.style.applymap(color_open, subset=['status']), use_container_width=True)
            
            fix_id = st.selectbox("Select Station ID to Resolve", report_df['station_id'].tolist())
            if st.button("Mark as Fixed/Available"):
                malfunction_service.resolve_malfunction(fix_id)
                st.session_state['success_msg'] = f"✅ Station {fix_id} is now back online."
                st.rerun()
        else:
            st.success("No active malfunctions detected.")

if __name__ == "__main__":
    main()