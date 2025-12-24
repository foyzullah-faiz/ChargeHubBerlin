# ⚡ ChargeHub Berlin

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](PASTE_YOUR_LINK_HERE)

**ChargeHub Berlin** is an interactive dashboard built with **Streamlit** that helps Electric Vehicle (EV) drivers in Berlin find charging stations and report malfunctions. It also provides an interface for operators to track and resolve reported issues.

## 🚀 Features

### 🗺️ For Drivers (Public View)
* **Interactive Map:** Visualizes charging stations using **PyDeck**.
    * **Smart Visibility:** Uses a "jitter" algorithm to slightly separate stacked stations (e.g., in parking lots) so every single plug is visible.
    * **Status Indicators:**
        * 🟢 **Green:** Available
        * 🔴 **Red:** Reported / Malfunctioning
    * **Numbering:** Stations are numbered (1, 2, 3...) on the map and table for easy reference.
* **Search & Filter:**
    * **By Zip Code:** Enter a 5-digit Berlin PLZ (e.g., `10557`).
    * **By Operator:** Sidebar filter to show specific providers (e.g., *Vattenfall*, *Allego*).
* **Report Malfunctions:**
    * Users can report issues like "Screen Broken", "No Power", or "Cable Damaged".
    * **Dynamic Form:** The "Description" text box only appears if "Other" is selected.

### 👮 For Operators (Admin View)
* **Ticket Dashboard:** View a list of all active malfunction reports.
* **Resolve Issues:** Select a station ID and mark it as "Fixed" to instantly turn it back to **Green** on the map.

---

## 🛠️ Tech Stack
* **Python 3.8+**
* **Streamlit** (UI Framework)
* **PyDeck** (Map Visualizations)
* **Pandas** (Data Manipulation)

---

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd chargehub-berlin
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## ▶️ Usage

1.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

2.  **Navigate:**
    * Open your browser at `http://localhost:8501`.
    * Select **"🚗 Driver"** to search for stations.
    * Select **"👮 Operator"** to view reported issues.