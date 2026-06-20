import json
import requests

# Deshabilitar advertencias de certificados SSL no verificados
requests.packages.urllib3.disable_warnings()

# 1. URL apuntando específicamente a la interfaz Loopback1
api_url = "https://192.168.56.102/restconf/data/ietf-interfaces:interfaces/interface=Loopback1"

# 2. Cabeceras requeridas para RESTCONF usando formato YANG-JSON
headers = { 
    "Accept": "application/yang-data+json",
    "Content-type": "application/yang-data+json"
}

# 3. Credenciales de tu entorno DEVASC (según tus scripts, usuario 'cisco')
basicauth = ("cisco", "cisco123!")

# 4. Estructura YANG para la Loopback1
# "enabled": False -> Apaga la interfaz (Equivalente a 'shutdown')
# "netmask": "255.255.255.255" -> Equivale al prefijo /32
yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback1",
        "description": "Interfaz Loopback 1 - Requerimiento DEVASC",
        "type": "iana-if-type:softwareLoopback",
        "enabled": False,  
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "1.1.1.1",
                    "netmask": "255.255.255.255" 
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}

print("Enviando petición RESTCONF para crear y apagar Loopback1...")

# 5. Realizar la petición PUT (crea la interfaz si no existe o la reemplaza)
resp = requests.put(
    api_url, 
    data=json.dumps(yangConfig), 
    auth=basicauth,
    headers=headers, 
    verify=False
)

# 6. Validar la respuesta del servidor
# El protocolo RESTCONF suele responder con 201 (Created) o 204 (No Content) si todo sale bien
if 200 <= resp.status_code <= 299:
    print("STATUS OK: {}".format(resp.status_code))
    print("La interfaz Loopback1 se ha configurado y está APAGADA de manera exitosa.")
else:
    print('Error. Status Code: {}'.format(resp.status_code))
    try:
        print('Error message:\n', json.dumps(resp.json(), indent=4))
    except Exception:
        print('No se recibió un mensaje JSON detallado de error.')