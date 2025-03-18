import mysql.connector
from mysql.connector import Error
import pymysql
from datetime import datetime
import pytz
import requests
from threading import Thread
from diccionario import guardar_estudiantes_en_diccionario
import os

def conectar_bd():
    """Conecta a la base de datos MySQL en Railway y devuelve la conexión."""
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("MYSQLHOST", "centerbeam.proxy.rlwy.net"),  
            port=os.getenv("MYSQLPORT", "24244"),  
            user=os.getenv("MYSQLUSER", "root"),  
            password=os.getenv("MYSQLPASSWORD", "gdfXAVEjBiGuWIECQjBNKPgiupwMkzch"),  
            database=os.getenv("MYSQLDATABASE", "railway"),  
            #Obligar que use esto
            auth_plugin="caching_sha2_password"
        )
        print("✅ Conexión exitosa a la base de datos")
        return conexion
    except mysql.connector.Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None


    
'''def conectar_bd():
    """Conecta a la base de datos MySQL y devuelve la conexión."""
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='asistencia1'
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None'''

def obtener_estudiantes():
    """Obtiene la lista de estudiantes desde la base de datos."""
    conexion = conectar_bd()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estudiante")
        estudiantes = cursor.fetchall()
        return estudiantes
    except Error as e:
        print(f"Error al obtener estudiantes: {e}")
        return []
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

########## MATERIAS - ESTUDIANTES #############
def obtener_materias():
    """Obtiene la lista de estudiantes desde la base de datos."""
    conexion = conectar_bd()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM materia")
        materias = cursor.fetchall()
        return materias
    except Error as e:
        print(f"Error al obtener materias: {e}")
        return []
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
########################################
def agregar_estudiante(ci, apellidos, nombres, curso, foto, ppff):
    """Agrega un nuevo estudiante a la base de datos."""
    conexion = conectar_bd()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        query = (
            "INSERT INTO estudiante (CI, apellidos, nombres, curso, foto, ppff) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(query, (ci, apellidos, nombres, curso, foto, ppff))
        conexion.commit()
        return True
    except Error as e:
        print(f"Error al agregar estudiante: {e}")
        return False
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


def get_user_credentials(username):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="asistencia1"
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id_docente, CI FROM docente WHERE id_docente = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result:
                return {"username": result[0], "password": result[1]}
    finally:
        connection.close()
    return None

# Función para obtener la lista de cursos
def obtener_cursos():
    connection = conectar_bd()
    try:
        cursor = connection.cursor()
        try:
            query = "SELECT id_curso, nombre_curso FROM curso"
            cursor.execute(query)
            resultados = cursor.fetchall()  # Devuelve una lista de diccionarios
            # Convertir tuplas a diccionarios
            cursos = [{"id_curso": fila[0], "nombre_curso": fila[1]} for fila in resultados]
        finally:
            cursor.close()  # Asegura que el cursor se cierre
        return cursos
    finally:
        connection.close()  # Asegura que la conexión se cierre

# Función para obtener la lista de materias
def obtener_materias1():
    connection = conectar_bd()
    try:
        cursor = connection.cursor()
        try:
            query = "SELECT id_materia, nombre_materia FROM materia"
            cursor.execute(query)
            resultados2 = cursor.fetchall()  # Devuelve una lista de diccionarios
            # Convertir tuplas a diccionarios
            materias = [{"id_materia": fila[0], "nombre_materia": fila[1]} for fila in resultados2]
        
        finally:
            cursor.close()  # Asegura que el cursor se cierre
        return materias
    finally:
        connection.close()  # Asegura que la conexión se cierre

asistencia_registrada = {}

def guardar_estudiantes_en_diccionario():
    """
    Obtiene la lista de estudiantes desde la base de datos
    y los guarda en un diccionario.
    """
    estudiantes = obtener_estudiantes()  # Llama a la función que obtiene los estudiantes
    #print(estudiantes)
    
    if not estudiantes:
        print("No se encontraron estudiantes o hubo un error al obtenerlos.")
        
        return {}

    # Crear un diccionario donde la clave sea el ID del estudiante
    diccionario_estudiantes = {estudiante['id_estudiante']: estudiante for estudiante in estudiantes}
    
    return diccionario_estudiantes

######### MATERIAS - ESTUDIANTES ##############
def guardar_materias_en_diccionario():
    """
    Obtiene la lista de estudiantes desde la base de datos
    y los guarda en un diccionario.
    """
    materias = obtener_materias()  # Llama a la función que obtiene las materias
    #print(estudiantes)
    
    if not materias:
        print("No se encontraron materias o hubo un error al obtenerlos.")
        
        return {}

    # Crear un diccionario donde la clave sea el ID de 
    diccionario_materias = {materia['id_materia']: materia for materia in materias}
    
    return diccionario_materias
#############################################
    
#estudiantes_diccionario = guardar_estudiantes_en_diccionario()

def guardar_asistencia(id_estudiante, id_curso, materia):
    connection=conectar_bd()
    cursor = connection.cursor()
    est=obtener_estudiantes()
    # Obtener fecha y hora actuales
    #ahora = datetime.now()

    # Configurar la zona horaria de Bolivia (UTC-4)
    '''tz_bolivia = pytz.timezone('America/La_Paz')
    ahora = datetime.now(tz_bolivia)  # Obtener la hora exacta de Bolivia
    
    fecha = ahora.date()
    hora = ahora.time()'''
    fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Solo la fecha sin la hora
    hora_actual = datetime.now().strftime("%H:%M:%S")
     

    '''if estudiantes_diccionario:
        #print("Estudiantes guardados en el diccionario:")
        for id_estudiante, datos in estudiantes_diccionario.items():
            print(f"ID: {id_estudiante}, Datos: {datos}")'''
    '''try:
        # Insertar registro en la tabla
        consulta = "INSERT INTO registro(estudiante, curso, materia, fecha, hora, estado) VALUES (%s, %s, %s,%s,%s,%s)"'''
    
    try:
                
        # Si no existe, guardar el registro
        consulta = """
        INSERT INTO registro (estudiante, curso, materia, fecha, hora, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(consulta, (id_estudiante, id_curso, materia, fecha_actual, hora_actual, "Asistido"))
        connection.commit()
        print(f"✅ Registro guardado para estudiante {id_estudiante} el {fecha_actual} a las {hora_actual}")

    except Exception as e:
        print(f"❌ Error al guardar el registro: {e}")

    finally:
        cursor.close()
        connection.close()

