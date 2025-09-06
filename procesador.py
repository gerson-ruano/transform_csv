import os
import glob
import pandas as pd
from datetime import datetime
from limpieza import limpiar_dataframe, formatear_fecha_especifica
from formato import crear_excel_formato_especifico

def procesar_csv_a_excel(carpeta_entrada, carpeta_salida=None):
    if carpeta_salida is None:
        carpeta_salida = os.path.join(carpeta_entrada, 'EXCEL_PROCESADOS')
    os.makedirs(carpeta_salida, exist_ok=True)

    archivos_csv = glob.glob(os.path.join(carpeta_entrada, '*.csv'))
    if not archivos_csv:
        print("❌ No se encontraron archivos CSV en la carpeta especificada")
        return []

    print(f"📁 {len(archivos_csv)} archivos CSV Encontrados")
    print("=" * 60)

    archivos_procesados = []
    fecha_actual = datetime.now().strftime('%d-%m-%Y')

    for archivo in archivos_csv:
        nombre_archivo = os.path.basename(archivo)
        df_temp = pd.read_csv(archivo, delimiter=',', encoding='utf-8')
        # ================================
        # 🔹 Extravíos
        # ================================
        if 'no_extravio' in df_temp.columns or (
            'fh_ingreso' in df_temp.columns and 'correlativo_completo' not in df_temp.columns
        ):
            try:
                if 'fh_ingreso' in df_temp.columns:
                    fechas = pd.to_datetime(df_temp['fh_ingreso'], errors='coerce').dropna()
                    if not fechas.empty:
                        fecha_min = fechas.min().strftime('%d-%m-%Y')
                        fecha_max = fechas.max().strftime('%d-%m-%Y')
                        nombre_salida = f"extravios_ingresados_{fecha_min}_a_{fecha_max}"
                    else:
                        nombre_salida = f"extravios_ingresados_hasta_{fecha_actual}"
                else:
                    nombre_salida = f"extravios_ingresados_hasta_{fecha_actual}"
            except Exception as e:
                print(f"⚠️ Error al procesar fechas en extravíos: {e}")
                nombre_salida = f"extravios_ingresados_hasta_{fecha_actual}"

        # ================================
        # 🔹 Informes
        # ================================
        elif 'tipo_denuncia' in df_temp.columns:
            try:
                if 'fh_ingreso' in df_temp.columns:
                    fechas = pd.to_datetime(df_temp['fh_ingreso'], errors='coerce').dropna()
                    if not fechas.empty:
                        fecha_min = fechas.min().strftime('%d-%m-%Y')
                        fecha_max = fechas.max().strftime('%d-%m-%Y')
                        nombre_salida = f"informes_ingresados_{fecha_min}_a_{fecha_max}"
                    else:
                        nombre_salida = f"informes_ingresados_hasta_{fecha_actual}"
                else:
                    nombre_salida = f"informes_ingresados_hasta_{fecha_actual}"
            except Exception as e:
                print(f"⚠️ Error al procesar fechas en informes: {e}")
                nombre_salida = f"informes_ingresados_hasta_{fecha_actual}"

        # ================================
        # 🔹 Lesiones
        # ================================
        elif 'tipo_hecho' in df_temp.columns:
            #nombre_salida = f"lesiones_intensionales_hasta_{fecha_actual}"
            try:
                if 'fh_suceso' in df_temp.columns:
                    fechas = pd.to_datetime(df_temp['fh_suceso'], errors='coerce').dropna()
                    if not fechas.empty:
                        fecha_min = fechas.min().strftime('%d-%m-%Y')
                        fecha_max = fechas.max().strftime('%d-%m-%Y')
                        nombre_salida = f"lesiones_intensionales_{fecha_min}_a_{fecha_max}"
                    else:
                        nombre_salida = f"lesiones_intensionales_hasta_{fecha_actual}"
                else:
                    nombre_salida = f"lesiones_intensionales_hasta_{fecha_actual}"
            except Exception as e:
                print(f"⚠️ Error al procesar fechas en informes: {e}")
                nombre_salida = f"lesiones_intensionales_hasta_{fecha_actual}"

        # ================================
        # 🔹 Reportes POLCOM
        # ================================
        elif 'problematica' in df_temp.columns:
            #nombre_salida = f"reporte_POLCOM_hasta_{fecha_actual}"
            try:
                if 'fecha' in df_temp.columns:
                    fechas = pd.to_datetime(df_temp['fecha'], errors='coerce').dropna()
                    if not fechas.empty:
                        fecha_min = fechas.min().strftime('%d-%m-%Y')
                        fecha_max = fechas.max().strftime('%d-%m-%Y')
                        nombre_salida = f"reporte_polcom_{fecha_min}_a_{fecha_max}"
                    else:
                        nombre_salida = f"reporte_polcom_hasta_{fecha_actual}"
                else:
                    nombre_salida = f"reporte_polcom_hasta_{fecha_actual}"
            except Exception as e:
                print(f"⚠️ Error al procesar fechas en informes: {e}")
                nombre_salida = f"reporte_polcom_hasta_{fecha_actual}"

        # ================================
        # 🔹 Caso por defecto
        # ================================
        else:
            nombre_salida = os.path.splitext(nombre_archivo)[0] + "_PROCESADO"

        archivo_salida = os.path.join(carpeta_salida, f"{nombre_salida}.xlsx")

        print(f"🔄 Procesando: {nombre_archivo} → {os.path.basename(archivo_salida)}")
        try:
            convertir_csv_a_excel(archivo, archivo_salida)
            archivos_procesados.append(archivo_salida)
            print(f"✅ Convertido a Excel: {os.path.basename(archivo_salida)}")
        except Exception as e:
            print(f"❌ Error procesando {nombre_archivo}: {str(e)}")
        print("-" * 40)

    return archivos_procesados


def convertir_csv_a_excel(archivo_entrada, archivo_salida):
    for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
        try:
            df = pd.read_csv(archivo_entrada, delimiter=',', encoding=encoding)
            break
        except:
            continue
    else:
        raise ValueError("No se pudo leer el archivo con ningún encoding compatible")

    df.insert(0, 'no.', range(1, len(df) + 1))

    columnas_fecha = [col for col in df.columns if any(x in col.lower() 
                        for x in ['fecha', 'fh_suceso', 'fh_ingreso'])]
    print(f"🔍 Columnas de fecha detectadas: {columnas_fecha}")

    for columna in columnas_fecha:
        df[columna] = df[columna].apply(formatear_fecha_especifica)

    df = limpiar_dataframe(df)
    crear_excel_formato_especifico(df, archivo_salida)
