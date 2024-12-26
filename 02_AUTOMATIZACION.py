# Importacion de Librerias
import sqlite3
import pandas as pd
import os 
import win32com.client as win32


#------------------ Conexión a base de datos y su respectiva obtención -----------------------#
# Función para obtener tablas y sus datos
def obtener_tablas_y_datos(conn):
    """
    Recupera todas las tablas de una base de datos SQLite y sus respectivos datos.

    Esta función ejecuta una consulta para obtener los nombres de todas las tablas
    en la base de datos y luego realiza una consulta SELECT sobre cada tabla para
    recuperar todos sus datos. Los resultados se devuelven en forma de un diccionario,
    donde las claves son los nombres de las tablas y los valores son DataFrames de pandas
    con el contenido de cada tabla.

    Parámetros:
    conn : sqlite3.Connection
        Objeto de conexión a la base de datos SQLite.

    Retorna:
    dict
        Un diccionario donde las claves son los nombres de las tablas y los valores
        son DataFrames que contienen los datos de cada tabla.
    """

    tablas_query = "SELECT name FROM sqlite_master WHERE type='table';"
    tablas = pd.read_sql_query(tablas_query, conn)['name'].tolist()
    dbs = {tabla: pd.read_sql_query(f"SELECT * FROM {tabla};", conn) for tabla in tablas}
    return dbs

# Conectar a las bases de datos
with sqlite3.connect('database.sqlite') as conn1, sqlite3.connect('database_contratos.sqlite') as conn2:
    # Obtener datos de cada base de datos
    db1 = obtener_tablas_y_datos(conn1)
    db2 = obtener_tablas_y_datos(conn2)


#Conversión de las bases de datos al formato DataFrame
db_apicall = pd.DataFrame(db1['apicall'])
db_commerce = pd.DataFrame(db1['commerce'])
db_contratos = pd.DataFrame(db2['contract'])

#Unión de la tabla apicall y commerce
db_completa = pd.merge(db_apicall,db_commerce,on='commerce_id')
#Conversión a tipo de fecha datetime
db_completa['date_api_call']  = pd.to_datetime(db_completa['date_api_call'])
#Filtro inicial : Extraer solo los comercios con estado activo
db_completa = db_completa[db_completa['commerce_status'] == 'Active']

#-----------------------------------------------------------------------------------------------------------#
#----------------------Creación Funciones principales-------------------------------------------------------#

def creacion_factura_mes_año(db_datos, db_contrato, mes,año):
    """
    Genera un DataFrame de facturación de comisiones mensual para comercios basado en las peticiones exitosas y no exitosas.

    Esta función toma como entrada bases de datos con información de peticiones de comercios, información básica de cada comercio
    y contratos, filtra los datos del mes y año especificados, calcula la comisión a cobrar para cada comercio y aplica descuentos 
    según el tipo de contrato y el número de peticiones no exitosas.

    Parámetros:
        db_datos (pd.DataFrame): DataFrame con los datos de peticiones y la información básica de los comercios,
        incluyendo la fecha ('date_api_call') y el estado de la petición ('ask_status').
        db_contrato (pd.DataFrame): DataFrame con los contratos asociados a cada comercio, indicando el tipo de 
                                    contrato ('contract_type'), valores de comisión ('commission_value') y 
                                    rangos de descuento.
        mes (int): Mes para el que se generará la factura (1-12).
        año (int): Año para el que se generará la factura.

    Retorna:
        pd.DataFrame: DataFrame con las facturas generadas, que incluye columnas como:
                      'Fecha-Mes', 'Nombre', 'Nit', 'Valor_comision', 'Valor Descuento', 'Valor_iva', 
                      'Valor_Total' y 'Correo'.
    """

    db_comission = []
    db_datos = db_datos.loc[(db_datos['date_api_call'].dt.year == año)& (db_datos['date_api_call'].dt.month == mes)]
    agrupacion = db_datos.groupby(['commerce_id', 'ask_status']).size().unstack(fill_value=0)
    for i in range(0,len(agrupacion)):
        name = agrupacion.iloc[i].name
        comercio_especifico = db_commerce[db_commerce['commerce_id'] == name] # base de datos commerce filtrado al comercio según iteración
        contrato_especifico = db_contrato[db_contrato['commerce_id'] == name] # base de datos contratos filtrado al comercio según iteración
        #Creación de las variables asociadas al numero total de peticiones exitosas y no exitosas
        exitosas = agrupacion.iloc[i].loc['Successful']
        no_exitosas = agrupacion.iloc[i].loc['Unsuccessful']
        if contrato_especifico['contract_type'].iloc[0] == 'Fijo':  # Evaluación del caso donde el contrato es fijo
            # calculo del valor total comision 
            valor_total_comision = contrato_especifico['commission_value'].iloc[0] * exitosas
            # Encontrar el rango correcto de descuento según la cantidad de peticiones no exitosas
            '''
            Filtro de contrato especifico esta evaluando si el numero de peticiones no existosas esta en los rangos de [numero,NaN]
            o [numero1,numero2] donde NaN se considera que no hay limite superior.
            '''
            descuento_idx = contrato_especifico[(contrato_especifico['discount_available'] == 1) &
                                                (no_exitosas >= contrato_especifico['unsuccessful_requests_start_range']) &
                                                ((contrato_especifico['unsuccessful_requests_end_range'].isna()) |
                                                 (no_exitosas <= contrato_especifico['unsuccessful_requests_end_range']))].index
            
            if len(descuento_idx) > 0:
                descuento = contrato_especifico.loc[descuento_idx[0],'discount_value']
                valor_total_comision -= descuento * valor_total_comision # aplicando descuento
            else:
                descuento = 0
            
        else:  # Evaluación del caso donde : El contrato es  Variable
            '''
            Filtro de contrato especifico esta evaluando si el numero de peticiones existosas esta en los rangos de [numero,NaN]
            o [numero1,numero2] donde NaN se considera que no hay limite superior.
            '''
            idx = contrato_especifico[(exitosas >= contrato_especifico['successful_requests_start_range'] ) &
                                      ((exitosas <= contrato_especifico['successful_requests_end_range']) |
                                       (contrato_especifico['successful_requests_end_range'].isna()))].index
            
            if len(idx) > 0:
                '''
                Filtro de contrato especifico esta evaluando si el numero de peticiones no existosas esta en los rangos de [numero,NaN]
                o [numero1,numero2] donde NaN se considera que no hay limite superior.
                '''
                valor_total_comision =  contrato_especifico.loc[idx[0], 'commission_value'] * exitosas
                descuento_idx = contrato_especifico[(contrato_especifico['discount_available'] == 1) &
                                                    (no_exitosas >= contrato_especifico['unsuccessful_requests_start_range']) &
                                                    ((contrato_especifico['unsuccessful_requests_end_range'].isna()) |
                                                     (no_exitosas <= contrato_especifico['unsuccessful_requests_end_range']))].index
                
                if len(descuento_idx) > 0:
                    descuento = contrato_especifico.loc[descuento_idx[0], 'discount_value']
                    valor_total_comision -= descuento * valor_total_comision
                else:
                    descuento = 0
            else: 
                valor_total_comision = 0
            
        # Calculo del IVA correspondiente
        iva = contrato_especifico['iva_value'].iloc[0]
        valor_iva = valor_total_comision * iva
        valor_total = valor_total_comision + valor_iva
        # Agregar a la lista de resultados
        db_comission.append({
            'Fecha-Mes': f"{año}-{mes}",
            'Nombre': comercio_especifico['commerce_name'].iloc[0],
            'Nit': comercio_especifico['commerce_nit'].iloc[0],
            'Valor_comision': valor_total_comision,
            'Valor Descuento': descuento,
            'Valor_iva': valor_iva,
            'Valor_Total': valor_total,
            'Correo': comercio_especifico['commerce_email'].iloc[0]
        })
    # Crear DataFrame con resultados
    factura = pd.DataFrame(db_comission)
    return factura


def programa_factura(db_datos, db_contrato, mes_inicio, mes_final, año):
    """
    Genera un DataFrame de facturación de comisiones para un rango de meses dentro de un año especificado.

    La función recorre los meses desde el mes de inicio hasta el mes final, generando una factura
    para cada mes y concatenándolas en un único DataFrame.

    Parámetros:
        db_datos (pd.DataFrame): DataFrame con los datos de peticiones e información básica de los comercios.
        db_contrato (pd.DataFrame): DataFrame con los contratos asociados a los comercios.
        mes_inicio (int): Mes de inicio del rango (1-12).
        mes_final (int): Mes final del rango (1-12).
        año (int): Año para el que se generará la factura.

    Retorna:
        pd.DataFrame: DataFrame con todas las facturas generadas en el rango especificado.
    """
    facturas_totales = []

    for mes in range(mes_inicio, mes_final + 1):
        # Generar factura para cada mes
        factura_mes = creacion_factura_mes_año(db_datos, db_contrato, mes, año)
        facturas_totales.append(factura_mes)

    # Concatenar todas las facturas en un solo DataFrame
    facturas_completas = pd.concat(facturas_totales, ignore_index=True)
    return facturas_completas
#---------------------------------------------------- Fin funciones ----------------------------------------------------#

#-------------------------------------------------------Programa Principal ---------------------------------------------#
print("Bienvenid@ al programa donde podrás generar la factura de comisiones para el mes de julio y agosto del 2024")


factura_final = programa_factura(db_completa, db_contratos, 7, 8, 2024)
# Obtener los valores únicos de la columna 'Fecha-Mes'
valores_unicos = factura_final['Fecha-Mes'].unique()
# Convertir la lista de valores en un string, separados por comas
valores_como_string = ", ".join(map(str, valores_unicos))
# Ruta de destino (Carpeta actual)
nombre_archivo = f"Facturas_{valores_como_string}.xlsx"
ruta_completa = os.path.join(os.getcwd(), nombre_archivo)  # Guardar en el directorio actual
# Guardar las facturas en el archivo Excel en la ruta especificada
factura_final.to_excel(ruta_completa, index=False)
print(f"Archivo de facturas guardado como {ruta_completa}")

#---------------------------------------Envió de la factura a los destinarios -----------------------------------------------#

# Pedir al usuario el número de destinatarios
num_destinatarios = int(input("¿A cuántos destinatarios deseas enviarles el correo? (Escribe un número): "))

# Recopilación de los correos electrónicos
correos_destino = []
for i in range(num_destinatarios):
    correo = input(f"Ingrese el correo del destinatario {i + 1}: ")
    correos_destino.append(correo)

# Unión de los correos con "; " (Outlook requiere este formato para múltiples destinatarios)
correos_destino_str = "; ".join(correos_destino)

# Configuración del cliente de Outlook
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)

# Configuración del contenido del correo
mail.To = correos_destino_str
mail.Subject = f"Facturas de {valores_como_string}"
mail.Body = (
    f"Cordial saludo,\n\n"
    f"Espero que se encuentre bien.Adjunto encontrarás las facturas correspondientes al periodo de las fechas {valores_como_string}.\n\n"
    f"Gracias por su atención."
)

# Adjuntar el archivo desde la ruta completa
mail.Attachments.Add(ruta_completa)
# Enviar el correo
mail.Send()
print(f"Correo enviado a: {correos_destino_str}")