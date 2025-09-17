import folium

def get_popup_css():
    """Return CSS for popup styling with animated glowing border"""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
    
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
    
    /* Glowing Border Animation */
    .ufo-popup-container {
        position: relative;
        min-width: 280px;
        display: inline-block;
    }
    
    .animated-border-box, .animated-border-box-glow {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        overflow: hidden;
        z-index: 0;
        border-radius: 13px;
    }
    
    .animated-border-box-glow {
        overflow: hidden;
        /* Glow Blur */
        filter: blur(15px);
    }
    
    .animated-border-box:before, .animated-border-box-glow:before {
        content: '';
        z-index: -2;
        text-align: center;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(0deg);
        position: absolute;
        width: 99999px;
        height: 99999px;
        background-repeat: no-repeat;
        background-position: 0 0;
        /* Border color with UFO theme colors */
        background-image: conic-gradient(rgba(0,0,0,0), #00ff99, rgba(0,0,0,0) 25%);
        /* Animation speed */
        animation: rotate 3s linear infinite;
    }
    
    /* Alternative multi-color version - uncomment if preferred */
    /*
    .animated-border-box:before, .animated-border-box-glow:before {
        background-image: conic-gradient(
            rgba(0,0,0,0), 
            #00ff99, 
            #006aff,
            #ff0095,
            rgba(0,0,0,0) 40%
        );
    }
    */
    
    .animated-border-box:after {
        content: '';
        position: absolute;
        z-index: -1;
        /* Border width */
        left: 3px;
        top: 3px;
        /* Double the px from the border width */
        width: calc(100% - 6px);
        height: calc(100% - 6px);
        /* Background color */
        background: #1c1f2b;
        /* Box border radius */
        border-radius: 10px;
    }
    
    @keyframes rotate {
        100% {
            transform: translate(-50%, -50%) rotate(1turn);
        }
    }
    
    .ufo-popup-content {
        background: transparent;
        color: #f0f0f0;
        font-family: 'Poppins', Arial, sans-serif;
        padding: 16px;
        border-radius: 10px;
        position: relative;
        z-index: 10;
    }
    
    .ufo-popup-content h4 {
        margin: 0 0 12px 0;
        color: white;
        font-size: 18px;
        font-weight: 600;
        text-align: center;
    }
    
    .ufo-popup-content .info-line {
        margin: 8px 0;
        color: #a2a5b3;
        font-size: 14px;
        line-height: 1.4;
    }
    
    .ufo-popup-content .info-line b {
        color: #f0f0f0;
        font-weight: 500;
    }
    
    .ufo-popup-content .encounter-text {
        margin-top: 12px;
        padding: 8px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 6px;
        font-size: 13px;
        line-height: 1.3;
        color: #a2a5b3;
        border-left: 3px solid #00ff99;
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

def create_popup_html(formatted_date, city, shape, encounter, style_config=None):
    """Create styled HTML for popup with animated glowing border"""
    # Truncate encounter text if too long
    if len(encounter) > 150:
        encounter = encounter[:147] + "..."
    
    return f"""
    <div class="ufo-popup-container">
        <div class="animated-border-box-glow"></div>
        <div class="animated-border-box"></div>
        <div class="ufo-popup-content">
            <h4>🛸 UFO Sighting 🛸</h4>
            <div class="info-line"><b>Date:</b> {formatted_date}</div>
            <div class="info-line"><b>City:</b> {city}</div>
            <div class="info-line"><b>Shape:</b> {shape}</div>
            <div class="info-line"><b>Encounter:</b> {encounter}</div>
        </div>
    </div>
    """