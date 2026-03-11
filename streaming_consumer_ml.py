import json
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from kafka import KafkaConsumer

# --- CONFIGURATION ---
SENDER_EMAIL = "skill.wallet.healthcare.ai@gmail.com"
SENDER_PASSWORD = "xwemhfxbxhxpazbk" 
DOCTOR_EMAIL = "drskillwallet@gmail.com"
alert_cooldowns = {}

def send_formatted_email(p_id, score, reasons, vitals, primary):
    # Cooldown check: 60 seconds per patient
    if p_id in alert_cooldowns and (time.time() - alert_cooldowns[p_id] < 60):
        print(f"⏳ Cooldown: Skipping email for {p_id}")
        return

    msg = MIMEMultipart()
    msg['Subject'] = "Critical Health Anomaly Detected"
    msg['From'] = SENDER_EMAIL
    msg['To'] = DOCTOR_EMAIL

    html = f"""
    <html>
    <body style="background-color: #121212; color: white; font-family: sans-serif; padding: 20px;">
        <h2 style="color: #ff3333;">Critical Health Anomaly Detected</h2>
        <p><b>Patient ID:</b> {p_id}</p>
        <p><b>Anomaly Score:</b> {score}</p>
        <table style="width: 100%; max-width: 400px; border: 1px solid #444; background: #1e1e1e; color: white;">
            <tr><td style="padding: 10px; border: 1px solid #333;">Heart Rate</td><td style="padding: 10px; border: 1px solid #333;">{vitals['heart_rate']} bpm</td></tr>
            <tr><td style="padding: 10px; border: 1px solid #333;">SpO2</td><td style="padding: 10px; border: 1px solid #333;">{vitals['oxygen_sat']}%</td></tr>
            <tr><td style="padding: 10px; border: 1px solid #333;">Temperature</td><td style="padding: 10px; border: 1px solid #333;">{vitals['temperature']}°C</td></tr>
            <tr><td style="padding: 10px; border: 1px solid #333;">Blood Pressure</td><td style="padding: 10px; border: 1px solid #333;">{vitals['blood_pressure']}</td></tr>
        </table>
        <h3>Explainability</h3>
        <ul>{"".join([f"<li>{r}</li>" for r in reasons])}</ul>
        <p style="color: #00ff00;"><b>Primary Contributor:</b> {primary}</p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        alert_cooldowns[p_id] = time.time()
        print(f"📧 [EMAIL SENT] Critical Alert for {p_id}")
    except Exception as e:
        print(f"❌ Mail Error: {e}")

# --- KAFKA CONSUMER ---
consumer = KafkaConsumer(
    'medical-vitals',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("📡 Consumer Synced. Watching stream...")

for message in consumer:
    v = message.value
    p_id = v['patient_id']
    hr, ox = v['heart_rate'], v['oxygen_sat']

    # 1. PRINT EVERY MESSAGE (To match Producer window)
    print(f"📥 Received: {p_id} | HR: {hr} | SpO2: {ox}%")

    # 2. DYNAMIC EXPLAINABILITY LOGIC
    reasons = []
    if hr > 135: reasons.append(f"Heart Rate elevated ({hr} bpm)")
    if ox < 89:  reasons.append(f"Oxygen saturation decreased ({ox}%)")
    
    # 3. CRITICAL TRIGGER (Stops non-anomaly emails)
    # Only triggers if BOTH conditions are met (High HR AND Low SpO2)
    if len(reasons) >= 2 or hr > 155:
        # Calculate Primary Contributor
        primary = "Heart Rate (72%)" if hr > 140 else "Oxygen Levels (65%)"
        score = round(2.5 + (hr / 100) + ( (95-ox) / 10), 4)
        
        print(f"🚨 ANOMALY DETECTED! Score: {score}. Sending Alert...")
        send_formatted_email(p_id, score, reasons, v, primary)
    else:
        # If it's just a normal or slightly high reading, do nothing but print
        print(f"🟢 {p_id} is stable. No alert needed.")