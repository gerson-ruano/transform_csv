import pandas as pd
from dateutil import parser
from datetime import datetime

def limpiar_dataframe(df, valor_defecto="null", columnas_ignoradas=['nip_responsable','edades']):
    """
    Limpieza general del DataFrame
    Permite excluir columnas específicas de la limpieza.
    """
    if columnas_ignoradas is None:
        columnas_ignoradas = []

    # Eliminar filas completamente vacías
    df = df.dropna(how='all')

    # Rellenar NaN/None con valor por defecto
    df = df.fillna(valor_defecto)

    # Limpiar solo columnas de texto (excepto las ignoradas)
    for col in df.select_dtypes(include=['object']).columns:
        if col in columnas_ignoradas:
            continue
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace(['nan', 'NaN', 'None'], valor_defecto)

    return df

def formatear_fecha_especifica(valor):
    """
    Convierte cualquier valor de fecha/hora a DD/MM/YYYY HH:MM
    """
    if pd.isna(valor) or str(valor).strip() in ['', 'NaN', 'None']:
        return ''

    valor_str = str(valor).strip()

     # Intentar parsear con dateutil
    try:
        fecha_obj = parser.parse(valor_str, dayfirst=True)

        # Si la hora es 00:00 → devolver solo la fecha
        if fecha_obj.hour == 0 and fecha_obj.minute == 0 and fecha_obj.second == 0:
            return fecha_obj.strftime('%d/%m/%Y')
        else:
            return fecha_obj.strftime('%d/%m/%Y %H:%M')

    except (ValueError, OverflowError):
        pass

    # Intentar convertir timestamp UNIX
    try:
        timestamp = float(valor_str)
        if 1000000000 < timestamp < 2000000000:  # rango UNIX válido
            fecha_obj = datetime.fromtimestamp(timestamp)
            if fecha_obj.hour == 0 and fecha_obj.minute == 0:
                return fecha_obj.strftime('%d/%m/%Y')
            else:
                return fecha_obj.strftime('%d/%m/%Y %H:%M')
    except:
        pass

    # Si no es fecha, devolver como string
    return valor_str
