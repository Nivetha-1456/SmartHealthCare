import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import datetime
import random

app = Flask(__name__)
app.secret_key = 'smart_healthcare_secret'  # Change in production!
DATABASE = 'healthcare.db'

# For progress photos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        db.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'Patient',
                full_name TEXT,
                age INTEGER,
                gender TEXT,
                height REAL,
                weight REAL,
                bmi REAL,
                medical_history TEXT,
                allergies TEXT,
                current_medications TEXT,
                family_medical_history TEXT
            );

            CREATE TABLE IF NOT EXISTS family_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                age INTEGER,
                relationship TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS health_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                temperature REAL,
                heart_rate INTEGER,
                bp TEXT,
                spo2 INTEGER,
                blood_sugar REAL,
                cholesterol REAL,
                sleep_hours REAL,
                water_intake REAL,
                steps INTEGER,
                stress_level INTEGER,
                mood TEXT,
                bmi REAL,
                health_score INTEGER,
                risk_level TEXT,
                ai_diagnosis TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                date TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'Pending'
            );

            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                doctor_id INTEGER,
                rating INTEGER,
                feedback TEXT
            );

            -- New tables for additional features
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                dosage TEXT,
                time TEXT,
                frequency TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS progress_photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                image_path TEXT NOT NULL,
                date DATE NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS community_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        ''')
        db.commit()

init_db()

# --- Helper Functions ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Context Processors ---
@app.context_processor
def utility_processor():
    return {'now': datetime.datetime.now}

@app.context_processor
def inject_user():
    db = get_db()
    current_user = None
    if 'user_id' in session:
        current_user = db.execute("SELECT * FROM users WHERE id=?", (session['user_id'],)).fetchone()
    return dict(current_user=current_user)

# --- Auth Decorators ---
def login_required(f):
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

def role_required(role):
    def decorator(f):
        def wrap(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            if session.get('role') != role:
                flash('Unauthorized access!', 'error')
                return redirect(url_for('dashboard_patient'))
            return f(*args, **kwargs)
        wrap.__name__ = f.__name__
        return wrap
    return decorator

# --- Routes ---
@app.route('/')
def index():
    if 'user_id' in session:
        role = session.get('role')
        if role == 'Admin':
            return redirect(url_for('dashboard_admin'))
        elif role == 'Doctor':
            return redirect(url_for('dashboard_doctor'))
        else:
            return redirect(url_for('dashboard_patient'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'Patient')
        if role not in ['Patient', 'Doctor']:
            role = 'Patient'
        hashed_pw = generate_password_hash(password)
        db = get_db()
        try:
            db.execute('INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
                       (username, email, hashed_pw, role))
            db.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or Email already exists!', 'error')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            if user['role'] == 'Admin':
                return redirect(url_for('dashboard_admin'))
            elif user['role'] == 'Doctor':
                return redirect(url_for('dashboard_doctor'))
            else:
                return redirect(url_for('dashboard_patient'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

# --- Dashboards ---
@app.route('/patient/dashboard')
@role_required('Patient')
def dashboard_patient():
    db = get_db()
    records = db.execute('SELECT * FROM health_records WHERE user_id=? ORDER BY date DESC LIMIT 5', (session['user_id'],)).fetchall()
    latest_record = records[0] if records else None
    return render_template('dashboard_patient.html', records=records, latest=latest_record)

@app.route('/doctor/dashboard')
@role_required('Doctor')
def dashboard_doctor():
    db = get_db()
    patients = db.execute('SELECT * FROM users WHERE role="Patient"').fetchall()
    appts = db.execute('''
        SELECT a.*, u.full_name FROM appointments a
        JOIN users u ON a.patient_id = u.id
        WHERE a.doctor_id = ? AND a.status = "Pending"
    ''', (session['user_id'],)).fetchall()
    return render_template('dashboard_doctor.html', patients=patients, appointments=appts)

@app.route('/admin/dashboard')
@role_required('Admin')
def dashboard_admin():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    record_count = db.execute('SELECT COUNT(*) as c FROM health_records').fetchone()['c']
    return render_template('dashboard_admin.html', users=users, record_count=record_count)

# --- Profile ---
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    db = get_db()
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        height = float(request.form.get('height') or 0)
        weight = float(request.form.get('weight') or 0)
        bmi = weight / ((height/100)**2) if height > 0 else 0
        medical_history = request.form.get('medical_history')
        allergies = request.form.get('allergies')
        db.execute('''UPDATE users SET full_name=?, age=?, gender=?, height=?, weight=?, bmi=?,
            medical_history=?, allergies=? WHERE id=?''',
            (full_name, age, gender, height, weight, bmi, medical_history, allergies, session['user_id']))
        db.commit()
        flash('Profile updated successfully!', 'success')
    user = db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    return render_template('profile.html', user=user)

# --- Health Logs ---
@app.route('/health', methods=['GET', 'POST'])
@role_required('Patient')
def health():
    db = get_db()
    if request.method == 'POST':
        temp = float(request.form.get('temperature', 98.6))
        hr = int(request.form.get('heart_rate', 70))
        bp = request.form.get('bp', '120/80')
        spo2 = int(request.form.get('spo2', 98))
        sugar = float(request.form.get('blood_sugar', 90))
        sleep = float(request.form.get('sleep_hours', 7))
        steps = int(request.form.get('steps', 0))
        stress = int(request.form.get('stress_level', 5))

        # AI Mock Logic
        health_score = max(0, 100 - (abs(98.6 - temp)*10 + abs(70 - hr) + (100 - spo2)*2))
        risk_level = "High" if health_score < 50 else ("Medium" if health_score < 75 else "Low")
        ai_diagnosis = "Fatigue detected" if sleep < 5 else "Normal"
        if temp > 100:
            ai_diagnosis = "Fever indicated"

        db.execute('''INSERT INTO health_records
            (user_id, temperature, heart_rate, bp, spo2, blood_sugar, sleep_hours, steps, stress_level, health_score, risk_level, ai_diagnosis)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (session['user_id'], temp, hr, bp, spo2, sugar, sleep, steps, stress, health_score, risk_level, ai_diagnosis))
        db.commit()
        flash('Health data logged!', 'success')
        return redirect(url_for('health'))

    records = db.execute('SELECT * FROM health_records WHERE user_id=? ORDER BY date DESC', (session['user_id'],)).fetchall()
    return render_template('health.html', records=records)

# --- Appointments ---
@app.route('/appointments')
@login_required
def appointments():
    db = get_db()
    user_id = session['user_id']
    role = session['role']
    if role == 'Patient':
        appts = db.execute('''
            SELECT a.*, u.full_name as doctor_name FROM appointments a
            JOIN users u ON a.doctor_id = u.id
            WHERE a.patient_id = ? ORDER BY a.date
        ''', (user_id,)).fetchall()
    elif role == 'Doctor':
        appts = db.execute('''
            SELECT a.*, u.full_name as patient_name FROM appointments a
            JOIN users u ON a.patient_id = u.id
            WHERE a.doctor_id = ? ORDER BY a.date
        ''', (user_id,)).fetchall()
    else:
        appts = []
    return render_template('appointments.html', appointments=[dict(a) for a in appts], role=role)

# --- Static Feature Pages (PAGE ROUTES – these render the HTML templates) ---
@app.route('/medications')
@login_required
def medications():
    return render_template('medications.html')

@app.route('/family')
@login_required
def family():
    return render_template('family.html')

@app.route('/progress')
@login_required
def progress():
    return render_template('progress.html')

@app.route('/community')
@login_required
def community():
    return render_template('community.html')

@app.route('/video_call')
@login_required
def video_call():
    return render_template('video_call.html')

@app.route('/ai_doctor')
@login_required
def ai_doctor():
    return render_template('ai_doctor.html')

@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

# --- API Routes for Medications (DATA ROUTES) ---
@app.route('/api/medications', methods=['GET'])
@login_required
def get_medications():
    db = get_db()
    meds = db.execute('SELECT * FROM medications WHERE user_id=? ORDER BY time', (session['user_id'],)).fetchall()
    return jsonify([dict(m) for m in meds])

@app.route('/api/medications', methods=['POST'])
@login_required
def add_medication():
    data = request.json
    db = get_db()
    db.execute('''INSERT INTO medications (user_id, name, dosage, time, frequency)
                  VALUES (?, ?, ?, ?, ?)''',
               (session['user_id'], data['name'], data['dosage'], data['time'], data['frequency']))
    db.commit()
    return jsonify({'status': 'success'})

@app.route('/api/medications/<int:med_id>', methods=['DELETE'])
@login_required
def delete_medication(med_id):
    db = get_db()
    db.execute('DELETE FROM medications WHERE id=? AND user_id=?', (med_id, session['user_id']))
    db.commit()
    return jsonify({'status': 'success'})

# --- API Routes for Family ---
@app.route('/api/family', methods=['GET'])
@login_required
def get_family():
    db = get_db()
    family = db.execute('SELECT * FROM family_members WHERE user_id=?', (session['user_id'],)).fetchall()
    return jsonify([dict(m) for m in family])

@app.route('/api/family', methods=['POST'])
@login_required
def add_family():
    data = request.json
    db = get_db()
    db.execute('''INSERT INTO family_members (user_id, name, age, relationship)
                  VALUES (?, ?, ?, ?)''',
               (session['user_id'], data['name'], data['age'], data['relationship']))
    db.commit()
    return jsonify({'status': 'success'})

@app.route('/api/family/<int:member_id>', methods=['DELETE'])
@login_required
def delete_family(member_id):
    db = get_db()
    db.execute('DELETE FROM family_members WHERE id=? AND user_id=?', (member_id, session['user_id']))
    db.commit()
    return jsonify({'status': 'success'})

# --- API Routes for Progress Photos ---
@app.route('/api/progress', methods=['POST'])
@login_required
def upload_progress():
    if 'photo' not in request.files:
        return jsonify({'error': 'No file'}), 400
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{session['user_id']}_{datetime.datetime.now().timestamp()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        db = get_db()
        db.execute('''INSERT INTO progress_photos (user_id, image_path, date)
                      VALUES (?, ?, ?)''',
                   (session['user_id'], filepath, datetime.date.today()))
        db.commit()
        return jsonify({'status': 'success', 'path': filepath})
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/progress', methods=['GET'])
@login_required
def get_progress():
    db = get_db()
    photos = db.execute('SELECT * FROM progress_photos WHERE user_id=? ORDER BY date DESC', (session['user_id'],)).fetchall()
    return jsonify([dict(p) for p in photos])

# --- API Routes for Community ---
@app.route('/api/community', methods=['GET'])
@login_required
def get_posts():
    db = get_db()
    posts = db.execute('''
        SELECT p.*, u.username FROM community_posts p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC LIMIT 50
    ''').fetchall()
    return jsonify([dict(p) for p in posts])

@app.route('/api/community', methods=['POST'])
@login_required
def create_post():
    data = request.json
    db = get_db()
    db.execute('INSERT INTO community_posts (user_id, content) VALUES (?, ?)',
               (session['user_id'], data['content']))
    db.commit()
    return jsonify({'status': 'success'})

# --- Watch Sync (simulated) ---
@app.route('/api/watch/sync', methods=['POST'])
@login_required
def watch_sync():
    data = request.json
    db = get_db()
    db.execute('''INSERT INTO health_records (user_id, heart_rate, steps, spo2, ai_diagnosis)
                  VALUES (?, ?, ?, ?, ?)''',
               (session['user_id'], data.get('heart_rate'), data.get('steps'), data.get('spo2'), 'Watch Sync'))
    db.commit()
    return jsonify({'status': 'success'})

# --- Create default Admin if none exists ---
with app.app_context():
    db = get_db()
    admin = db.execute("SELECT * FROM users WHERE role='Admin'").fetchone()
    if not admin:
        pw = generate_password_hash('admin123')
        db.execute("INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                   ('admin', 'admin@example.com', pw, 'Admin'))
        db.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)