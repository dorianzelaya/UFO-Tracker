import pandas as pd

class UFODataLoader:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = None
        
    def load_data(self):
        """Load and return the full dataset"""
        self.data = pd.read_csv(self.csv_file)
        return self.data
    
    def filter_by_state(self, state="CA"):
        """Filter data for specific state"""
        if self.data is None:
            self.load_data()
        return self.data[self.data["Location.State"] == state]
    
    def prepare_map_data(self, filtered_data):
        """Extract and clean columns needed for mapping"""
        return {
            'shape': filtered_data["Data.Shape"].astype(str),
            'encounter': filtered_data["Data.Description excerpt"].fillna("No description").astype(str),
            'city': filtered_data["Location.City"].astype(str),
            'lat': filtered_data["Location.Coordinates.Latitude "].astype(float),
            'lon': filtered_data["Location.Coordinates.Longitude "].astype(float),
            'year': filtered_data["Dates.Sighted.Year"].fillna("").astype(str),
            'month': filtered_data["Dates.Sighted.Month"].fillna("").astype(str),
            'day': filtered_data["Date.Sighted.Day"].fillna("").astype(str)
        }