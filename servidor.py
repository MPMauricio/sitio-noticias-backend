import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

# 1. Cargamos el archivo secreto .env que creamos por consola
load_dotenv()

# 2. Python lee la nueva URL en completo secreto sin exponerla en GitHub
URL_CONEXION_NEON = os.getenv("URL_CONEXION_NEON")

app = Flask(__name__)

@app.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    comentario = request.form.get('comentario')
    
    try:
        conexion = psycopg2.connect(URL_CONEXION_NEON)
        cursor = conexion.cursor()
        
        sql = "INSERT INTO suscriptores (nombre, correo, comentario) VALUES (%s, %s, %s)"
        valores = (nombre, correo, comentario)
        
        cursor.execute(sql, valores)
        conexion.commit()
        
        cursor.close()
        conexion.close()
        
        return '''
        <div style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h1 style="color: #2b6cb0;">¡Suscripción Guardada en la Nube!</h1>
            <p>Los datos han viajado con éxito desde internet hasta los servidores de Neon.</p>
            <a href="https://mpmauricio.github.io/sitio-noticias-backend/" style="color: #1a365d; font-weight: bold; text-decoration: none;">← Volver al Periódico</a>
        </div>
        '''
        
    except Exception as err:
        return f'''
        <div style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px; color: red;">
            <h1>Hubo un error en la conexión remota</h1>
            <p>{err}</p>
            <a href="https://mpmauricio.github.io/sitio-noticias-backend/">Intentar de nuevo</a>
        </div>
        '''

@app.route('/usuarios')
def ver_usuarios():
    try:
        conexion = psycopg2.connect(URL_CONEXION_NEON)
        cursor = conexion.cursor(cursor_factory=RealDictCursor) 
        
        cursor.execute("SELECT * FROM suscriptores ORDER BY id DESC;")
        lista_suscriptores = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        
        return render_template('usuarios.html', suscriptores=lista_suscriptores)
        
    except Exception as err:
        return f'''
        <div style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px; color: red;">
            <h1>Error al cargar el panel desde la nube</h1>
            <p>{err}</p>
            <a href="https://mpmauricio.github.io/sitio-noticias-backend/">Volver al Periódico</a>
        </div>
        '''

if __name__ == '__main__':
    app.run(debug=True, port=5001)