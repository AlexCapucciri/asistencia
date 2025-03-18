import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import mysql.connector
from database import conectar_bd


def obtener_ausencias():
    """Consulta estudiantes con dos ausencias en una materia."""
    conexion = conectar_bd()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)
        query = """
        SELECT 
            id_registro,
            estudiante,
            curso,
            materia,
            fecha, 
            hora, 
            COUNT(estado) AS total_ausencias
        FROM registro r
        WHERE r.estado = 'Asistido'
        GROUP BY estudiante, materia
        HAVING total_ausencias >= 2
        """
        cursor.execute(query)
        ausencias = cursor.fetchall()
        return ausencias
    except mysql.connector.Error as e:
        print(f"Error al consultar ausencias: {e}")
        return []
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def enviar_correo(destinatario, asunto, mensaje):
    """Envía un correo electrónico."""
    remitente = "alexronaldenise@gmail.com"
    contraseña = "kczu nhdr xaxm kkbt"

    try:
        # Configuración del correo
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = destinatario
        msg['Subject'] = asunto

        msg.attach(MIMEText(mensaje, 'plain'))

        # Conexión con el servidor SMTP
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, contraseña)
        servidor.send_message(msg)
        servidor.quit()

        print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

def notificar_ausencias():
    """Notifica a los padres de familia por ausencias de sus hijos."""
    ausencias = obtener_ausencias()
    if not ausencias:
        print("No hay ausencias pendientes para notificar.")
        return

    for registro in ausencias:
        nombre_estudiante = registro['estudiante']
        email="alexronaldenise2@gmail.com"
        email_ppff = email
        nombre_materia = registro['materia']
        total_ausencias = registro['total_ausencias']

        if not email_ppff:
            print(f"No se encontró un correo electrónico para el estudiante {nombre_estudiante}.")
            continue

        asunto = f"Notificación de Ausencias - {nombre_estudiante}"
        mensaje = (
            f"Estimado Padre/Madre de Familia,\n\n"
            f"Le informamos que su hijo/a {nombre_estudiante} ha registrado {total_ausencias} ausencias "
            f"en la materia {nombre_materia}.\n"
            "Por favor, tome las medidas necesarias para evitar más ausencias.\n\n"
            "Atentamente,\nEl Colegio Loyola"
        )

        enviar_correo(email_ppff, asunto, mensaje)

def iniciar_sheduler():
    # 🔹 Programar la ejecución automática cada día a las 08:00 AM
    print("📅 Programando la tarea de notificaciones...")  
    #schedule.every().day.at("08:00").do(notificar_ausencias)
    schedule.every(1).minutes.do(notificar_ausencias)  # Prueba cada 1 minuto en lugar de una hora específica

    #print("⏳ Servicio de notificaciones de ausencias iniciado...")

    # 🔄 Loop infinito para mantener el programa en ejecución
    while True:
        schedule.run_pending()
        time.sleep(10)  # Verifica cada minuto si hay una tarea pendiente
