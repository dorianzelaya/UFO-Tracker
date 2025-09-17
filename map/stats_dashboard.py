import folium
from folium import plugins
import pandas as pd
from collections import Counter
import json

class UFOStatsDashboard:
    def __init__(self, map_data, style_config):
        self.map_data = map_data
        self.style_config = style_config
        self.stats = self._calculate_stats()
    
    def _calculate_stats(self):
        """Calculate all statistics for the dashboard"""
        # Convert map_data to DataFrame for easier analysis
        df = pd.DataFrame(self.map_data)
        
        # Basic counts
        total_sightings = len(df)
        unique_cities = df['city'].nunique()
        unique_shapes = df['shape'].nunique()
        
        # Shape analysis
        shape_counts = df['shape'].value_counts().head(5)
        most_common_shape = shape_counts.index[0] if len(shape_counts) > 0 else "Unknown"
        
        # City analysis
        city_counts = df['city'].value_counts().head(5)
        
        # Year analysis (handle empty years)
        df_years = df[df['year'] != ''].copy()
        if not df_years.empty:
            df_years['year'] = pd.to_numeric(df_years['year'], errors='coerce')
            df_years = df_years.dropna(subset=['year'])
            
            if not df_years.empty:
                year_counts = df_years['year'].value_counts().head(5)
                peak_year = int(year_counts.index[0]) if len(year_counts) > 0 else "Unknown"
                earliest_year = int(df_years['year'].min())
                latest_year = int(df_years['year'].max())
            else:
                year_counts = pd.Series()
                peak_year = "Unknown"
                earliest_year = "Unknown"
                latest_year = "Unknown"
        else:
            year_counts = pd.Series()
            peak_year = "Unknown"
            earliest_year = "Unknown"
            latest_year = "Unknown"
        
        # Month analysis
        df_months = df[df['month'] != ''].copy()
        month_names = {
            '1': 'January', '2': 'February', '3': 'March', '4': 'April',
            '5': 'May', '6': 'June', '7': 'July', '8': 'August',
            '9': 'September', '10': 'October', '11': 'November', '12': 'December'
        }
        
        if not df_months.empty:
            month_counts = df_months['month'].value_counts()
            peak_month = month_names.get(month_counts.index[0], "Unknown") if len(month_counts) > 0 else "Unknown"
        else:
            peak_month = "Unknown"
        
        return {
            'total_sightings': total_sightings,
            'unique_cities': unique_cities,
            'unique_shapes': unique_shapes,
            'most_common_shape': most_common_shape,
            'peak_year': peak_year,
            'peak_month': peak_month,
            'earliest_year': earliest_year,
            'latest_year': latest_year,
            'shape_counts': shape_counts.to_dict(),
            'city_counts': city_counts.to_dict(),
            'year_counts': year_counts.to_dict() if not year_counts.empty else {}
        }
    
    def get_dashboard_css(self):
        """Get CSS for the statistics dashboard"""
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;500;600&display=swap');
        
        .stats-dashboard {
            position: fixed;
            top: 20px;
            right: 20px;
            width: 320px;
            background: rgba(20, 25, 35, 0.95);
            border: 2px solid #00ff99;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            z-index: 1000;
            font-family: 'Poppins', sans-serif;
            box-shadow: 0 0 30px rgba(0, 255, 153, 0.3);
            max-height: 80vh;
            overflow-y: auto;
            transition: transform 0.3s ease;
        }
        
        .stats-dashboard.collapsed .stats-content {
            display: none;
        }
        
        .stats-dashboard.collapsed {
            width: auto;
            min-width: 180px;
        }
        
        .stats-header {
            background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
            padding: 15px 20px;
            border-bottom: 1px solid #00ff99;
            border-radius: 13px 13px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1001;
            gap: 15px;
        }
        
        .stats-title {
            font-family: 'Orbitron', monospace;
            font-size: 18px;
            font-weight: 700;
            color: #00ff99;
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .toggle-btn {
            background: none;
            border: 1px solid #00ff99;
            color: #00ff99;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s ease;
        }
        
        .toggle-btn:hover {
            background: #00ff99;
            color: #1a1f2e;
            box-shadow: 0 0 15px rgba(0, 255, 153, 0.5);
        }
        
        .stats-content {
            padding: 20px;
        }
        
        .stat-section {
            margin-bottom: 25px;
        }
        
        .section-title {
            font-family: 'Orbitron', monospace;
            font-size: 14px;
            font-weight: 700;
            color: #00ccff;
            text-transform: uppercase;
            margin-bottom: 12px;
            letter-spacing: 0.5px;
            border-bottom: 1px solid rgba(0, 204, 255, 0.3);
            padding-bottom: 5px;
        }
        
        .key-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, rgba(0, 255, 153, 0.1) 0%, rgba(0, 204, 255, 0.1) 100%);
            border: 1px solid rgba(0, 255, 153, 0.3);
            border-radius: 8px;
            padding: 12px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            border-color: #00ff99;
            box-shadow: 0 0 15px rgba(0, 255, 153, 0.2);
            transform: translateY(-2px);
        }
        
        .stat-number {
            font-family: 'Orbitron', monospace;
            font-size: 24px;
            font-weight: 900;
            color: #00ff99;
            display: block;
            line-height: 1;
        }
        
        .stat-label {
            font-size: 11px;
            color: #a2a5b3;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }
        
        .top-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .top-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid rgba(162, 165, 179, 0.2);
            color: #f0f0f0;
            font-size: 13px;
        }
        
        .top-item:last-child {
            border-bottom: none;
        }
        
        .item-name {
            flex: 1;
            text-transform: capitalize;
        }
        
        .item-count {
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            color: #00ccff;
            margin-left: 10px;
        }
        
        .progress-bar {
            width: 40px;
            height: 4px;
            background: rgba(0, 204, 255, 0.3);
            border-radius: 2px;
            margin-left: 10px;
            position: relative;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00ccff 0%, #00ff99 100%);
            border-radius: 2px;
            transition: width 0.5s ease;
        }
        
        .highlight-stat {
            background: rgba(0, 255, 153, 0.15);
            border: 1px solid rgba(0, 255, 153, 0.4);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .highlight-value {
            font-family: 'Orbitron', monospace;
            font-size: 20px;
            font-weight: 700;
            color: #00ff99;
            display: block;
        }
        
        .highlight-label {
            font-size: 12px;
            color: #a2a5b3;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }
        
        /* Scrollbar styling */
        .stats-dashboard::-webkit-scrollbar {
            width: 6px;
        }
        
        .stats-dashboard::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 3px;
        }
        
        .stats-dashboard::-webkit-scrollbar-thumb {
            background: rgba(0, 255, 153, 0.5);
            border-radius: 3px;
        }
        
        .stats-dashboard::-webkit-scrollbar-thumb:hover {
            background: rgba(0, 255, 153, 0.7);
        }
        
        @media (max-width: 768px) {
            .stats-dashboard {
                width: 280px;
                top: 10px;
                right: 10px;
            }
            
            .key-stats {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """
    
    def get_dashboard_js(self):
        """Get JavaScript for dashboard interactivity"""
        return """
        <script>
        function toggleStatsPanel() {
            const dashboard = document.querySelector('.stats-dashboard');
            const btn = document.querySelector('.toggle-btn');
            
            dashboard.classList.toggle('collapsed');
            
            if (dashboard.classList.contains('collapsed')) {
                btn.textContent = '◀';
                btn.title = 'Show Statistics';
            } else {
                btn.textContent = '✕';
                btn.title = 'Hide Statistics';
            }
        }
        
        // Initialize progress bars
        function initProgressBars() {
            const progressBars = document.querySelectorAll('.progress-fill');
            progressBars.forEach(bar => {
                const width = bar.dataset.width;
                setTimeout(() => {
                    bar.style.width = width + '%';
                }, 100);
            });
        }
        
        // Auto-initialize when DOM is ready
        document.addEventListener('DOMContentLoaded', function() {
            initProgressBars();
        });
        
        // Initialize after a delay to ensure folium map is ready
        setTimeout(initProgressBars, 1000);
        </script>
        """
    
    def create_dashboard_html(self):
        """Create the complete dashboard HTML"""
        stats = self.stats
        
        # Calculate percentages for progress bars
        max_shape_count = max(stats['shape_counts'].values()) if stats['shape_counts'] else 1
        max_city_count = max(stats['city_counts'].values()) if stats['city_counts'] else 1
        
        # Build top shapes list
        shapes_html = ""
        for i, (shape, count) in enumerate(list(stats['shape_counts'].items())[:5]):
            percentage = (count / max_shape_count) * 100
            shapes_html += f"""
            <li class="top-item">
                <span class="item-name">{shape}</span>
                <span class="item-count">{count}</span>
                <div class="progress-bar">
                    <div class="progress-fill" data-width="{percentage}"></div>
                </div>
            </li>
            """
        
        # Build top cities list
        cities_html = ""
        for i, (city, count) in enumerate(list(stats['city_counts'].items())[:5]):
            percentage = (count / max_city_count) * 100
            cities_html += f"""
            <li class="top-item">
                <span class="item-name">{city}</span>
                <span class="item-count">{count}</span>
                <div class="progress-bar">
                    <div class="progress-fill" data-width="{percentage}"></div>
                </div>
            </li>
            """
        
        # Year range display
        year_range = f"{stats['earliest_year']} - {stats['latest_year']}" if stats['earliest_year'] != "Unknown" else "Unknown"
        
        html = f"""
        <div class="stats-dashboard" id="ufoStatsDashboard">
            <div class="stats-header">
                <h3 class="stats-title">🛸 UFO Intel</h3>
                <button class="toggle-btn" onclick="toggleStatsPanel()" title="Hide Statistics">✕</button>
            </div>
            <div class="stats-content">
                
                <!-- Key Statistics -->
                <div class="stat-section">
                    <div class="key-stats">
                        <div class="stat-card">
                            <span class="stat-number">{stats['total_sightings']:,}</span>
                            <div class="stat-label">Total Sightings</div>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">{stats['unique_cities']}</span>
                            <div class="stat-label">Cities</div>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">{stats['unique_shapes']}</span>
                            <div class="stat-label">Shape Types</div>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">{year_range}</span>
                            <div class="stat-label">Year Range</div>
                        </div>
                    </div>
                </div>
                
                <!-- Peak Activity -->
                <div class="stat-section">
                    <h4 class="section-title">🔥 Peak Activity</h4>
                    <div class="highlight-stat">
                        <span class="highlight-value">{stats['peak_year']}</span>
                        <div class="highlight-label">Most Active Year</div>
                    </div>
                    <div class="highlight-stat">
                        <span class="highlight-value">{stats['peak_month']}</span>
                        <div class="highlight-label">Most Active Month</div>
                    </div>
                </div>
                
                <!-- Top UFO Shapes -->
                <div class="stat-section">
                    <h4 class="section-title">👁️ Common Shapes</h4>
                    <ul class="top-list">
                        {shapes_html}
                    </ul>
                </div>
                
                <!-- Top Cities -->
                <div class="stat-section">
                    <h4 class="section-title">🏙️ Hotspot Cities</h4>
                    <ul class="top-list">
                        {cities_html}
                    </ul>
                </div>
                
            </div>
        </div>
        """
        
        return html
    
    def add_to_map(self, folium_map):
        """Add the statistics dashboard to the folium map"""
        # Add CSS
        css = self.get_dashboard_css()
        folium_map.get_root().html.add_child(folium.Element(css))
        
        # Add JavaScript
        js = self.get_dashboard_js()
        folium_map.get_root().html.add_child(folium.Element(js))
        
        # Add HTML
        html = self.create_dashboard_html()
        folium_map.get_root().html.add_child(folium.Element(html))
        
        return folium_map