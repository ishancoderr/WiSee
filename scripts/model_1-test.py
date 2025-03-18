import asyncio
import websockets
import numpy as np
from tensorflow import keras
import joblib

# Load the saved model and scaler
model = keras.models.load_model('D:\\WiSee\\models\\imodel_2.h5')
scaler = joblib.load('D:\\WiSee\\models\\scaler.joblib')

# Define the WebSocket connection parameters
ESP32_IP = "192.168.4.1"
WEBSOCKET_URL = f"ws://{ESP32_IP}:81"

async def receive_data():
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("Connected to ESP32 WebSocket!")
            
            receiver_data = {"Receiver_1": [], "Receiver_2": [], "Receiver_3": []}  # Initialize a dictionary to store data for each receiver
            
            while True:
                data = await websocket.recv()  # Receive data from ESP32
                print(f"Data from ESP32: {data}")  # Print the received data

                # Parse the received data, assuming format: "Receiver_X,-XX,value"
                parts = data.split(',')
                
                if len(parts) == 3:
                    receiver, rssi, value = parts
                    rssi = int(float(rssi))  # Convert RSSI value to integer, first cast to float and then to int
                    
                    # Store the RSSI value for each receiver in the dictionary
                    if receiver == "Receiver_1":
                        receiver_data["Receiver_1"].append(rssi)
                    elif receiver == "Receiver_2":
                        receiver_data["Receiver_2"].append(rssi)
                    elif receiver == "Receiver_3":
                        receiver_data["Receiver_3"].append(rssi)
                    
                    print(receiver_data)
                    # If we have data for all three receivers, process it and make predictions
                    if len(receiver_data["Receiver_1"]) > 0 and len(receiver_data["Receiver_2"]) > 0 and len(receiver_data["Receiver_3"]) > 0:
                        # Prepare the data for the model (only use the most recent RSSI values)
                        new_rssi_values = np.array([[receiver_data["Receiver_1"][-1], 
                                                      receiver_data["Receiver_2"][-1], 
                                                      receiver_data["Receiver_3"][-1]]])
                        
                        print(new_rssi_values)
                        # If human presence was added as a feature, add it to the new data
                        human_presence = 1  # Example: human presence is True (1)
                        new_rssi_values = np.append(new_rssi_values, [[human_presence]], axis=1)
                        print('new_rssi_values', new_rssi_values)
                        
                        # Scale the new data using the loaded scaler
                        new_rssi_scaled = scaler.transform(new_rssi_values)
                        
                        # Make predictions
                        prediction_probs = model.predict(new_rssi_scaled)
                        predicted_tile = np.argmax(prediction_probs, axis=1) + 1  # Add 1 if tile numbers start from 1

                        # Print the result without decimal places for the predicted tile
                        print(f"Predicted Tile: {predicted_tile}")
                        print(f"Prediction confidence: {int(np.max(prediction_probs) * 100)}%")

                        # Clear the receiver data after processing (optional, depending on your needs)
                        receiver_data = {"Receiver_1": [], "Receiver_2": [], "Receiver_3": []}

    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(receive_data())

