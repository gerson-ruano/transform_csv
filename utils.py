import os

def carpeta_valida(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"La carpeta no existe: {path}")
    return path
