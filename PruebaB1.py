import json
import requests

requests.packages.urllib3.disable_warnings()

api_url = "https://192.168.56.102/restconf/data/Cisco-IOS-XE-native:native"

headers = { 
    "Accept": "application/yang-data+json",
    "Content-type": "application/yang-data+json"
}

basicauth = ("cisco", "cisco123!")

yangConfig = {
    "Cisco-IOS-XE-native:native": {
        "router": {
            "Cisco-IOS-XE-ospf:ospf": [
                {
                    "id": 10,
                    "network": [
                        {
                            "ip": "192.168.56.0",
                            "mask": "0.0.0.255",
                            "area": 0
                        },
                        {
                            "ip": "1.1.1.1",
                            "mask": "0.0.0.0",
                            "area": 0
                        }
                    ],
                    "passive-interface": {
                        "interface": [
                            "Loopback1" 
                        ]
                    }
                }
            ]
        }
    }
}

print("Enviando petición PATCH corregida para OSPF 10...")

resp = requests.patch(
    api_url, 
    data=json.dumps(yangConfig), 
    auth=basicauth,
    headers=headers, 
    verify=False
)

if 200 <= resp.status_code <= 299:
    print("STATUS OK: {}".format(resp.status_code))
    print("¡Logrado! OSPF 10 configurado con éxito.")
else:
    print('Error. Status Code: {}'.format(resp.status_code))
    try:
        print('Error message:\n', json.dumps(resp.json(), indent=4))
    except Exception:
        print('No se recibió un mensaje JSON de error.')
