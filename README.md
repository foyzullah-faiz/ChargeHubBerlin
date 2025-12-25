# ⚡ ChargeHub Berlin (v8.3)

A professional interactive dashboard to locate and manage EV charging infrastructure across Berlin. 

**Live App:** [https://berlinchargingstations.streamlit.app/](https://berlinchargingstations.streamlit.app/)

## 🚀 Key Features
- **Sequential Search Flow:** The map remains clean and blank until a user enters a Postal Code or selects "View All".
- **Uniform ID System:** Every station is assigned a custom identifier: `BER-[PostalCode]-[SerialNumber]` (e.g., `BER-10409-1`).
- **Conditional Status Styling:**
    - **Green:** Available stations.
    - **Red:** Not Available / Maintenance required.
- **Dual-User Interface:**
    - **Driver Mode:** Search, filter by operator, and report malfunctions with real-time success feedback.
    - **Operator Mode:** Administrative view to resolve "Open" tickets highlighted in red.

## 🛠️ Installation & Local Setup
1. Clone this repository:
   `git clone https://github.com/your-username/your-repo-name.git`
2. Install dependencies:
   `pip install -r requirements.txt`
3. Launch the app:
   `streamlit run src/main.py`

## 📊 Data Mapping
The application processes the official **Bundesnetzagentur Ladesäulenregister**. It handles German-specific CSV formatting (semicolon delimiters and comma decimals) and filters coordinates specifically for the Berlin metropolitan area.