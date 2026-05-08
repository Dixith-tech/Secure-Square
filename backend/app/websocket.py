from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import random
import logging
import json
from typing import List, Set
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.client_data: dict = {}
    
    async def connect(self, websocket: WebSocket, client_id: str = None):
        """Accept and register a new connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        if client_id:
            self.client_data[client_id] = websocket
        logger.info(f"✓ WebSocket client connected. Total connections: {len(self.active_connections)}")
    
    async def disconnect(self, websocket: WebSocket, client_id: str = None):
        """Unregister and close a connection"""
        self.active_connections.discard(websocket)
        if client_id and client_id in self.client_data:
            del self.client_data[client_id]
        logger.info(f"✓ WebSocket client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, data: dict):
        """Send data to all connected clients"""
        if not self.active_connections:
            return
        
        disconnected = set()
        
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                logger.error(f"✗ WebSocket broadcast failed: {str(e)}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            await self.disconnect(conn)
    
    async def send_personal(self, websocket: WebSocket, data: dict):
        """Send data to specific client"""
        try:
            await websocket.send_json(data)
        except Exception as e:
            logger.error(f"✗ WebSocket personal send failed: {str(e)}")
            await self.disconnect(websocket)

# Global connection manager
manager = ConnectionManager()

async def manage_connections():
    """Manage all connections"""
    return manager

async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint for threat updates"""
    client_id = f"client_{random.randint(10000, 99999)}"
    
    try:
        await manager.connect(websocket, client_id)
        
        # Send welcome message
        await manager.send_personal(websocket, {
            "type": "connection",
            "status": "connected",
            "client_id": client_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Generate and broadcast fake threat data (for demo)
        # In production, this would receive data from detection engines
        counter = 0
        while True:
            try:
                # Check for client messages (optional)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30)
                
                # Echo back with timestamp
                await manager.send_personal(websocket, {
                    "type": "echo",
                    "message": data,
                    "timestamp": datetime.utcnow().isoformat()
                })
                
            except asyncio.TimeoutError:
                # Generate threat data periodically
                threat_data = generate_threat_data(counter)
                
                # Broadcast to all clients
                await manager.broadcast({
                    "type": "threat",
                    "data": threat_data,
                    "timestamp": datetime.utcnow().isoformat()
                })
                
                counter += 1
                
                # Wait before next update
                await asyncio.sleep(2)
                
    except WebSocketDisconnect:
        await manager.disconnect(websocket, client_id)
        logger.info(f"Client {client_id} disconnected normally")
        
    except Exception as e:
        logger.error(f"✗ WebSocket error for {client_id}: {str(e)}")
        await manager.disconnect(websocket, client_id)
        raise

def generate_threat_data(counter: int = 0) -> dict:
    """Generate sample threat data for demo"""
    threat_types = ["Phishing", "Spoofing", "Port Scan", "Brute Force", "DDoS", "Intrusion"]
    severities = ["Low", "Medium", "High", "Critical"]
    countries = ["United States", "China", "Russia", "India", "Brazil", "Germany"]
    
    return {
        "id": counter,
        "ip_address": f"192.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
        "threat_type": random.choice(threat_types),
        "severity": random.choice(severities),
        "confidence": round(random.uniform(0.6, 0.99), 2),
        "country": random.choice(countries),
        "latitude": round(random.uniform(-90, 90), 2),
        "longitude": round(random.uniform(-180, 180), 2),
        "risk_score": round(random.uniform(20, 95), 1),
        "anomaly_score": round(random.uniform(0.1, 0.9), 2)
    }

# Connection context functions
async def get_connection_manager():
    """Dependency for getting connection manager"""
    return manager
