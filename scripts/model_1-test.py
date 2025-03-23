import asyncio
import websockets
import numpy as np
import joblib
import pygame
from pydub import AudioSegment
from pydub.generators import Sine
import threading
import os
import tempfile
from tensorflow.keras.models import load_model

# Load the saved model and scaler
model = load_model('D:\\WiSee\\models\\rssi_human_detection_model_s.h5')
scaler = joblib.load('D:\\WiSee\\models\\scaler_s.save')

# Function to generate a sine wave and save it as a temporary file
def generate_sine_wave(frequency=440, duration=1000, volume=-20):
    sine_wave = Sine(frequency).to_audio_segment(duration=duration).apply_gain(volume)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sine_wave.export(temp_file.name, format="wav")
    return temp_file.name

# Define the WebSocket connection parameters
ESP32_IP = "192.168.4.1"
WEBSOCKET_URL = f"ws://{ESP32_IP}:81"

# Initialize pygame for sound playback and display
pygame.init()

# Generate sounds and store their file paths
sound_files = {
    'Empty Room': generate_sine_wave(frequency=220, duration=500),
    'Stationary Person': generate_sine_wave(frequency=440, duration=1000),
    'Moving Person': generate_sine_wave(frequency=880, duration=1500)
}

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("WiSee Human Detection")

# Load fonts
font = pygame.font.Font(None, 74)  # Large font for status
small_font = pygame.font.Font(None, 48)  # Smaller font for accuracy

# Function to make predictions
def predict_human_status(new_rssi_values, model, scaler):
    new_rssi_scaled = scaler.transform(new_rssi_values)
    new_rssi_scaled = new_rssi_scaled.reshape(new_rssi_scaled.shape[0], new_rssi_scaled.shape[1], 1)
    predicted_proba = model.predict(new_rssi_scaled)
    predicted_classes = np.argmax(predicted_proba, axis=1)
    status_map = {0: 'Empty Room', 1: 'Stationary Person', 2: 'Moving Person'}
    predicted_labels = [status_map[cls] for cls in predicted_classes]
    return predicted_classes, predicted_labels, predicted_proba

# Function to update the Pygame display
def update_display(predicted_labels, predictions):
    screen.fill(WHITE)  # Clear the screen

    # Display the status
    status_text = f"Status: {predicted_labels[0]}"
    status_surface = font.render(status_text, True, BLACK)
    screen.blit(status_surface, (50, 50))

    # Display the accuracy
    accuracy_text = f"Accuracy: {np.max(predictions) * 100:.2f}%"
    accuracy_surface = small_font.render(accuracy_text, True, BLACK)
    screen.blit(accuracy_surface, (50, 150))

    # Draw a colored rectangle based on the status
    if predicted_labels[0] == 'Empty Room':
        pygame.draw.rect(screen, GREEN, (50, 250, 700, 200))  # Green for empty room
    elif predicted_labels[0] == 'Stationary Person':
        pygame.draw.rect(screen, BLUE, (50, 250, 700, 200))  # Blue for stationary person
    elif predicted_labels[0] == 'Moving Person':
        pygame.draw.rect(screen, RED, (50, 250, 700, 200))  # Red for moving person

    # Update the display
    pygame.display.flip()

    # Play the corresponding sound
    sound_file = sound_files.get(predicted_labels[0])
    if sound_file:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

async def receive_data():
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("Connected to ESP32 WebSocket!")
            receiver_data = {"Receiver_1": None, "Receiver_2": None, "Receiver_3": None}
            while True:
                data = await websocket.recv()
                print(f"Data from ESP32: {data}")
                parts = data.split(',')
                if len(parts) == 3:
                    receiver, rssi, value = parts
                    rssi = int(float(rssi))
                    if receiver == "Receiver_1":
                        receiver_data["Receiver_1"] = rssi
                    elif receiver == "Receiver_2":
                        receiver_data["Receiver_2"] = rssi
                    elif receiver == "Receiver_3":
                        receiver_data["Receiver_3"] = rssi
                    print("Most recent RSSI values:", receiver_data)
                    if all(value is not None for value in receiver_data.values()):
                        # Create the array with original 3 RSSI values
                        rssi_values = np.array([[
                            receiver_data["Receiver_1"], 
                            receiver_data["Receiver_2"], 
                            receiver_data["Receiver_3"]
                        ]])
                        
                        predicted_classes, predicted_labels, predictions = predict_human_status(rssi_values, model, scaler)
                        print("Predicted Classes:", predicted_classes)
                        print("Predicted Labels:", predicted_labels)
                        print("Prediction Probabilities:\n", predictions)
                        update_display(predicted_labels, predictions)
    except Exception as e:
        print(f"Connection error: {e}")

# Function to run the asyncio event loop in a separate thread
def start_asyncio_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(receive_data())

# Start the asyncio event loop in a separate thread
threading.Thread(target=start_asyncio_loop, daemon=True).start()

# Pygame main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

# Clean up temporary sound files after the program exits
for sound_file in sound_files.values():
    try:
        os.remove(sound_file)
    except Exception as e:
        print(f"Error deleting temporary file {sound_file}: {e}")

pygame.quit()