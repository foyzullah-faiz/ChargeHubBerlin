# ⚡ ChargeHub Berlin: Smart Infrastructure Dashboard
**A Data-Driven EV Management System for the Berlin Metropolitan Area**

**Live Application:** [https://berlinchargingstations.streamlit.app/](https://berlinchargingstations.streamlit.app/)

---

## 📖 Project Overview
ChargeHub Berlin is a specialized dashboard designed to bridge the gap between EV infrastructure data and real-world usability. It transforms the raw **Bundesnetzagentur (BNetzA)** registry into a functional tool for two distinct user groups: everyday drivers and city maintenance operators.



## 🛠️ The Technical Pipeline
The project follows a 4-stage engineering pipeline to ensure data integrity and performance:

### 1. Data Ingestion & Localization
- **Raw Processing:** The system ingests the official German Ladesäulenregister (CSV). It handles localized formatting challenges, specifically semicolon (`;`) delimiters and comma (`,`) decimal points for geodata.
- **Geofencing:** Stations are filtered using a coordinate bounding box (Lat: 52.3 to 52.7, Lon: 13.0 to 13.8) to strictly isolate the Berlin city limits.

### 2. Standardization & ID Normalization
Since the raw dataset lacks a uniform ID system, this project implements a **Normalization Layer**. Every station is assigned a unique, location-based identifier:
- **Format:** `BER-[PostalCode]-[SerialNumber]` (e.g., `BER-10409-1`).
- **Logic:** This ensures that every physical charging pole is traceable and reportable, even when the source data is missing a unique key.

### 3. Sequential Logic Engine
To maintain a high-performance UI, the application implements a **Trigger-Based Loading Flow**:
- **Initial State:** Map is blank to save resources.
- **Triggers:** Search by Postal Code → Filter by Availability → Filter by Operator.

### 4. Role-Based UI Architecture
- **🚗 Driver Module:** Optimized for quick discovery. Includes a reporting form with dynamic input fields (e.g., "Other" description box only appears when needed).
- **👮 Operator Module:** An administrative dashboard that pulls reported malfunctions into a prioritized list. "Open" tickets are highlighted in **Red** for immediate action.

---

## 📊 Project Structure
```text
ChargeHub-Berlin/
├── README.md               # Full Technical Report & Live Link
├── requirements.txt        # Deployment Dependencies
├── src/
│   ├── main.py             # Application Entry Point & UI Logic
│   ├── shared/             # Domain Logic & Services
│   │   ├── application/    # Malfunction & Station Services
│   │   └── infrastructure/ # CSV Repositories & Data Access
│   └── maintenance/        # Dataset Management