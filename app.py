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


if __name__ == "__main__":
    app.run(debug=True)
