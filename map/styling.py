import folium

def get_popup_css():
    """Return CSS for popup styling"""
    return """
    <style>
    .leaflet-popup-content-wrapper {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }
    .leaflet-popup-tip {
        background: transparent !important;
        border: none !important;
    }
    .leaflet-popup-content {
        margin: 0 !important;
        padding: 0 !important;
    }
    .leaflet-interactive {
        outline: none !important;
    }
    .leaflet-interactive:focus {
        outline: none !important;
    }
    path.leaflet-interactive:focus {
        outline: none !important;
    }
    .city-label {
        transition: opacity 0.3s ease;
    }
    .city-label.major-city {
        z-index: 1000;
    }
    .city-label.minor-city {
        z-index: 999;
    }
    </style>
    """

def get_zoom_responsive_js():
    """Return JavaScript for zoom-responsive city labels"""
    return """
    <script>
    setTimeout(function() {
        var mapObj = window[Object.keys(window).find(key => key.startsWith('map_'))];
        
        if (!mapObj) {
            mapObj = window.map;
        }
        
        if (mapObj) {
            mapObj.on('zoomend', function() {
                var zoom = this.getZoom();
                var cityLabels = document.querySelectorAll('.city-label');
                
                cityLabels.forEach(function(label) {
                    if (zoom < 9) {
                        label.style.opacity = '0';
                    } else if (zoom < 11) {
                        if (label.classList.contains('major-city')) {
                            label.style.opacity = '1';
                        } else {
                            label.style.opacity = '0';
                        }
                    } else {
                        label.style.opacity = '1';
                    }
                });
            });
            
            mapObj.fire('zoomend');
        }
    }, 1500);
    </script>
    """

def create_popup_html(formatted_date, city, shape, encounter, style_config):
    """Create styled HTML for popup"""
    return f"""
    <div style="
        background-color: {style_config['background_color']};
        color: {style_config['text_color']};
        font-family: Arial, sans-serif;
        font-size: 14px;
        border: 2px solid {style_config['border_color']};
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.8);
        margin: 0;
        min-width: 250px;
    ">
        <h4 style="margin: 0 0 8px 0; color:{style_config['header_color']}; font-size: 16px;">UFO Sighting</h4>
        <b>Date:</b> {formatted_date}<br>
        <b>City:</b> {city}<br>
        <b>Shape:</b> {shape}<br>
        <b>Encounter:</b> {encounter}
    </div>
    """