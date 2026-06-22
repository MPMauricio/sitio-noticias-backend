from flask import Flask, request, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# 🔑 REEMPLAZA ESTA URL: Pega aquí la "Connection String" completa que copiaste de Neon
URL_CONEXION_NEON = "postgresql://neondb_owner:npg_YDjrI80SacUb@ep-tiny-waterfall-ahcpsftn.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"

@app.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    comentario = request.form.get('comentario')
    
    try:
        # Nos conectamos directamente a la nube usando la URL
        conexion = psycopg2.connect(URL_CONEXION_NEON)
        cursor = conexion.cursor()
        
        # En PostgreSQL se usa %s para los valores, igual que en MySQL
        sql = "INSERT INTO suscriptores (nombre, correo, comentario) VALUES (%s, %s, %s)"
        valores = (nombre, correo, comentario)
        
        cursor.execute(sql, valores)
        conexion.commit()
        
        cursor.close()
        conexion.close()
        
        return '''
        <div style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h1 style="color: #2b6cb0;">¡Suscripción Guardada en la Nube!</h1>
            <p>Los datos han viajado con éxito desde tu laptop hasta los servidores de Neon.</p>
            <a href="http://127.0.0.1:5500/index.html" style="color: #1a365d; font-weight: bold; text-decoration: none;">← Volver al Periódico</a>
        </div>
        '''
        
    except Exception as err:
        return f'''
        <div style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px; color: red;">
            <h1>Hubo un error en la conexión remota</h1>
            <p>{err}</p>
            <a href="http://127.0.0.1:5500/index.html">Intentar de nuevo</a>
        </div>
        '''

@app.route('/usuarios')
def ver_usuarios():
    try:
        conexion = psycopg2.connect(URL_CONEXION_NEON)
        # RealDictCursor sirve para que los datos vengan ordenados como un diccionario, igual que en MySQL
        cursor = conexion.cursor(cursor_factory=RealDictCursor) 
        
        cursor.execute("SELECT * FROM suscriptores")
        lista_suscriptores = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        
        # Renderizamos tu tabla en usuarios.html
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