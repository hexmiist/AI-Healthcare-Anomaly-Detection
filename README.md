# AI-Healthcare-Anomaly-Detection
🛠️ Pre-requisites
Before running this project, ensure you have the following installed and configured:

1. Core Software
🐍 Python 3.9+: The primary programming language for AI and backend logic.

🎢 Apache Kafka: Used for real-time data streaming of patient vitals.

🗄️ PostgreSQL: The database for persistent storage of detected anomalies.

🐙 Git: For version control and project management.

2. Python Dependencies
Install the required libraries using the following command:

Bash
pip install flask flask-cors kafka-python psycopg2-binary tensorflow scikit-learn pandas numpy
🧠 AI/ML: tensorflow, scikit-learn.

🌐 Backend: flask, flask-cors.

📊 Data: pandas, numpy.

3. External Configurations
📧 Gmail App Password: Required for the SMTP Email Alert System to send emergency notifications.

🔑 Kafka Broker: Ensure Zookeeper and Kafka server are running on localhost:9092



🎯Project Workflow & Milestones
  This project follows a structured development lifecycle to ensure real-time accuracy and system reliability.


➡️Milestone 1: Environment Setup & Project Initialization
Activity 1.1: Python 3.9+ Environment Setup

Activity 1.2: Dependency Installation (Flask, Kafka, TensorFlow, etc.)

Activity 1.3: Healthcare Dataset Loading & Validation

Activity 1.4: Project Directory Structure Setup


➡️Milestone 2: Data Preparation
Activity 2.1: Exploratory Data Analysis (EDA) on patient vitals

Activity 2.2: Feature Engineering for Heart Rate and SpO2

Activity 2.3: Feature Scaling using StandardScaler


➡️Milestone 3: AI Model Development
Activity 3.1: Temporal Modeling for time-series data

Activity 3.2: Unsupervised Model Training

Activity 3.3: Anomaly Scoring & Severity Classification


➡️Milestone 4: Real-Time Streaming & Alerts
Activity 4.1: Apache Kafka Integration for data streaming

Activity 4.2: Patient-Wise Monitoring logic

Activity 4.3: Explainable Anomaly Detection

Activity 4.4: SMTP Email Alert System for critical vitals


➡️Milestone 5: Dashboard & Backend
Activity 5.1: Flask REST API Development

Activity 5.2: Real-time Interactive Dashboard (Chart.js)

Activity 5.3: PostgreSQL Database Integration


➡️Milestone 6: Validation & Deployment
Activity 6.1: System Testing

Activity 6.2: End-to-End Validation

Activity 6.3: GitHub Version Control & Deployment
