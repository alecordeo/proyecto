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
    show_all = True
   
    try:
        conn = get_conn()
        cur = conn.cursor()
       
        if request.method == "POST":
            search_term = request.form.get("search", "")
            if search_term:
                show_all = False
                # ¡CÓDIGO VULNERABLE A SQL INJECTION!
                query = f"SELECT id, nombre, descripcion FROM ejemplo WHERE nombre LIKE '%{search_term}%'"
                print(f"🔍 Ejecutando query vulnerable: {query}")
            else:
                # Query normal para mostrar todos
                query = "SELECT id, nombre, descripcion FROM ejemplo LIMIT 10"
           
            cur.execute(query)
            rows = cur.fetchall()
           
        else:
            # GET request - mostrar límite de registros
            cur.execute("SELECT id, nombre, descripcion FROM ejemplo LIMIT 10")
            rows = cur.fetchall()
           
        cur.close()
        conn.close()
       
    except Exception as e:
        print("Error al leer BD:", e)
        rows = []

    return render_template("index.html", rows=rows, search_term=search_term, show_all=show_all)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))