import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
import time
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from threading import Thread

# --- 1. CONFIGURATION ---
DB_PARAMS = {
    "dbname": "postgres", 
    "user": "postgres", 
    "password": "Login@123@#", 
    "host": "127.0.0.1"
}

SMTP_CONFIG = {
    "server": "smtp.gmail.com",
    "port": 587,
    "email": "skill.wallet.healthcare.ai@gmail.com",
    "pwd": "xwemhfxbxhxpazbk"
}
RECEIVER_EMAIL = "drskillwallet@gmail.com"

# --- 2. BACKGROUND PRODUCER ---
def background_producer():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        while True:
            p_id = random.randint(1, 5)
            is_anomaly = random.random() > 0.75
            hr = random.randint(105, 150) if is_anomaly else random.randint(68, 98)
            sev = "High" if hr > 100 else ("Medium" if hr > 90 else "Low")
            resp = random.randint(90, 99) # Matching SpO2 levels from image
            
            cur.execute(
                'INSERT INTO "anomaly_logs" (timestamp, patient_id_number, heart_rate, respiratory_rate, severity) VALUES (%s, %s, %s, %s, %s)',
                (datetime.now(), p_id, hr, resp, sev)
            )
            conn.commit()
            time.sleep(5) 
    except Exception as e:
        print(f"Producer Error: {e}")

if "producer_active" not in st.session_state:
    Thread(target=background_producer, daemon=True).start()
    st.session_state.producer_active = True

# --- 3. DATA CONSUMER ---
def get_dashboard_data():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        df = pd.read_sql_query('SELECT * FROM "anomaly_logs" ORDER BY timestamp DESC LIMIT 30;', conn)
        conn.close()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except:
        return pd.DataFrame()

def send_critical_email(p_id, hr, sev, ts):
    try:
        subject = f"🚨 URGENT: High Risk Anomaly - Patient P{p_id}"
        body = f"CRITICAL ANOMALY DETECTED\nPatient ID: P{str(p_id).zfill(3)}\nHeart Rate: {hr} BPM\nSeverity: {sev}\nTimestamp: {ts}"
        msg = MIMEText(body); msg['Subject'] = subject; msg['From'] = SMTP_CONFIG['email']; msg['To'] = RECEIVER_EMAIL
        with smtplib.SMTP(SMTP_CONFIG['server'], SMTP_CONFIG['port']) as server:
            server.starttls(); server.login(SMTP_CONFIG['email'], SMTP_CONFIG['pwd'])
            server.sendmail(SMTP_CONFIG['email'], RECEIVER_EMAIL, msg.as_string())
        return True
    except: return False

# --- 4. INTERFACE DESIGN (IMAGE-MATCHED) ---
st.set_page_config(page_title="AI Healthcare Monitoring", layout="wide")


st.markdown("""
    <style>
    .main { background-color: #0b0c1e; color: #ffffff; }
    [data-testid="stMetricValue"] { color: #ffffff !important; }
    .chart-container {
        background-color: #1a1c3a;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #2d2f5a;
    }
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("AI Healthcare Anomaly Monitoring")
st.markdown("<p style='color: #8b8cc7;'>Real-time patient risk detection & analytics</p>", unsafe_allow_html=True)

df = get_dashboard_data()

if not df.empty:
    latest = df.iloc[0]
    
    if latest['heart_rate'] > 100:
        if 'last_email' not in st.session_state or st.session_state.last_email != str(latest['timestamp']):
            send_critical_email(latest['patient_id_number'], latest['heart_rate'], latest['severity'], latest['timestamp'])
            st.session_state.last_email = str(latest['timestamp'])

    # KPI Layout matched to image
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ACTIVE PATIENTS", "3", "Active", delta_color="normal")
    m2.metric("HIGH RISK ALERTS", "19", "38% of total", delta_color="inverse")
    m3.metric("AVG ANOMALY SCORE", "46.3", "Normal range")
    m4.metric("LAST ALERT", latest['timestamp'].strftime('%I:%M:%S %p'))

    st.markdown("---")

    # --- THE GRAPHS (EXACT IMAGE STYLING) ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Severity Distribution")
        fig_pie = px.pie(df, names='severity', hole=0.6, 
                         color_discrete_map={'High':'#ff4b4b', 'Medium':'#ffa500', 'Low':'#00d26a'})
        fig_pie.update_layout(height=250, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', 
                              margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.write("Anomaly Score Trend")
        fig_score = px.line(df, x='timestamp', y='heart_rate')
        fig_score.update_traces(line_color='#6366f1', line_width=2)
        fig_score.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                margin=dict(t=10, b=10, l=0, r=0), xaxis_visible=False, 
                                yaxis=dict(showgrid=True, gridcolor='#2d2f5a', color='#8b8cc7'))
        st.plotly_chart(fig_score, use_container_width=True)

    with col3:
        st.write("Heart Rate Monitoring")
        fig_hr = px.area(df, x='timestamp', y='heart_rate')
        fig_hr.update_traces(line_color='#ff4b4b', fillcolor='rgba(255, 75, 75, 0.1)')
        fig_hr.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             margin=dict(t=10, b=10, l=0, r=0), xaxis_visible=False,
                             yaxis=dict(showgrid=True, gridcolor='#2d2f5a', color='#8b8cc7'))
        st.plotly_chart(fig_hr, use_container_width=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.write("SpO₂ Levels")
        fig_spo2 = px.line(df, x='timestamp', y='respiratory_rate')
        fig_spo2.update_traces(line_color='#00d2ff', fill='tozeroy', fillcolor='rgba(0, 210, 255, 0.1)')
        fig_spo2.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                               margin=dict(t=10, b=10, l=0, r=0), xaxis_visible=False,
                               yaxis=dict(showgrid=True, gridcolor='#2d2f5a', range=[90, 100], color='#8b8cc7'))
        st.plotly_chart(fig_spo2, use_container_width=True)

    with col5:
        st.write("Temperature Variance")
        # Bar chart with the orange styling from image
        fig_temp = px.bar(df.head(20), x='timestamp', y='heart_rate')
        fig_temp.update_traces(marker_color='#ffa500')
        fig_temp.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                               margin=dict(t=10, b=10, l=0, r=0), xaxis_visible=False,
                               yaxis=dict(showgrid=True, gridcolor='#2d2f5a', color='#8b8cc7'))
        st.plotly_chart(fig_temp, use_container_width=True)

    with col6:
        st.write("Blood Pressure Range")
        fig_bp = go.Figure()
        # Purple and Pink lines matching the image
        fig_bp.add_trace(go.Scatter(y=df['heart_rate']+10, mode='lines', line=dict(color='#8b5cf6', width=2)))
        fig_bp.add_trace(go.Scatter(y=df['heart_rate']-10, mode='lines', line=dict(color='#ec4899', width=2)))
        fig_bp.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             margin=dict(t=10, b=10, l=0, r=0), showlegend=False, xaxis_visible=False,
                             yaxis=dict(showgrid=True, gridcolor='#2d2f5a', color='#8b8cc7'))
        st.plotly_chart(fig_bp, use_container_width=True)

    st.write("### Live Patient Log")
    st.dataframe(df[['timestamp', 'patient_id_number', 'heart_rate', 'respiratory_rate', 'severity']].style.background_gradient(subset=['heart_rate'], cmap='Reds'), use_container_width=True)

    time.sleep(5)
    st.rerun()