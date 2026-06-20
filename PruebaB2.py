import json
import requests

requests.packages.urllib3.disable_warnings()

# 1. URL hacia la raíz nativa de configuración del router
api_url = "https://192.168.56.102/restconf/data/Cisco-IOS-XE-native:native"

headers = { 
    "Accept": "application/yang-data+json",
    "Content-type": "application/yang-data+json"
}

basicauth = ("cisco", "cisco123!")

# 2. Estructura YANG para modificar las líneas VTY 0 a 4 y de 5 a 15
# Colocamos "ssh" en 'transport/input/none/vty' para deshabilitar Telnet
yangConfig = {
    "Cisco-IOS-XE-native:native": {
        "line": {
            "vty": [
                {
                    "first": 0,
                    "last": 4,
                    "transport": {
                        "input": {
                            "input": [
                                "ssh"
                            ]
                        }
                    }
                },
                {
                    "first": 5,
                    "last": 15,
                    "transport": {
                        "input": {
                            "input": [
                                "ssh"
                            ]
                        }
                    }
                }
            ]
        }
    }
}

print("Enviando petición PATCH para deshabilitar Telnet en las líneas VTY...")

# 3. Envío de la petición PATCH
resp = requests.patch(
    api_url, 
    data=json.dumps(yangConfig), 
    auth=basicauth,
    headers=headers, 
    verify=False
)

if 200 <= resp.status_code <= 299:
    print("STATUS OK: {}".format(resp.status_code))
    print("¡Logrado! Acceso por Telnet deshabilitado (Solo SSH permitido).")
else:
    print('Error. Status Code: {}'.format(resp.status_code))
    try:
        print('Error message:\n', json.dumps(resp.json(), indent=4))
    except Exception:
        print('No se recibió un mensaje JSON de error.')