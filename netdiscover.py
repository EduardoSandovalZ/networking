from scapy.all import ARP, Ether, srp
import datetime
import speedtest
import pytz
import json
import re
from pymongo import MongoClient

# Función para obtener la fecha y hora actual en la Ciudad de México
def get_current_datetime():
    mexico_tz = pytz.timezone('America/Mexico_City')
    return datetime.datetime.now(mexico_tz)

# Función para escanear la red y guardar en un archivo de texto
def scan_and_save(ip_range, output_file):
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
    download_speed = st.download() / 1e6  # Convertir a megabits
    upload_speed = st.upload() / 1e6  # Convertir a megabits

    # Obtener la fecha y hora actual en la Ciudad de México
    current_datetime = get_current_datetime()

    # Guardar en un archivo de texto
    with open(output_file, 'a') as file:
        file.write(f"Fecha: {current_datetime.strftime('%Y-%m-%d %H:%M:%S.%f %z')}\n")
        for device in devices_list:
            file.write(f"IP: {device['ip']}\tMAC: {device['mac']}\tAncho de Banda: Descarga - {download_speed:.2f} Mbps, Carga - {upload_speed:.2f} Mbps\n")
        file.write("\n")

    print(f"Datos guardados en {output_file}.")

# Especifica la IP o rango de IPs de tu red
ip_range = "172.31.0.0/20"

# Especifica el nombre del archivo de texto
output_file = "datos_red7.txt"

# Llama a la función para escanear y guardar en el archivo de texto
scan_and_save(ip_range, output_file)