import folium
from folium.plugins import MarkerCluster, HeatMap
from folium import DivIcon
from .styling import create_popup_html
from utils.geojson_utils import GeoJSONProcessor

class LayerManager:
    def __init__(self, folium_map, style_config):
        self.map = folium_map
        self.style_config = style_config
    
    def add_marker_layer(self, map_data, show=True):
        """Add UFO markers with clustering"""
        marker_group = folium.FeatureGroup(name="UFO Markers", show=show).add_to(self.map)
        marker_cluster = MarkerCluster().add_to(marker_group)
        
        for lt, ln, sh, enc, ct, yr, mn, dy in zip(
            map_data['lat'], map_data['lon'], map_data['shape'], 
            map_data['encounter'], map_data['city'], map_data['year'], 
            map_data['month'], map_data['day']
        ):
            formatted_date = self._format_date(mn, dy, yr)
            html = create_popup_html(formatted_date, ct, sh, enc, self.style_config)
            
            # Replace CircleMarker with UFO emoji marker
            folium.Marker(
                location=[lt, ln],
                icon=DivIcon(
                    icon_size=(30, 30),
                    icon_anchor=(15, 15),
                    html=f'''<div style="
                        font-size: 40px;
                        text-align: center;
                        line-height: 50px;
                        width: 50px;
                        height: 50px;
                    ">🛸</div>''',
                    class_name='ufo-marker'
                ),
                popup=folium.Popup(html, max_width=300, show=True)
            ).add_to(marker_cluster)
    
    def add_heatmap_layer(self, map_data, show=True):
        """Add heatmap layer"""
        heat_group = folium.FeatureGroup(name="Heatmap", show=show).add_to(self.map)
        heat_data = [[lt, ln] for lt, ln in zip(map_data['lat'], map_data['lon'])]
        HeatMap(heat_data, min_opacity=0.5, radius=10).add_to(heat_group)
    
    def add_city_boundaries(self, geojson_file, show=True):
        """Add city boundary layer"""
        folium.GeoJson(
            geojson_file,
            name="City Boundaries",
            show=show,
            style_function=lambda feature: {
                "fillColor": "black",
                "color": "#439dcd",
                "weight": 1,
                "fillOpacity": 0.3,
            },
            highlight_function=lambda feature: {
                "weight": 4,
                "fillColor": "#902C1DFF",
                "fillOpacity": 0.3
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["CDTFA_CITY"],
                aliases=["City:"]
            )
        ).add_to(self.map)
    
    def add_city_labels(self, geojson_file, major_cities, show=True):
        """Add city name labels"""
        city_labels_group = folium.FeatureGroup(name="City Names", show=show).add_to(self.map)
        processor = GeoJSONProcessor(geojson_file)
        city_data = processor.extract_city_centroids()
        
        for city_name, centroid_lat, centroid_lon in city_data:
            if city_name in ['Unknown', '', 'nan'] or len(city_name) < 2:
                continue
                
            is_major = city_name in major_cities
            font_size = '16px' if is_major else '13px'
            font_weight = 'bold' if is_major else 'normal'
            priority_class = 'major-city' if is_major else 'minor-city'
            
            folium.Marker(
                location=[centroid_lat, centroid_lon],
                icon=DivIcon(
                    icon_size=(200, 25),
                    icon_anchor=(100, 12),
                    html=f'''<div style="
                        font-size: {font_size}; 
                        color: white; 
                        font-weight: {font_weight}; 
                        text-align: center;
                        text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
                        font-family: Arial, sans-serif;
                        white-space: nowrap;
                        pointer-events: none;
                    " class="city-label {priority_class}" data-city-name="{city_name}">{city_name}</div>''',
                    class_name=f'city-label {priority_class}'
                )
            ).add_to(city_labels_group)
    
    def _format_date(self, mn, dy, yr):
        """Format date string from components"""
        date_parts = []
        if mn and mn != 'nan':
            date_parts.append(mn)
        if dy and dy != 'nan':
            date_parts.append(dy)
        if yr and yr != 'nan':
            date_parts.append(yr)
        
        if len(date_parts) == 3:
            return f"{mn}/{dy}/{yr}"
        elif len(date_parts) == 2 and yr and yr != 'nan':
            return f"{mn or '?'}/{dy or '?'}/{yr}"
        elif yr and yr != 'nan':
            return f"?/?/{yr}"
        else:
            return "Unknown"