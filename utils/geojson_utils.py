import json

class GeoJSONProcessor:
    def __init__(self, geojson_file):
        self.geojson_file = geojson_file
        self.data = None
    
    def load_data(self):
        """Load GeoJSON data"""
        with open(self.geojson_file, 'r') as f:
            self.data = json.load(f)
        return self.data
    
    def extract_city_centroids(self):
        """Extract city names and their centroid coordinates"""
        if not self.data:
            self.load_data()
        
        city_data = []
        for feature in self.data['features']:
            city_name = feature['properties'].get('CDTFA_CITY', 'Unknown')
            geometry = feature['geometry']
            
            centroid = self._calculate_centroid(geometry)
            if centroid:
                city_data.append((city_name, centroid[0], centroid[1]))
        
        return city_data
    
    def _calculate_centroid(self, geometry):
        """Calculate centroid of geometry"""
        if geometry['type'] == 'Polygon':
            coords = geometry['coordinates'][0]
        elif geometry['type'] == 'MultiPolygon':
            coords = geometry['coordinates'][0][0]
        else:
            return None
        
        lats = [coord[1] for coord in coords]
        lons = [coord[0] for coord in coords]
        return (sum(lats) / len(lats), sum(lons) / len(lons))