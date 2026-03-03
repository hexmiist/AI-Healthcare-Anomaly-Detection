🏥 AI-Driven Healthcare Anomaly Detection System


🛠️ Pre-requisitesBefore running this project, ensure you have the following tools and configurations ready:
1. Core Software
  🐍 Python 3.9+: The primary environment for AI and backend logic.
  🎢 Apache Kafka: Handles real-time streaming of patient vitals.
  🗄️ PostgreSQL: Database for storing detected health anomalies.
  🐙 Git: Essential for version control and deployment.
2. Python DependenciesRun this command in your terminal to install all required libraries:
   Bash:  pip install flask flask-cors kafka-python psycopg2-binary tensorflow scikit-learn pandas numpy
3. External Setup📧 Gmail App Password:
   16-character key for the SMTP Email Alert System.
   🔑 Kafka Broker: Ensure the server is running on localhost:9092.


📋 Project Workflow & Milestones
This project is divided into six key milestones to ensure a smooth and reliable healthcare monitoring system.


🏗️ Milestone 1: Environment Setup & Project Initialization
🐍 Activity 1.1: Python 3.9+ Environment Setup
📦 Activity 1.2: Dependency Installation
📊 Activity 1.3: Healthcare Dataset Loading & Validation
📂 Activity 1.4: Project Directory Structure Setup


🧹 Milestone 2: Data Preparation
🔍 Activity 2.1: Exploratory Data Analysis (EDA)
⚙️ Activity 2.2: Feature Engineering for Heart Rate and $SpO_{2}$
📏 Activity 2.3: Feature Scaling using StandardScaler


🧠 Milestone 3: AI Model Development
⏳ Activity 3.1: Temporal Modeling for time-series data
🏋️ Activity 3.2: Unsupervised Machine Learning Model Training
🚨 Activity 3.3: Anomaly Scoring & Severity Classification


📡 Milestone 4: Real-Time Streaming & Alerts
🎢 Activity 4.1: Apache Kafka Integration
⌚ Activity 4.2: Patient-Wise Monitoring logic
💡 Activity 4.3: Explainable Anomaly Detection
📧 Activity 4.4: SMTP Email Alert System for emergency vitals


💻 Milestone 5: Dashboard & Backend
🌐 Activity 5.1: Flask REST API Development
📈 Activity 5.2: Real-time Interactive Dashboard (Chart.js)
🗄️ Activity 5.3: PostgreSQL Database Integration


✅ Milestone 6: Validation & Deployment
🧪 Activity 6.1: Comprehensive System Testing
🆗 Activity 6.2: End-to-End System Validation
🐙 Activity 6.3: GitHub Version Control & Deployment
