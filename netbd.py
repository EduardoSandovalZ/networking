import json
import re
from pymongo import MongoClient

# Nombre del archivo de entrada y salida
#archivo_entrada = 'datos/datos_red4.txt'
#archivo_entrada = 'datos/datos_red5.txt'
#archivo_entrada = 'datos/datos_red6.txt'
archivo_entrada = 'datos_red7.txt'
archivo_salida = 'datos8.json'

# Lista para almacenar los datos
datos = []

# Leer el archivo.txt y procesar cada línea
with open(archivo_entrada, 'r') as file:
    fecha = None
    hora = None
    for line in file:
        # Buscar la línea que contiene la fecha y hora
        if line.startswith('Fecha:'):
            fecha_hora = line.strip()[7:26]  # Extraer la fecha y hora
            fecha, hora = fecha_hora.split()  # Separar fecha y hora
            continue

        match = re.match(r'IP: (\d+\.\d+\.\d+\.\d+)\s+MAC: ([\da-fA-F:]+)\s+Ancho de Banda: Descarga - (\d+\.\d+) Mbps, Carga - (\d+\.\d+) Mbps', line)
        if match:
            ip, mac, descarga, carga = match.groups()
            descarga = float(descarga)
            carga = float(carga)

            # Agregar datos a la lista con la fecha y hora separadas
            datos.append({
                'Fecha': fecha,
                'Hora': hora,
                'IP': ip,
                'MAC': mac,
                'Ancho de Banda': {
                    'Descarga': descarga,
                    'Carga': carga
                }
            })

# Imprimir datos antes de insertar
#print(datos)

# Escribir datos en formato JSON en el archivo de salida
with open(archivo_salida, 'w') as json_file:
    json.dump(datos, json_file, indent=2)

print(f"Se ha creado el archivo {archivo_salida}.")

# Conectarse a la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NetScanBUAP']
collection = db['fcc']

# Verificar la conexión
print(client.list_database_names())  # Deberías ver 'Testing' en la salida

# Leer el archivo JSON de salida
with open(archivo_salida, 'r') as json_file:
    data = json.load(json_file)

# Insertar los datos en la base de datos
try:
    collection.insert_many(data)
    print("Datos insertados en la base de datos MongoDB.")
except Exception as e:
    print(f"Error al insertar datos en MongoDB: {e}")
