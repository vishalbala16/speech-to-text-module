#!/usr/bin/env python3
"""
Mobile Bridge for React Native Integration
"""

import asyncio
import websockets
import json
from speech_module import SpeechToTextModule

class MobileBridge:
    def __init__(self):
        self.stt = SpeechToTextModule()
        self.stt.set_transcription_callback(self.handle_transcription)
        self.clients = set()
        
    def handle_transcription(self, text):
        """Send transcription to all connected mobile clients"""
        if self.clients:
            # Include wake/sleep status
            status = self.stt.get_status()
            message = json.dumps({
                "type": "transcription", 
                "text": text,
                "status": status
            })
            asyncio.create_task(self.broadcast(message))
    
    async def broadcast(self, message):
        """Broadcast to all clients"""
        if self.clients:
            await asyncio.gather(*[client.send(message) for client in self.clients], return_exceptions=True)
    
    async def handle_client(self, websocket, path):
        """Handle mobile app connections"""
        self.clients.add(websocket)
        print(f"Mobile client connected. Total: {len(self.clients)}")
        
        try:
            async for message in websocket:
                data = json.loads(message)
                
                if data.get("action") == "start":
                    self.stt.start_listening()
                    await websocket.send(json.dumps({"status": "listening"}))
                    
                elif data.get("action") == "stop":
                    self.stt.stop_listening()
                    await websocket.send(json.dumps({"status": "stopped"}))
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            print(f"Mobile client disconnected. Total: {len(self.clients)}")
    
    def start_server(self, port=8765):
        """Start WebSocket server for React Native"""
        print(f"Mobile bridge server starting on port {port}")
        print("React Native can connect to: ws://localhost:8765")
        
        start_server = websockets.serve(self.handle_client, "localhost", port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    bridge = MobileBridge()
    bridge.start_server()