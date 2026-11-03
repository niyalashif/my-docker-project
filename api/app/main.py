from flask import Flask
import psycopg2
import os
import time

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=5432
    )


@app.route("/")
def home():
    return "API is working!"


@app.route("/health")
def health():
    return {"status": "healthy"}


@app.route("/db-test")
def db_test():

    try:
        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute("SELECT version();")

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return {
            "database": "connected",
            "postgresql_version": result[0]
        }

    except Exception as e:

        return {
            "database": "connection failed",
            "error": str(e)
        }, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


