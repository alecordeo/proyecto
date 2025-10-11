from flask import Flask, render_template
import os
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)

# Render inyecta esta variable si conectas tu app con la base de datos
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    result = urlparse(DATABASE_URL)
    return psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port or 5432
    )

@app.route("/")
def index():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, descripcion FROM ejemplo LIMIT 2;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        rows = []
        print("Error al leer BD:", e)

    return render_template("index.html", rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))