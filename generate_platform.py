import folium
from folium.plugins import HeatMap
import random
from datetime import datetime
import os
import webbrowser

def build_github_style_urban_platform():
    print("[Platform Engine] Generating GitHub-style Urban Intelligence Webpage with Satellite View...")
    
    map_center = [28.6139, 77.2090]
    city_map = folium.Map(location=map_center, zoom_start=13, tiles=None)

    folium.TileLayer('CartoDB positron', name='Clean Map (Default)').add_to(city_map)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
        name='Satellite View (Esri World Imagery)'
    ).add_to(city_map)
    folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(city_map)

    bus_ids = ["BUS-DL-04-1234", "BUS-DL-01-9876", "BUS-DL-08-4321"]
    event_types = ["pothole", "missing_zebra_crossing", "damaged_signboard", "waterlogging", "rash_driving", "traffic_update"]
    color_mapping = {
        "pothole": "red",
        "missing_zebra_crossing": "orange",
        "damaged_signboard": "purple",
        "waterlogging": "blue",
        "rash_driving": "darkred",
        "traffic_update": "green"
    }

    heat_data = []
    random.seed(42)
    for _ in range(15):
        lat = 28.6139 + random.uniform(-0.025, 0.025)
        lon = 77.2090 + random.uniform(-0.025, 0.025)
        event = random.choice(event_types)
        bus = random.choice(bus_ids)
        conf = round(random.uniform(0.85, 0.99), 2)
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        heat_data.append([lat, lon])

        popup_html = (
            f"<div style='font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Helvetica, Arial, sans-serif; font-size: 13px; width: 220px; color: #24292e;'>"
            f"<b style='color: #0366d6;'>Event:</b> {event.replace('_', ' ').title()}<br>"
            f"<b>Bus ID:</b> {bus}<br>"
            f"<b>AI Confidence:</b> {conf * 100}%<br>"
            f"<b>Timestamp:</b> {time_str}"
            f"</div>"
        )
        
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color=color_mapping.get(event, "gray"), icon="info-sign")
        ).add_to(city_map)

    HeatMap(heat_data, radius=15, blur=10, max_zoom=1, name="Congestion/Hazard Heatmap").add_to(city_map)
    folium.LayerControl().add_to(city_map)

    map_html_string = city_map._repr_html_()

    github_page_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Powered Mobile Urban Intelligence Platform</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #0d1117;
            color: #c9d1d9;
        }}
        header {{
            background-color: #161b22;
            border-bottom: 1px solid #30363d;
            padding: 16px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .repo-title {{
            font-size: 20px;
            font-weight: 600;
            color: #58a6ff;
            text-decoration: none;
        }}
        .repo-title span {{
            color: #8b949e;
            font-weight: 300;
        }}
        .badge {{
            background-color: #238636;
            color: #ffffff;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }}
        .container {{
            max-width: 1280px;
            margin: 24px auto;
            padding: 0 16px;
        }}
        .nav-tabs {{
            display: flex;
            border-bottom: 1px solid #30363d;
            margin-bottom: 24px;
            gap: 16px;
        }}
        .tab {{
            padding: 8px 16px;
            color: #c9d1d9;
            border-bottom: 2px solid #f78166;
            font-weight: 600;
            cursor: pointer;
        }}
        .tab-inactive {{
            border-bottom: 2px solid transparent;
            color: #8b949e;
        }}
        .markdown-body {{
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 32px;
            margin-bottom: 32px;
        }}
        .markdown-body h1, .markdown-body h2 {{
            border-bottom: 1px solid #21262d;
            padding-bottom: .3em;
            color: #f0f6fc;
        }}
        .file-explorer {{
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            margin-bottom: 24px;
        }}
        .file-row {{
            padding: 8px 16px;
            border-bottom: 1px solid #21262d;
            display: flex;
            align-items: center;
            font-size: 14px;
        }}
        .file-row:last-child {{ border-bottom: none; }}
        .file-row span {{ margin-left: 8px; color: #58a6ff; }}
        .map-wrapper {{
            border: 1px solid #30363d;
            border-radius: 6px;
            overflow: hidden;
            background: #ffffff;
        }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 6px; }}
    </style>
</head>
<body>

    <header>
        <div>
            <a href="#" class="repo-title">municipal-ai <span>/</span> <strong>urban-intelligence-platform</strong></a>
        </div>
        <div>
            <span class="badge">Public PoC v1.0</span>
        </div>
    </header>

    <div class="container">
        <div class="nav-tabs">
            <div class="tab">Code & Live Dashboard</div>
            <div class="tab tab-inactive">Issues (3)</div>
            <div class="tab tab-inactive">Pull Requests</div>
            <div class="tab tab-inactive">Actions</div>
        </div>

        <div class="file-explorer">
            <div class="file-row" style="background: #21262d; font-weight: 600; color: #f0f6fc;">
                📁 Latest commit <span>main @ 2026 release</span>
            </div>
            <div class="file-row">📦 <span>edge_node.py</span> — Onboard YOLOv10 edge filtering module</div>
            <div class="file-row">🗺️ <span>urban_intelligence_map.html</span> — Interactive GIS & Satellite Command view</div>
            <div class="file-row">📄 <span>README.md</span> — System architecture specifications</div>
        </div>

        <div class="markdown-body" style="padding: 16px;">
            <h2 style="margin-top: 0; border: none;">🛰️ Live Fleet Command & Satellite GIS View</h2>
            <p style="color: #8b949e; font-size: 14px;">Toggle map layers on the top right of the map below to switch between standard map mode and <b>High-Resolution Satellite View</b>.</p>
            <div class="map-wrapper">
                {map_html_string}
            </div>
        </div>

        <div class="markdown-body">
            <h1>AI-Powered Mobile Urban Intelligence Platform</h1>
            <p>Transforms standard public transport municipal bus fleets into mobile IoT and edge-computing sensor networks, replacing expensive stationary roadside cameras.</p>
            
            <h2>Architecture Highlights</h2>
            <ul>
                <li><strong>Edge AI Vision Pods:</strong> Filters 99% of raw video data onboard using optimized model weights, broadcasting only lightweight JSON payloads via cellular networks.</li>
                <li><strong>Multi-Layer GIS Command Map:</strong> Aggregates live road defects (potholes, waterlogging, missing signs) and tracks traffic density heatmaps.</li>
                <li><strong>Satellite Intelligence Integration:</strong> Supports precise geospatial overlays against high-definition satellite imagery for urban planners.</li>
            </ul>
        </div>
    </div>

</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(github_page_content)
        
    print("[Success] GitHub-style platform web page generated successfully as 'index.html'!")

if __name__ == "__main__":
    build_github_style_urban_platform()
    webbrowser.open("file://" + os.path.realpath("index.html"))
