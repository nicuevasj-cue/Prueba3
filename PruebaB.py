import json
import requests

requests.packages.urllib3.disable_warnings()

api_url = "https://192.168.56.102/restconf/data/ietf-interfaces:interfaces/interface=Loopback1"

headers = { 
    "Accept": "application/yang-data+json",
    "Content-type": "application/yang-data+json"
}

basicauth = ("cisco", "cisco123!")


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

resp = requests.put(
    api_url, 
    data=json.dumps(yangConfig), 
    auth=basicauth,
    headers=headers, 
    verify=False
)

if 200 <= resp.status_code <= 299:
    print("STATUS OK: {}".format(resp.status_code))
    print("La interfaz Loopback1 se ha configurado y está APAGADA de manera exitosa.")
else:
    print('Error. Status Code: {}'.format(resp.status_code))
    try:
        print('Error message:\n', json.dumps(resp.json(), indent=4))
    except Exception:
        print('No se recibió un mensaje JSON detallado de error.')
