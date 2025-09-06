import sys
import os
import io 
from procesador import procesar_csv_a_excel
from utils import carpeta_valida

# Forzar salida estándar a UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def ejecucion_automatica():
    #CARPETA_ENTRADA = Path.home() / "Documents" / "CSV"
    CARPETA_ENTRADA = os.path.join(os.path.expanduser("~"), "Documents", "CSV")
    
    # Crear carpeta si no existe
    if not os.path.exists(CARPETA_ENTRADA):
        os.makedirs(CARPETA_ENTRADA)
        print(f"📁 Carpeta creada: {CARPETA_ENTRADA}")
    
    # Validar la carpeta (ahora debería existir)
    CARPETA_VALIDADA = carpeta_valida(CARPETA_ENTRADA)

    print(f"⚡ Conversión automática en: {CARPETA_ENTRADA}")
    archivos = procesar_csv_a_excel(CARPETA_ENTRADA)
    print(f"✅ Se convirtieron {len(archivos)} archivos a Excel en: {CARPETA_ENTRADA}/EXCEL_PROCESADOS")

if __name__ == "__main__":
    ejecucion_automatica()
