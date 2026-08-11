from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="clinic_db"
    )
    return connection


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Total patients
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM patients
        """)
        total_patients = cursor.fetchone()["total"]

        # Total doctors
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM doctors
        """)
        total_doctors = cursor.fetchone()["total"]

        # Total appointments
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM appointments
        """)
        total_appointments = cursor.fetchone()["total"]

        # Today's appointments
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM appointments
            WHERE appointment_date = CURDATE()
        """)
        todays_appointments = cursor.fetchone()["total"]

        # Recent appointments
        cursor.execute("""
            SELECT
                a.id,
                p.name AS patient_name,
                d.name AS doctor_name,
                d.specialization,
                a.appointment_date,
                a.appointment_time,
                a.status
            FROM appointments a
            JOIN patients p
                ON a.patient_id = p.id
            JOIN doctors d
                ON a.doctor_id = d.id
            ORDER BY
                a.appointment_date DESC,
                a.appointment_time DESC
            LIMIT 5
        """)

        recent_appointments = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "dashboard.html",
        total_patients=total_patients,
        total_doctors=total_doctors,
        total_appointments=total_appointments,
        todays_appointments=todays_appointments,
        recent_appointments=recent_appointments
    )


# =========================
# PATIENTS
# =========================

@app.route("/patients")
def patients():
    return render_template("patients.html")


# =========================
# ADD PATIENT
# =========================

@app.route("/add_patient", methods=["POST"])
def add_patient():

    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form.get("email", "")

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO patients
            (name, phone, email)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (name, phone, email)
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()

    return redirect("/patients")


# =========================
# DOCTORS
# =========================

@app.route("/doctors")
def doctors():
    return render_template("doctors.html")


# =========================
# ADD DOCTOR
# =========================

@app.route("/add_doctor", methods=["POST"])
def add_doctor():

    name = request.form["name"]
    specialization = request.form["specialization"]

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO doctors
            (name, specialization)
            VALUES (%s, %s)
        """

        cursor.execute(
            query,
            (name, specialization)
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()

    return redirect("/doctors")


# =========================
# APPOINTMENTS
# =========================

@app.route("/appointments")
def appointments():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Get patients
        cursor.execute("""
            SELECT
                id,
                name
            FROM patients
            ORDER BY name
        """)

        patients = cursor.fetchall()

        # Get doctors
        cursor.execute("""
            SELECT
                id,
                name,
                specialization
            FROM doctors
            ORDER BY name
        """)

        doctors = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "appointments.html",
        patients=patients,
        doctors=doctors
    )


# =========================
# BOOK APPOINTMENT
# =========================

@app.route("/book_appointment", methods=["POST"])
def book_appointment():

    patient_id = request.form["patient_id"]
    doctor_id = request.form["doctor_id"]
    appointment_date = request.form["appointment_date"]
    appointment_time = request.form["appointment_time"]

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO appointments
            (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time
            )
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time
            )
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()

    return redirect("/appointments")


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)
