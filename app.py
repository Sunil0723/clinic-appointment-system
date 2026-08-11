from flask import Flask, render_template
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


if __name__ == "__main__":
    app.run(debug=True)
