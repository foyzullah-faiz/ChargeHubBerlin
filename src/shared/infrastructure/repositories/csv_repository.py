import pandas as pd
from typing import List
from src.shared.domain.entities.charging_station import ChargingStation
from src.shared.domain.repositories.charging_station_repository import ChargingStationRepository

class CsvChargingStationRepository(ChargingStationRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        try:
            # 1. Try reading with UTF-8 (standard)
            df = pd.read_csv(
                self.file_path, 
                sep=';', 
                encoding='utf-8', 
                on_bad_lines='skip', 
                dtype=str 
            )
            df.columns = df.columns.str.strip()
            return df
        except UnicodeDecodeError:
            # 2. Fallback to Latin1 (common for German Excel CSVs)
            try:
                df = pd.read_csv(
                    self.file_path, 
                    sep=';', 
                    encoding='latin1', 
                    on_bad_lines='skip', 
                    dtype=str
                )
                df.columns = df.columns.str.strip()
                return df
            except Exception as e:
                print(f"❌ Error loading CSV (Encoding): {e}")
                return pd.DataFrame()
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            return pd.DataFrame()

    def find_by_postal_code(self, postal_code: str) -> List[ChargingStation]:
        if self.df.empty or 'Postleitzahl' not in self.df.columns:
            return []

        # Filter by Zip Code
        filtered_df = self.df[self.df['Postleitzahl'] == str(postal_code)]
        
        stations = []
        for index, row in filtered_df.iterrows():
            try:
                # 1. LATITUDE (Breitengrad)
                # German CSV uses comma for decimals (52,516 -> 52.516)
                lat_str = str(row.get('Breitengrad', '0')).replace(',', '.')
                
                # 2. LONGITUDE (Längengrad)
                # Note the German 'ä'. We look for the exact header name.
                lon_str = str(row.get('Längengrad', '0')).replace(',', '.')
                
                # 3. OPERATOR & STREET
                operator = row.get('Betreiber', 'Unknown')
                street = row.get('Straße', 'Unknown') # Note the German 'ß'
                house_num = str(row.get('Hausnummer', ''))
                
                # 4. CREATE ID
                # Since the CSV has no unique ID, we generate one: Operator + Zip + RowIndex
                station_id = f"{operator[:3]}_{postal_code}_{index}"
                
                station = ChargingStation(
                    station_id=station_id,
                    operator=operator,
                    street=f"{street} {house_num}".strip(),
                    zip_code=str(row.get('Postleitzahl', '')),
                    lat=float(lat_str) if lat_str != 'nan' else 0.0,
                    lon=float(lon_str) if lon_str != 'nan' else 0.0
                )
                stations.append(station)
            except ValueError:
                continue 
                
        return stations