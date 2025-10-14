from flask import Flask, render_template, request
import os
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def index():
    rows = []
    search_term = ""
   
    if request.method == "POST":
        search_term = request.form.get("search", "")
       
        try:
            conn = get_conn()
            cur = conn.cursor()
           
            if search_term:
                # ¡CÓDIGO VULNERABLE A SQL INJECTION!
                query = f"SELECT id, nombre, descripcion FROM ejemplo WHERE nombre LIKE '%{search_term}%'"
                print(f"🔍 Ejecutando query vulnerable: {query}")
            else:
                # Si buscan vacío, mostrar todos
                query = "SELECT id, nombre, descripcion FROM ejemplo"
           
            cur.execute(query)
            rows = cur.fetchall()
           
            cur.close()
            conn.close()
           
        except Exception as e:
            print("Error en búsqueda:", e)
            rows = []

    return render_template("index.html", rows=rows, search_term=search_term)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))