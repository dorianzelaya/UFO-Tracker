from data.data_loader import UFODataLoader
from map.base_map import BaseMap
from map.layers import LayerManager
from map.stats_dashboard import UFOStatsDashboard  # Add this import
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
    
    # NEW: Add statistics dashboard
    stats_dashboard = UFOStatsDashboard(map_data, config.POPUP_STYLE)
    ufomap = stats_dashboard.add_to_map(ufomap)
    
    # Finalize map
    #base_map.add_layer_control()
    base_map.add_zoom_js()
    base_map.save(config.OUTPUT_FILE)
    
    print(f"Map saved to {config.OUTPUT_FILE}")
    print(f"Statistics Dashboard Added:")
    print(f"  - Total Sightings: {stats_dashboard.stats['total_sightings']:,}")
    print(f"  - Unique Cities: {stats_dashboard.stats['unique_cities']}")
    print(f"  - Most Common Shape: {stats_dashboard.stats['most_common_shape']}")
    print(f"  - Peak Year: {stats_dashboard.stats['peak_year']}")

if __name__ == "__main__":
    main()