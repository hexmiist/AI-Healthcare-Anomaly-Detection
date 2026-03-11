import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

patients = ["P001", "P002", "P003"]
print("🚀 Producer started. Sending vitals to Kafka...")

try:
    while True:
        for p_id in patients:
            # Generate Vitals
            hr = random.randint(60, 160)
            spo2 = round(random.uniform(80, 99), 2)
            temp = round(random.uniform(36.5, 40.0), 1)
            # Generating a random Blood Pressure for the report
            bp = f"{random.randint(110, 190)}/{random.randint(70, 110)}"
            
            data = {
                "patient_id": p_id,
                "heart_rate": hr,
                "oxygen_sat": spo2,
                "temperature": temp,
                "blood_pressure": bp,
                "timestamp": time.time()
            }
            
            producer.send('medical-vitals', value=data)
            print(f"📡 Sent to Kafka -> {p_id} | HR: {hr} | SpO2: {spo2}%")
            
        time.sleep(2)
except KeyboardInterrupt:
    print("Stopping Producer...")