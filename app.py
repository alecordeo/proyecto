from flask import Flask, render_template, request, redirect, url_for, session
import os
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sessions'  # Necesaria para sessions

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
    # Si es POST, procesar y REDIRIGIR a GET
    if request.method == "POST":
        search_term = request.form.get("search", "")
        print(f"🔍 Búsqueda recibida: '{search_term}'")
       
        try:
            conn = get_conn()
            cur = conn.cursor()
           
            # Query vulnerable
            query = f"SELECT id, nombre, descripcion FROM ejemplo WHERE nombre LIKE '%{search_term}%'"
            print(f"📝 Query ejecutada: {query}")
           
            cur.execute(query)
            rows = cur.fetchall()
            print(f"✅ Resultados: {len(rows)} registros")
           
            cur.close()
            conn.close()
           
            # Guardar resultados en session y REDIRIGIR
            session['last_search_results'] = rows
            session['last_search_term'] = search_term
            session['show_results'] = True
           
            return redirect(url_for('index'))
           
        except Exception as e:
            print(f"❌ Error: {e}")
            session['last_search_results'] = []
            session['last_search_term'] = search_term
            session['show_results'] = True
            session['error'] = str(e)
            return redirect(url_for('index'))
   
    # GET request - mostrar página con datos de session si existen
    rows = session.pop('last_search_results', [])
    search_term = session.pop('last_search_term', '')
    show_results = session.pop('show_results', False)
    error = session.pop('error', None)
   
    return render_template("index.html",
                         rows=rows,
                         search_term=search_term,
                         show_results=show_results,
                         error=error)

@app.route("/clear")
def clear():
    # Ruta para limpiar session manualmente
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))