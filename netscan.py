from scapy.all import ARP, Ether, srp
import datetime
import speedtest
import pytz
import json
from pymongo import MongoClient

# Función para obtener la fecha y hora actual en la Ciudad de México
def get_current_datetime():
    mexico_tz = pytz.timezone('America/Mexico_City')
    return datetime.datetime.now(mexico_tz)

# Función para formatear la fecha y hora actual
def format_datetime():
    current_datetime = get_current_datetime()
    formatted_datetime = current_datetime.strftime('%Y%m%d_%H%M')
    return formatted_datetime

# Función para escanear la red y guardar en un archivo JSON y en la base de datos MongoDB
def scan_and_save(ip_range):
    # Crear el paquete ARP
    arp_request = ARP(pdst=ip_range)

    # Crear el paquete Ether para la capa 2
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    # Combinar ambos paquetes
    packet = ether/arp_request

    # Enviar y recibir paquetes
    result = srp(packet, timeout=3, verbose=0)[0]

    # Lista para almacenar direcciones IP y MAC
    devices_list = []

    for sent, received in result:
        devices_list.append({'ip': received.psrc, 'mac': received.hwsrc})

    # Medir el ancho de banda
    st = speedtest.Speedtest()
    download_speed = round(st.download() / 1e6, 2)  # Convertir a megabits
    upload_speed = round(st.upload() / 1e6, 2)  # Convertir a megabits

    # Obtener la fecha y hora actual en la Ciudad de México
    current_datetime = get_current_datetime()

    # Crear estructura de datos similar al proporcionado

    data_list = []

    for device in devices_list:
        data_list.append({
            'Fecha': current_datetime.strftime('%Y-%m-%d'),
            'Hora': current_datetime.strftime('%H:%M:%S'),
            'IP': device['ip'],
            'MAC': device['mac'],
            'Ancho de Banda': {
                'Descarga': download_speed,
                'Carga': upload_speed
            }
        })

    # Crear el nombre del archivo JSON con la fecha, hora y minutos
    output_file = f"json_casa/datos_red_{format_datetime()}.json"

        # Guardar en un archivo JSON
    with open(output_file, 'w') as json_file:
        json.dump(data_list, json_file, indent=2)

    print(f"Datos guardados en {output_file}.")

    # Conectar a la base de datos MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['NetScanBUAP']
    collection = db['fcc']

        # Insertar los datos en la base de datos
    try:
        collection.insert_many(data_list)
        print("Datos insertados en la base de datos MongoDB.")
    except Exception as e:
        print(f"Error al insertar datos en MongoDB: {e}")
# Especifica la IP o rango de IPs de tu red
ip_range = "172.31.0.0/20"

# Llama a la función para escanear y guardar en el archivo JSON y en la base de datos MongoDB
scan_and_save(ip_range)
