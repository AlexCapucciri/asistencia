from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "¡La app funciona en Railway!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Usa el puerto de Railway o 8080 por defecto
    app.run(host='0.0.0.0', port=port)