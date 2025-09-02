import folium
from .styling import get_popup_css, get_zoom_responsive_js

class BaseMap:
    def __init__(self, center, zoom_start=11, tiles="CartoDB dark_matter"):
        self.center = center
        self.zoom_start = zoom_start
        self.tiles = tiles
        self.map = None
        
    def create_map(self):
        """Create the base folium map"""
        self.map = folium.Map(
            location=self.center,
            zoom_start=self.zoom_start,
            tiles=self.tiles
        )
        
        # Add custom CSS
        popup_css = get_popup_css()
        self.map.get_root().html.add_child(folium.Element(popup_css))
        
        return self.map
    
    def add_layer_control(self):
        """Add layer control to the map"""
        if self.map:
            folium.LayerControl().add_to(self.map)
    
    def add_zoom_js(self):
        """Add zoom-responsive JavaScript"""
        if self.map:
            zoom_js = get_zoom_responsive_js()
            self.map.get_root().html.add_child(folium.Element(zoom_js))
    
    def save(self, filename):
        """Save the map to file"""
        if self.map:
            self.map.save(filename)