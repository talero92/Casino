import json
import os

def guardar_usuario(usuario):
    """Guarda los datos del usuario en un archivo JSON"""
    # Obtener la ruta base del proyecto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    usuarios_dir = os.path.join(data_dir, 'usuarios')
    
    # Crear directorios si no existen
    try:
        if not os.path.exists(usuarios_dir):
            os.makedirs(usuarios_dir)
    except Exception as e:
        print(f"Error al crear directorio: {e}")
        # Intentar usar el directorio actual como fallback
        usuarios_dir = 'usuarios'
        if not os.path.exists(usuarios_dir):
            os.makedirs(usuarios_dir)
    
    # Construir la ruta del archivo
    ruta_archivo = os.path.join(usuarios_dir, f'{usuario.nombre}.json')
    
    try:
        with open(ruta_archivo, 'w') as f:
            json.dump(usuario.to_dict(), f, indent=4)
        return True
    except Exception as e:
        print(f"Error al guardar usuario: {e}")
        return False

def cargar_usuario(nombre):
    """Carga los datos del usuario desde un archivo JSON"""
    # Obtener la ruta base del proyecto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    usuarios_dir = os.path.join(base_dir, 'data', 'usuarios')
    
    # Si no existe el directorio principal, intentar con el directorio actual
    if not os.path.exists(usuarios_dir):
        usuarios_dir = 'usuarios'
    
    ruta_archivo = os.path.join(usuarios_dir, f'{nombre}.json')
    
    try:
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, 'r') as f:
                datos = json.load(f)
                from .usuarios import Usuario
                return Usuario.from_dict(datos)
        return None
    except Exception as e:
        print(f"Error al cargar usuario: {e}")
        return None