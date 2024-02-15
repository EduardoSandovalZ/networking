import os

resultados_positivos = []

ip_range = '148.228.16.'
num_paquetes = 2

for ip in range(255):
    #print(f'{ip_range + str(ip+1)}')
    respuesta = os.system(f'ping -n {num_paquetes} {ip_range + str(ip+1)}')
    # Si consigue hacer ping devuelve 0
    if respuesta == 0:
        resultados_positivos.append(ip_range + str(ip+1))
        print('Ping exitoso\n')
    else:
        print('Ping fallido\n')

print('\nRespondieron satisfactoriamente')
print(resultados_positivos)
