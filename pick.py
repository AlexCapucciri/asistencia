import face_recognition
import pickle

# Cargar imágenes conocidas
image_1 = face_recognition.load_image_file("static/faces/Alex.jpg")
image_2 = face_recognition.load_image_file("static/faces/Sheimi.jpg")

# Generar codificaciones
encoding_1 = face_recognition.face_encodings(image_1)[0]
encoding_2 = face_recognition.face_encodings(image_2)[0]

# Guardar las codificaciones y nombres
known_face_encodings = [encoding_1, encoding_2]
known_face_names = ["Alex Capussiri ", "Sheimi Peredo"]

# Guardar en un archivo para reutilizar
with open("face_data.pkl", "wb") as f:
    pickle.dump((known_face_encodings, known_face_names), f)
