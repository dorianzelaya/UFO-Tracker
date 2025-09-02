from data.data_loader import UFODataLoader
from map.base_map import BaseMap
from map.layers import LayerManager
import config

def main():
    # Load and prepare data
    loader = UFODataLoader(config.CSV_FILE)
    ca_data = loader.filter_by_state("CA")
    map_data = loader.prepare_map_data(ca_data)
    
    # Create base map
    base_map = BaseMap(config.DEFAULT_MAP_CENTER, config.DEFAULT_ZOOM)
    ufomap = base_map.create_map()
    
    # Create layer manager
    layer_manager = LayerManager(ufomap, config.POPUP_STYLE)
    
    # Add all layers
    layer_manager.add_marker_layer(map_data, show=True)
    layer_manager.add_heatmap_layer(map_data, show=True)
    layer_manager.add_city_boundaries(config.GEOJSON_FILE, show=True)
    layer_manager.add_city_labels(config.GEOJSON_FILE, config.MAJOR_CITIES, show=True)
    
    # Finalize map
    base_map.add_layer_control()
    base_map.add_zoom_js()
    base_map.save(config.OUTPUT_FILE)
    
    print(f"Map saved to {config.OUTPUT_FILE}")

if __name__ == "__main__":
    main()