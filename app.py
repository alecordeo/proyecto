from flask import Flask, render_template, request, redirect, url_for
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
    # Solo manejar POST para procesar búsquedas
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
           
            # Pasar los resultados como parámetros en la redirección
            return render_template("index.html",
                                 rows=rows,
                                 search_term=search_term,
                                 show_results=True)
           
        except Exception as e:
            print("Error en búsqueda:", e)
            return render_template("index.html",
                                 rows=[],
                                 search_term=search_term,
                                 error=str(e),
                                 show_results=True)
   
    # GET request - mostrar página limpia
    return render_template("index.html",
                         rows=[],
                         search_term="",
                         show_results=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
