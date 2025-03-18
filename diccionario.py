from database import *

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
    
# Ejemplo de uso
if __name__ == "__main__":
    estudiantes_diccionario = guardar_estudiantes_en_diccionario()
    if estudiantes_diccionario:
        print("Estudiantes guardados en el diccionario:")
        for id_estudiante, datos in estudiantes_diccionario.items():
            print(f"ID: {id_estudiante}, Datos: {datos}")
