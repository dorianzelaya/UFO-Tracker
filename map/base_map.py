import folium
from .styling import get_popup_css, get_zoom_responsive_js

class BaseMap:
    def __init__(self, center, zoom_start=11, tiles="jawg_matrix"):
        self.center = center
        self.zoom_start = zoom_start
        self.tiles = tiles
        self.map = None
        # Your Jawg access token
        self.jawg_token = "99pVx9Hsuz1q74VGgdqFiTdIJC3iwfiUGYEUudNKkhg8i8m8GbWkx7rcdSvXVXU4"
        
    def create_map(self):
        """Create the base folium map"""
        if self.tiles == "jawg_matrix":
            # Create map without default tiles
            self.map = folium.Map(
                location=self.center,
                zoom_start=self.zoom_start,
                tiles=None  # Don't load default tiles
            )
            
            # Add your updated custom Jawg style with {r} for retina support
            jawg_custom_url = f"https://tile.jawg.io/a5e97229-6841-42b0-a061-699608acacf8/{{z}}/{{x}}/{{y}}{{r}}.png?access-token={self.jawg_token}"
            folium.TileLayer(
                tiles=jawg_custom_url,
                attr='<a href="https://www.jawg.io?utm_medium=map&utm_source=attribution" target="_blank">&copy; Jawg</a> - <a href="https://www.openstreetmap.org?utm_medium=map-attribution&utm_source=jawg" target="_blank">&copy; OpenStreetMap</a>&nbsp;contributors',
                name='Jawg Custom UFO Style',
                overlay=False,
                control=True
            ).add_to(self.map)
            
        else:
            # Fallback to standard tiles
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