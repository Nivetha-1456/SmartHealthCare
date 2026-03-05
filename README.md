🩺 SmartHealth AI – Healthcare Monitoring Platform

SmartHealth AI is a web-based healthcare monitoring and management platform designed to help patients track their health, connect with doctors, and receive AI-based insights.
The system integrates health data logging, AI health score analysis, appointment management, and community interaction in a single platform.

This project was developed as part of Project Based Learning (PBL) for B.Tech AI/ML.

📌 Features
👤 User Management

Secure user registration and login

Role-based access:

Patient

Doctor

Admin

Password hashing for security

❤️ Health Monitoring

Log health parameters:

Temperature

Heart Rate

Blood Pressure

SpO₂

Blood Sugar

Sleep Hours

Steps

Stress Level

Automatic Health Score calculation

AI-based risk level prediction

🏥 Doctor Dashboard

View patient data

Monitor health logs

Manage appointments

👨‍⚕️ Admin Panel

Manage users

Monitor platform statistics

System administration

📅 Appointment System

Schedule doctor appointments

Track appointment status

💊 Medication Tracker

Add medications

Track dosage and time

Manage medication history

👨‍👩‍👧 Family Health Tracking

Add family members

Monitor family medical history

📸 Progress Monitoring

Upload health progress photos

Track improvements over time

🌐 Community Platform

Users can share health experiences

Support and discussion forum

⌚ Wearable Data Sync

API support for smartwatch data

Heart rate, steps, and oxygen levels

🧠 AI Features

SmartHealth AI includes an AI-based health scoring system that analyzes user health metrics.

Example:

Parameter	Effect
Temperature	Detects fever risk
Heart Rate	Identifies abnormal pulse
Sleep Hours	Detects fatigue
SpO₂	Oxygen level monitoring

The system calculates a Health Score (0–100) and categorizes risk levels:

Low Risk
Medium Risk
High Risk
🏗 System Architecture
User (Patient / Doctor / Admin)
        │
        ▼
Frontend (HTML, CSS, JavaScript)
        │
        ▼
Flask Backend (REST API)
        │
        ▼
PostgreSQL Database
        │
        ▼
AI Health Analysis Engine
🗄 Database Schema

Main tables used in the system:

users

health_records

medications

family_members

appointments

community_posts

progress_photos

The database is implemented using PostgreSQL.

🛠 Technologies Used
Backend

Python

Flask

Flask-Limiter

psycopg2

Requests

Frontend

HTML

CSS

JavaScript

Database

PostgreSQL

Security

Password hashing

Secure session cookies

Rate limiting

Tools

GitHub

pgAdmin

Draw.io (for diagrams)

📂 Project Structure
SmartHealth-AI
│
├── app.py
├── requirements.txt
├── .env.example
│
├── static
│   ├── css
│   └── js
│
├── templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard_patient.html
│   ├── dashboard_doctor.html
│   ├── dashboard_admin.html
│
├── uploads
│
└── README.md
⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/smarthealth-ai.git
cd smarthealth-ai
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Setup Environment Variables

Create .env file:

SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://postgres:password@localhost:5432/smarthealth
4️⃣ Run the application
python app.py

Open browser:

http://127.0.0.1:5000
🔑 Default Admin Login
Username: admin
Password: admin123
📊 Screenshots

Add screenshots here:

Homepage

Patient Dashboard

Doctor Dashboard

Admin Panel

Health Monitoring Interface

📈 Future Enhancements

Fitbit / Apple Health integration

Machine learning health prediction

Real-time wearable device monitoring

Mobile application using Capacitor

Advanced health analytics dashboard

Telemedicine video consultation

📚 References

Flask Documentation

PostgreSQL Documentation

Health Monitoring Research Papers

AI Healthcare Systems

👩‍💻 Author

Niveditha Adepu
B.Tech – AI & Machine Learning
Woxsen University
