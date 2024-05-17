import mysql.connector
import paho.mqtt.client as mqtt
import pygame

# MQTT Settings
MQTT_BROKER = "192.168.0.87"
MQTT_PORT = 1883
MQTT_TOPIC = "ultrasonic/distance"

# MariaDB Settings
DB_HOST = "localhost"
DB_USER = "new_user"
DB_PASSWORD = "user_password"
DB_NAME = "mydatabase"
TABLE_NAME = "distance_log"

# Initialize pygame mixer for playing sound
pygame.mixer.init()

# Load the sound file (make sure the file is in the same directory or provide the correct path)
sound_file = "pianoC.wav"  # Replace with the path to your sound file
pygame.mixer.music.load(sound_file)

# Callback function to handle MQTT messages
def on_message(client, userdata, message):
    # Convert the received message payload (distance) to float
    distance = float(message.payload.decode())

    try:
        # Connect to the MariaDB database
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        # Check if the connection was successful
        if conn.is_connected():
            print("Connected to MariaDB")

            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()

            # Insert the received distance into the table
            sql = "INSERT INTO {} (distance) VALUES (%s)".format(TABLE_NAME)
            cursor.execute(sql, (distance,))

            # Commit the transaction
            conn.commit()

            print("Distance logged successfully:", distance)

            # Play the sound when the distance is logged
            pygame.mixer.music.play()

        # Close the connection
        conn.close()

    except mysql.connector.Error as err:
        print("Error:", err)

# Create MQTT client instance
client = mqtt.Client()
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT)

# Subscribe to the MQTT topic
client.subscribe(MQTT_TOPIC)

# Start the MQTT loop to handle incoming messages
client.loop_forever()
