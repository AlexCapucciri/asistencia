# Usa una imagen base de Python
FROM python:3.12

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de la app al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que corre la app
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    python3-dev \
    libmariadb-dev

RUN apt-get update && apt-get install -y libmariadb-dev
    # Usa una imagen base con Python
FROM python:3.12-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
    
RUN apt-get update && apt-get install -y pkg-config libmariadb-dev
# Crea y activa un entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copia el código al contenedor
WORKDIR /app
COPY . .

# Instala las dependencias del proyecto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto de la aplicación (ajusta según tu framework)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
