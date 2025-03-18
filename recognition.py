import cv2
import os
import face_recognition
from database import conectar_bd

class FaceRecognition:
    def __init__(self, faces_path):
        self.facesEncodings = []
        self.facesNames = []
        self.faces_path = faces_path
        self.load_faces()

    def load_faces(self):
        """Carga las imágenes y codifica los rostros."""
        for file_name in os.listdir(self.faces_path):
            image = cv2.imread(os.path.join(self.faces_path, file_name))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            encodings = face_recognition.face_encodings(image)
            if len(encodings) > 0:
                self.facesEncodings.append(encodings[0])
                self.facesNames.append(file_name.split(".")[0])

    def recognize_faces(self):
        """Inicia la captura de video y reconoce rostros."""
        cap = cv2.VideoCapture(0)
        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            faces = faceClassif.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                face = frame[y:y + h, x:x + w]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

                encodings = face_recognition.face_encodings(face)
                name = "Desconocido"
                color = (50, 50, 255)

                if len(encodings) > 0:
                    actual_face_encoding = encodings[0]
                    matches = face_recognition.compare_faces(self.facesEncodings, actual_face_encoding)

                    if True in matches:
                        index = matches.index(True)
                        name = self.facesNames[index]
                        color = (125, 220, 0)
                        # Aquí puedes registrar la asistencia en la base de datos

                      # Registrar asistencia en MySQL
                        self.registrar_asistencia(name)

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.rectangle(frame, (x, y + h), (x + w, y + h + 30), color, -1)
                cv2.putText(frame, name, (x, y + h + 25), 2, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        
    def registrar_asistencia(self, student_name):
        """Registra la asistencia en la base de datos."""
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                # Verificar si ya se registró hoy
                query = """
                    SELECT * FROM registro 
                    WHERE student_name = %s AND DATE(date) = CURDATE()
                """
                cursor.execute(query, (student_name,))
                result = cursor.fetchone()

                if result is None:
                    # Registrar nueva asistencia
                    query = """
                        INSERT INTO registro (estudiante, curso, materia, fecha,hora)
                         
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (student_name, datetime.now(), "Presente"))
                    connection.commit()
                    print(f"Asistencia registrada para {student_name}")
                else:
                    print(f"Asistencia ya registrada para {student_name} hoy")
        except Exception as e:
            print(f"Error al registrar la asistencia: {e}")
        finally:
            connection.close()