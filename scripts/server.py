#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import logging
import sys
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("MQTT_Client")

# MQTT Configuration
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_TOPIC = "wifi/data"
RECONNECT_DELAY = 5

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback for when client connects to the broker"""
    if rc == 0:
        logger.info("✅ Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC, qos=1)
        logger.info(f"✅ Subscribed to {MQTT_TOPIC}")
    else:
        logger.error(f"❌ Failed to connect, return code {rc}")

def on_message(client, userdata, message):
    """Callback for when a message is received from the broker"""
    try:
        payload = message.payload.decode('utf-8')
        logger.info(f"📩 Received message on {message.topic}: {payload}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

def on_disconnect(client, userdata, rc):
    """Callback for when client disconnects from the broker"""
    if rc != 0:
        logger.warning(f"🔌 Unexpected disconnection, return code {rc}")
        logger.info(f"Reconnecting in {RECONNECT_DELAY} seconds...")
        time.sleep(RECONNECT_DELAY)
        client.reconnect()
    else:
        logger.info("🔌 Disconnected from broker")

def create_mqtt_client():
    """Create and configure MQTT client"""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, clean_session=True)
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    # Set Last Will and Testament (LWT)
    client.will_set(MQTT_TOPIC, payload="Client disconnected unexpectedly", qos=1, retain=True)
    
    # You can uncomment and set these if authentication is required
    # client.username_pw_set("username", "password")
    
    # You can uncomment and configure TLS if needed
    # client.tls_set(ca_certs="path/to/ca.crt")
    
    return client

def main():
    """Main function to run the MQTT client"""
    client = create_mqtt_client()
    
    connected = False
    while not connected:
        try:
            logger.info(f"🔄 Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
            client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
            connected = True
        except Exception as e:
            logger.error(f"⚠️ Connection Error: {e}")
            logger.info(f"Retrying in {RECONNECT_DELAY} seconds...")
            time.sleep(RECONNECT_DELAY)
    
    try:
        # Run the network loop
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Disconnecting...")
        client.disconnect()
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
    finally:
        logger.info("Exiting program")

if __name__ == "__main__":
    main()