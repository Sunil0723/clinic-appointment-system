from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="clinic_db"
    )
    return connection


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/patients")
def patients():
    return render_template("patients.html")


@app.route("/add_patient", methods=["POST"])
def add_patient():
    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO patients (name, phone, email)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, phone, email))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect("/patients")


@app.route("/doctors")
def doctors():
    return render_template("doctors.html")


@app.route("/add_doctor", methods=["POST"])
def add_doctor():
    name = request.form["name"]
    specialization = request.form["specialization"]

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO doctors (name, specialization)
        VALUES (%s, %s)
    """

    cursor.execute(query, (name, specialization))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect("/doctors")


@app.route("/appointments")
def appointments():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id, name FROM patients")
    patients = cursor.fetchall()

    cursor.execute("SELECT id, name, specialization FROM doctors")
    doctors = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "appointments.html",
        patients=patients,
        doctors=doctors
    )


@app.route("/book_appointment", methods=["POST"])
def book_appointment():
    patient_id = request.form["patient_id"]
    doctor_id = request.form["doctor_id"]
    appointment_date = request.form["appointment_date"]
    appointment_time = request.form["appointment_time"]

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO appointments
        (patient_id, doctor_id, appointment_date, appointment_time)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (patient_id, doctor_id, appointment_date, appointment_time)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return redirect("/appointments")


if __name__ == "__main__":
    app.run(debug=True)
