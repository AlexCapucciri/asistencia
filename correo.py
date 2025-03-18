import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo(destinatario, asunto, cuerpo):
    """
    Envía un correo electrónico.
    """
    # Configuración del servidor SMTP
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587
    remitente = "alexronaldenise@gmail.com"  # Reemplazar con tu correo
    contraseña = "200105839_Denise"  # Reemplazar con tu contraseña o usar una contraseña de aplicación

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(cuerpo, "plain"))

    # Enviar el correo
    try:
        servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
        servidor.starttls()
        servidor.login(remitente, contraseña)
        servidor.sendmail(remitente, destinatario, mensaje.as_string())
        servidor.quit()
        print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
