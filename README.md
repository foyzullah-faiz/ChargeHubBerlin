# ⚡ ChargeHub Berlin

A Streamlit-powered dashboard for managing and locating EV charging stations in Berlin. 

## 🚀 Key Features
* **Sequential Search Flow:** The map starts blank and populates only after a Postal Code search or "View All" selection.
* **BER-ID System:** Standardized Station IDs follow the format `BER-[PostalCode]-[SerialNumber]` (e.g., `BER-10115-1`).
* **Dual-Mode UI:** * **Driver Mode:** Locate chargers and report issues (Screen, Cable, Power) with real-time success confirmation.
    * **Operator Mode:** Maintenance dashboard with a list of "Open" tickets highlighted in red.
* **Status Visibility:** Interactive data table with conditional formatting (Green = Available, Red = Not Available).

## 🛠️ Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run src/main.py`

## 📊 Data Source
Data is fetched from the official **Bundesnetzagentur Ladesäulenregister**, filtered for the Berlin metropolitan area using bounding box coordinates.