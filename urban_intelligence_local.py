import time
import random
from datetime import datetime
from collections import defaultdict

class CentralCommandServer:
    """Simulates the centralized cloud server and PostGIS database."""
    def __init__(self):
        self.incident_database = []
        self.traffic_density_logs = defaultdict(list)

    def ingest_telemetry(self, payload):
        """Receives and stores lightweight JSON telemetry from the bus edge node."""
        self.incident_database.append(payload)
        
        event_type = payload["event_type"]
        bus_id = payload["bus_id"]
        
        if event_type in ["pothole", "missing_zebra_crossing", "damaged_signboard", "waterlogging"]:
            print(f"  [Cloud DB] 🔴 MUNICIPAL ALERT: '{event_type.upper()}' logged from {bus_id} at Lat: {payload['location']['latitude']:.4f}, Lon: {payload['location']['longitude']:.4f}")
        elif event_type == "rash_driving":
            plate = payload["metadata"].get("offending_plate", "UNKNOWN")
            print(f"  [Cloud DB] 🚨 SAFETY INCIDENT: Rash driving detected! Offender Plate: {plate} logged.")
        elif event_type == "traffic_update":
            count = payload["metadata"].get("vehicle_count", 0)
            print(f"  [Cloud DB] 📊 TRAFFIC METRIC: Route density updated ({count} vehicles counted nearby).")

    def generate_gis_summary(self):
        """Summarizes data for the central GIS command dashboard."""
        print("\n" + "="*50)
        print("🌍 CENTRAL COMMAND GIS & ANALYTICS DASHBOARD SUMMARY")
        print("="*50)
        print(f"Total Telemetry Packets Received: {len(self.incident_database)}")
        
        # Categorize incidents
        summary_counts = defaultdict(int)
        for record in self.incident_database:
            summary_counts[record["event_type"]] += 1
            
        print("\n[Infrastructure & Safety Breakdown]:")
        for event, count in summary_counts.items():
            print(f" - {event.replace('_', ' ').title()}: {count} report(s)")
        print("="*50 + "\n")


def simulate_bus_edge_node(server):
    """Simulates the bus onboard edge AI processing video feeds and filtering data."""
    print("[Edge Node] Initializing onboard multi-camera AI vision system...")
    print("[Edge Node] Loading optimized YOLOv10 weights onto edge hardware...\n")
    
    bus_id = "BUS-DL-04-1234"
    route_no = "Route 522 (Connaught Place - Nehru Place)"
    
    defect_types = [
        "pothole", 
        "missing_zebra_crossing", 
        "damaged_signboard", 
        "waterlogging", 
        "rash_driving",
        "traffic_update"
    ]
    
    # Simulate 5 cycles of frame capture and analysis
    for cycle in range(1, 6):
        print(f"\n--- [Edge Node] Processing Camera Frames Cycle {cycle} ---")
        time.sleep(1.5) # Simulate time elapsed between frames
        
        detected_event = random.choice(defect_types)
        confidence = round(random.uniform(0.85, 0.99), 2)
        
        # Simulated GPS coordinates around Delhi
        lat = 28.6139 + random.uniform(-0.01, 0.01)
        lon = 77.2090 + random.uniform(-0.01, 0.01)
        
        payload = {
            "bus_id": bus_id,
            "route": route_no,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": detected_event,
            "confidence": confidence,
            "location": {
                "latitude": round(lat, 6),
                "longitude": round(lon, 6)
            },
            "metadata": {
                "vehicle_count": random.randint(10, 55) if detected_event == "traffic_update" else None,
                "offending_plate": "DL-3C-9988" if detected_event == "rash_driving" else None
            }
        }
        
        print(f"[Edge Node] Analyzed frame. Detected: {detected_event} (Confidence: {confidence})")
        print(f"[Edge Node] Bandwidth saved: Discarding 50MB raw video frame. Transmitting 0.5KB JSON payload...")
        
        # Directly send payload to local central command instance (no network/API required)
        server.ingest_telemetry(payload)


if __name__ == "__main__":
    # Initialize the local central command database
    central_server = CentralCommandServer()
    
    # Run the onboard edge node simulation
    simulate_bus_edge_node(central_server)
    
    # Display the final command dashboard analytics
    central_server.generate_gis_summary()
