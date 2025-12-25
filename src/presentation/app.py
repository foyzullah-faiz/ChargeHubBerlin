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
    from src.shared.application.services.malfunction_service import MalfunctionService
except ImportError:
    st.error("❌ System Error: Internal modules not found.")
    st.stop()

@st.cache_data
def get_berlin_data(_path):
    try:
        # Load using German CSV standards
        df = pd.read_csv(_path, sep=';', encoding='utf-8', low_memory=False)
        df.columns = df.columns.str.strip()
        
        data = []
        zip_counters = {} 
        
        for i, row in df.iterrows():
            lat_str = str(row.get('Breitengrad', '0')).replace(',', '.').strip(' .')
            lon_str = str(row.get('Längengrad', '0')).replace(',', '.').strip(' .')
            
            try:
                lat, lon = float(lat_str), float(lon_str)
                # Geographic Authentication: Filter for Berlin Bounding Box
                if 52.3 <= lat <= 52.7 and 13.0 <= lon <= 13.8:
                    zip_val = str(row.get('Postleitzahl', '')).split('.')[0].zfill(5) if pd.notna(row.get('Postleitzahl')) else "00000"
                    
                    zip_counters[zip_val] = zip_counters.get(zip_val, 0) + 1
                    serial_no = zip_counters[zip_val]
                    station_id = f"BER-{zip_val}-{serial_no}"
                    
                    data.append({
                        "lat": lat, "lon": lon,
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
    st.title("⚡ ChargeHub Berlin (v8.6)")

    malfunction_service = MalfunctionService()
    all_data = get_berlin_data(CSV_PATH)
    
    # 🗝️ AUTHENTICATION: Get list of valid Berlin ZIP codes from dataset
    valid_berlin_zips = sorted(list({s['zip'] for s in all_data if s['zip'] != "00000"}))

    if 'success_msg' in st.session_state:
        st.success(st.session_state['success_msg'])
        del st.session_state['success_msg']

    st.sidebar.title("User Role")
    role = st.sidebar.radio("Select Access Mode:", ["🚗 Driver (Public)", "👮 Operator (Admin)"])
    st.sidebar.markdown("---")

    display_list = [] 

    # --- 🔎 STEP 1: AUTHENTICATED SEARCH ---
    st.sidebar.header("1. Search Area")
    zip_input = st.sidebar.text_input("Enter 5-digit Berlin Zip Code", "").strip()
    view_all = st.sidebar.checkbox("View All Berlin Stations")

    if view_all:
        display_list = all_data
    elif zip_input:
        # Check authentication of input
        if not zip_input.isdigit() or len(zip_input) != 5:
            st.sidebar.error("⚠️ Invalid Format: Must be 5 digits.")
        elif zip_input not in valid_berlin_zips:
            st.sidebar.error(f"❌ '{zip_input}' is not a valid Berlin ZIP code.")
        else:
            display_list = [s for s in all_data if s['zip'] == zip_input]
            st.sidebar.success(f"✅ Found {len(display_list)} stations in {zip_input}")

    # --- 🔎 STEP 2: SEQUENTIAL FILTERS ---
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

    # --- 🗺️ MAP & TABLE RENDER ---
    view_state = pdk.ViewState(latitude=52.5200, longitude=13.4050, zoom=10)
    layers = []
    if display_list:
        plot_df = pd.DataFrame([{
            "lat": s['lat'] + random.uniform(-0.0002, 0.0002),
            "lon": s['lon'] + random.uniform(-0.0002, 0.0002),
            "color": [220, 20, 60] if s['status'] == "Not Available" else [34, 139, 34],
            "ID": s['station_id'], "Operator": s['operator'], "Status": s['status']
        } for s in display_list])

        layers.append(pdk.Layer("ScatterplotLayer", data=plot_df, get_position="[lon, lat]", get_fill_color="color", get_radius=80, pickable=True, stroked=True, get_line_color=[0, 0, 0], line_width_min_pixels=1))

    st.pydeck_chart(pdk.Deck(map_style='https://basemaps.cartocdn.com/gl/positron-gl-style/style.json', initial_view_state=view_state, layers=layers, tooltip={"html": "<b>ID:</b> {ID}<br/><b>Status:</b> {Status}"}))

    if display_list:
        st.markdown("### 📋 Station Details")
        table_df = pd.DataFrame([{ "ID": s['station_id'], "Operator": s['operator'], "Street": s['street'], "Zip": s['zip'], "Status": s['status'] } for s in display_list])
        def color_status(val): return f"color: {'#2ecc71' if val == 'Available' else '#e74c3c'}; font-weight: bold"
        st.dataframe(table_df.style.applymap(color_status, subset=['Status']), use_container_width=True)

    # --- 🚦 ROLE TOOLS ---
    if role == "🚗 Driver (Public)":
        if not display_list and not view_all and not zip_input: st.info("💡 Map is blank. Please enter a ZIP code.")
        st.sidebar.markdown("---")
        with st.sidebar.form("report_form", clear_on_submit=True):
            st.header("🔧 Report Issue")
            issue_type = st.selectbox("Issue Type", ["Screen Broken", "No Power", "Cable Damaged", "Other"])
            station_id_input = st.text_input("Station ID")
            other_desc = st.text_input("Description (Required)") if issue_type == "Other" else ""
            if st.form_submit_button("🚨 Submit"):
                valid_ids = {s['station_id'] for s in all_data}
                if station_id_input.strip() not in valid_ids: st.error("❌ Invalid ID.")
                else:
                    malfunction_service.report_malfunction(station_id_input.strip(), issue_type)
                    st.session_state['success_msg'] = f"✅ Reported {station_id_input}!"
                    st.rerun()
    else:
        st.sidebar.warning("🔒 Admin Mode")
        reports = malfunction_service.get_all_reports()
        if reports:
            rep_df = pd.DataFrame(reports)
            rep_df['status'] = 'Open'
            st.dataframe(rep_df.style.applymap(lambda v: 'color: #e74c3c; font-weight: bold' if v == 'Open' else '', subset=['status']), use_container_width=True)
            fix_id = st.selectbox("Resolve ID", rep_df['station_id'].tolist())
            if st.button("Mark Fixed"):
                malfunction_service.resolve_malfunction(fix_id)
                st.session_state['success_msg'] = f"✅ Station {fix_id} resolved."
                st.rerun()

if __name__ == "__main__": main()