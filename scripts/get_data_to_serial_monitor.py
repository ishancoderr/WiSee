import asyncio
import websockets

ESP32_IP = "192.168.4.1"
WEBSOCKET_URL = f"ws://{ESP32_IP}:81"

async def receive_data():
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("Connected to ESP32 WebSocket!")
            while True:
                data = await websocket.recv()  # Receive data from ESP32
                print(f"Data from ESP32: {data}")  # Print the received data

    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(receive_data())


