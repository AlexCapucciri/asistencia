from flask import Flask, jsonify

app = Flask(__name__)

# Datos simulados (puedes reemplazarlos por datos de tu base de datos más adelante)
estudiantes = [
    {
        "apellidos": "Perez Lopez",
        "Nombres": "Juan",
        "curso": "1ro A",
        "materia": "Matematicas"
    },
    {
        "apellidos": "Cardozo Fuentes",
        "Nombres": "Dayana",
        "curso": "5to B",
        "materia": "Historia"
    }
]

@app.route('/api/estudiantes', methods=['GET'])
def obtener_estudiantes():
    return jsonify(estudiantes)

if __name__ == '__main__':
    app.run(debug=True)
