from waitress import serve
from app import app  # Importa tu aplicación Flask

# Inicia el servidor Waitress
serve(app, host='0.0.0.0', port=5000)