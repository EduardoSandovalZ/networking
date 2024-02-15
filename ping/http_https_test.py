import requests

def probar_conexion(url, protocolo):
  """
  Prueba la conexión a una URL/IP usando el protocolo especificado.
  Args:
    url: La URL a la que se desea conectar, se puede usar tambien la IP.
    protocolo: El protocolo a usar, "http" o "https".
  Returns:
    True si la conexión se pudo realizar, False en caso contrario.
  """
  try:
    if protocolo == "http":
      respuesta = requests.get('http://'+url)
    elif protocolo == "https":
      respuesta = requests.get('http://'+url, verify=False)
    else:
      raise ValueError("Protocolo no válido")
    return respuesta.status_code == 200
  except requests.exceptions.ConnectionError:
    return False

# Ejemplo de uso de url
# urls = [
#   "https://www.google.com",
#   "https://www.facebook.com",
#   "https://www.twitter.com",
#   "https://www.youtube.com",
#   "https://www.wikipedia.org",
# ]
# Ejemplo de uso de ip
urls = ['148.228.16.1', '148.228.16.2', '148.228.16.3', '148.228.16.4', '148.228.16.7', '148.228.16.9', 
        '148.228.16.11', '148.228.16.14', '148.228.16.19', '148.228.16.24', '148.228.16.26', '148.228.16.27', 
        '148.228.16.28', '148.228.16.50', '148.228.16.51', '148.228.16.52', '148.228.16.54'
]
for url in urls:
  print(f"Probando conexión a {url}:")
  if probar_conexion(url, "https"):
    print("  - Conexión exitosa")
  else:
    print("  - Error de conexión")
