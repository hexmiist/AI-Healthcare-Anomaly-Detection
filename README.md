# AI-Driven Healthcare Anomaly Detection System

## 🛠 Pre-requisites
The following tools and configurations are required to set up and run the system smoothly.

### 1. Core Software
* **Python 3.9+**: Primary environment for AI and backend logic.
* **Apache Kafka**: Handles real-time streaming of patient vitals.
* **PostgreSQL**: Database for persistent storage of detected anomalies.
* **Git**: Used for version control and project management.

### 2. Python Dependencies
Install all required libraries using the following command:

`pip install flask flask-cors kafka-python psycopg2-binary tensorflow scikit-learn pandas numpy`

### 3. External Configurations
* **SMTP Alerting**: A 16-character Gmail App Password is required for emergency notifications.
* **Kafka Broker**: Ensure the server is active on `localhost:9092`.

---

## 📋 Project Workflow & Milestones
This project is structured into six milestones to ensure reliability and scalability.

### Milestone 1: Environment Setup & Project Initialization
* **Activity 1.1:** Python 3.9+ Environment Setup
* **Activity 1.2:** Dependency Installation
* **Activity 1.3:** Healthcare Dataset Loading & Validation
* **Activity 1.4:** Project Directory Structure Setup

### Milestone 2: Data Preparation
* **Activity 2.1:** Exploratory Data Analysis (EDA)
* **Activity 2.2:** Feature Engineering for Heart Rate and SpO2
* **Activity 2.3:** Feature Scaling using StandardScaler

### Milestone 3: AI Model Development
* **Activity 3.1:** Temporal Modeling for time-series data
* **Activity 3.2:** Unsupervised Machine Learning Model Training
* **Activity 3.3:** Anomaly Scoring & Severity Classification

### Milestone 4: Real-Time Streaming & Alerts
* **Activity 4.1:** Apache Kafka Integration
* **Activity 4.2:** Patient-Wise Monitoring logic
* **Activity 4.3:** Explainable Anomaly Detection
* **Activity 4.4:** SMTP Email Alert System for emergency vitals

### Milestone 5: Dashboard & Backend
* **Activity 5.1:** Flask Backend Development
* **Activity 5.2:** Interactive Dashboard Development
* **Activity 5.3:** PostgreSQL Database Integration

### Milestone 6: Validation & Deployment
* **Activity 6.1:** Comprehensive System Testing
* **Activity 6.2:** End-to-End System Validation
* **Activity 6.3:** GitHub Version Control & Deployment [cite: Activity 6
