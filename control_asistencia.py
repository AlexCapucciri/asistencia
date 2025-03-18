from flask import Flask, render_template, Response, request
import cv2
import face_recognition
import numpy as np

app = Flask(__name__)

# Base de datos simulada de estudiantes
KNOWN_FACES = [
    {
        "name": "Estudiante 1",
        "image_path": "static/faces/Alex.jpg"
    },
    {
        "name": "Estudiante 2",
        "image_path": "static/faces/Sheimi.jpg"
    }
]

# Cargar las imágenes y codificaciones conocidas
known_face_encodings = []
known_face_names = []

for face in KNOWN_FACES:
    image = face_recognition.load_image_file(face["image_path"])
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)
    known_face_names.append(face["name"])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/control_asistenci', methods=['POST'])
def control_asistenci():
    curso = request.form.get('curso')
    materia = request.form.get('materia')
    return render_template('control_facial.html', curso=curso, materia=materia)


@app.route('/video_feed')
def video_feed():
    """RUTA: Transmite el video en vivo."""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames():
    """Función para capturar video y realizar reconocimiento facial."""
    video_capture = cv2.VideoCapture(0)

    while True:
        success, frame = video_capture.read()
        if not success:
            break

        # Convertir la imagen a RGB (face_recognition usa RGB)
        rgb_frame = frame[:, :, ::-1]

        # Detectar caras y generar codificaciones
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Desconocido"

            # Verificar si hay coincidencia
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Dibujar un rectángulo alrededor de la cara
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            # Agregar el nombre debajo del rectángulo
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Transmitir la imagen a la página web
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    video_capture.release()
