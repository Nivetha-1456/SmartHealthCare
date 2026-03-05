# 🩺 SmartHealth AI – Healthcare Monitoring Platform

SmartHealth AI is a **web-based healthcare monitoring and management system** designed to help users track their health data, receive AI-based insights, and connect with healthcare professionals.

The platform provides an integrated solution for **health data logging, AI-driven health analysis, appointment scheduling, medication tracking, and community interaction**.

This project was developed as part of **Project Based Learning (PBL)** for the B.Tech Artificial Intelligence & Machine Learning program.

---

# 📌 Project Overview

Modern healthcare systems require continuous monitoring and proactive health management. SmartHealth AI addresses this need by providing a **digital healthcare platform that enables users to monitor their health, track medical history, and receive AI-based insights about their health condition.**

The platform supports multiple user roles including:

- **Patients** – Track personal health and medical records
- **Doctors** – Monitor patient health data
- **Administrators** – Manage system operations and users

---

# 🚀 Features

## 👤 User Management
- Secure user registration and login
- Role-based authentication system
- Password hashing for security
- Session management

## ❤️ Health Monitoring
Users can log multiple health parameters including:

- Temperature
- Heart Rate
- Blood Pressure
- SpO₂ (Oxygen level)
- Blood Sugar
- Sleep Hours
- Daily Steps
- Stress Level

The system analyzes these inputs to generate a **Health Score and Risk Level**.

---

## 🧠 AI Health Score Analysis

SmartHealth AI includes a simple **AI-based health scoring algorithm** that evaluates user health data.

Example logic:

- Temperature above normal → fever indication
- Low sleep hours → fatigue detection
- Abnormal heart rate → risk warning

The platform calculates a **Health Score (0–100)** and classifies risk levels:

```
Low Risk
Medium Risk
High Risk
```

---

## 🏥 Doctor Dashboard

Doctors can:

- View patient records
- Monitor health data trends
- Manage appointments
- Provide feedback

---

## 👨‍💼 Admin Panel

Administrators can:

- Manage user accounts
- View system statistics
- Monitor platform activity
- Control system access

---

## 💊 Medication Tracking

Patients can:

- Add medications
- Track dosage and schedule
- Monitor medication history

---

## 👨‍👩‍👧 Family Health Tracking

Users can store and monitor family medical history including:

- Family member details
- Health information
- Medical conditions

---

## 📅 Appointment Management

Patients can schedule appointments with doctors.

Features include:

- Appointment scheduling
- Status tracking
- Doctor availability monitoring

---

## 📸 Progress Monitoring

Users can upload **progress images** or health updates to track improvements over time.

---

## 🌐 Community Platform

The system includes a **community discussion feature** where users can:

- Share health experiences
- Ask questions
- Provide support to other users

---

## ⌚ Wearable Device Data Sync

The platform provides API support for smartwatch or wearable data such as:

- Heart rate
- Steps count
- Oxygen levels

---

# 🏗 System Architecture

```
Users (Patient / Doctor / Admin)
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
```

---

# 🗄 Database Schema

The system uses **PostgreSQL** as the primary database.

Main tables include:

- `users`
- `health_records`
- `medications`
- `family_members`
- `appointments`
- `community_posts`
- `progress_photos`

Example relationship:

```
users
 │
 ├── health_records
 ├── medications
 ├── family_members
 ├── appointments
 └── community_posts
```

---

# 🛠 Technologies Used

## Backend
- Python
- Flask
- Flask-Limiter
- psycopg2
- Requests

## Frontend
- HTML
- CSS
- JavaScript

## Database
- PostgreSQL

## Security
- Password hashing
- Secure session cookies
- Rate limiting

## Development Tools
- GitHub
- pgAdmin
- Draw.io (for diagrams)

---

# 📂 Project Structure

```
SmartHealthCare
│
├── app.py
├── requirements.txt
├── .env.example
│
├── static
│   ├── css
│   │   └── style.css
│   └── js
│       └── main.js
│
├── templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard_patient.html
│   ├── dashboard_doctor.html
│   ├── dashboard_admin.html
│   ├── profile.html
│   ├── health.html
│   ├── appointments.html
│   ├── reports.html
│   └── community.html
│
├── uploads
│
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Nivetha-1456/SmartHealthCare.git
```

```
cd SmartHealthCare
```

---

## 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## 3️⃣ Setup Environment Variables

Create a `.env` file in the root directory.

```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://postgres:password@localhost:5432/smarthealth
```

---

## 4️⃣ Run the Application

```
python app.py
```

---

# 🌐 Access the Application

Open the browser and go to:

```
http://127.0.0.1:5000
```

---

# 🔑 Default Admin Login

```
Username: admin
Password: admin123
```

---

# 📸 Screenshots

Add screenshots of your platform here:

- Homepage
- Patient Dashboard
- Health Monitoring Page
- Doctor Dashboard
- Admin Panel
- Community Page

---

# 📈 Future Enhancements

The platform can be further improved with:

- Machine Learning based disease prediction
- Integration with wearable devices (Fitbit / Apple Health)
- Real-time health monitoring
- Mobile application using Capacitor
- Telemedicine video consultation
- Advanced AI health analytics dashboard

---

# 📚 References

1. Flask Documentation  
2. PostgreSQL Documentation  
3. AI in Healthcare Research Papers  
4. Health Monitoring Systems Literature  

---

# 👩‍💻 Author

**Niveditha Adepu**  
B.Tech – Artificial Intelligence & Machine Learning  
Woxsen University

---

# ⭐ Acknowledgement

This project was developed as part of **Project Based Learning (PBL)** under the guidance of faculty from the **School of Technology, Woxsen University**.

---
