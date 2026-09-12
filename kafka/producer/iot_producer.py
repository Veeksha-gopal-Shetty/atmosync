import csv
import json
import time
from kafka import KafkaProducer

KAFKA_SERVER = "localhost:9092"
TOPIC = "iot-sensor-readings"

CSV_FILE = r"Data\Data cleaning\sensor_readings_cleaned.xls"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

print("AtmoSync IoT Kafka Producer started")
print(f"Topic: {TOPIC}")
print("Streaming IoT sensor readings...\n")

with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    count = 0

    for row in reader:
        producer.send(TOPIC, value=row)
        count += 1

        if count % 100 == 0:
            print(f"Sent {count} IoT records")

        time.sleep(0.1)

producer.flush()
producer.close()

print(f"\nStreaming completed. Total records sent: {count}")