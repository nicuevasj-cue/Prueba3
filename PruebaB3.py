import json
import requests

# Deshabilitar advertencias de certificados SSL
requests.packages.urllib3.disable_warnings()

# Datos de conexión (IP 192.168.56.102)
router_ip = "192.168.56.102"
api_url = f"https://{router_ip}/restconf/data/Cisco-IOS-XE-native:native/ip/access-list/extended=PERMIT_DEVASC"

headers = {
    "Accept": "application/yang-data+json",
    "Content-type": "application/yang-data+json"
}
basicauth = ("cisco", "cisco123!")

# ESTRUCTURA CORREGIDA (Modelo Nativo Aplanado):
# 1. Se usa 'dst-eq' directamente en lugar de anidar 'dst-port'.
# 2. Se eliminan tildes en las descripciones para evitar errores de escritura (DMI).
yangConfig = {
    "Cisco-IOS-XE-acl:extended": {
        "name": "PERMIT_DEVASC",
        "access-list-seq-rule": [
            {
                "sequence": "10",
                "ace-rule": {
                    "action": "permit",
                    "protocol": "tcp",
                    "ipv4-address": "192.168.56.0",
                    "mask": "0.0.0.255",
                    "dst-any": [None],
                    "dst-eq": "22"
                }
            },
            {
                "sequence": "20",
                "ace-rule": {
                    "action": "permit",
                    "protocol": "tcp",
                    "ipv4-address": "192.168.56.0",
                    "mask": "0.0.0.255",
                    "dst-any": [None],
                    "dst-eq": "830"
                }
            },
            {
                "sequence": "30",
                "ace-rule": {
                    "action": "permit",
                    "protocol": "tcp",
                    "ipv4-address": "192.168.56.0",
                    "mask": "0.0.0.255",
                    "dst-any": [None],
                    "dst-eq": "443"
                }
            }
        ]
    }
}

try:
    resp = requests.put(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
    )

    if resp.status_code >= 200 and resp.status_code <= 299:
        print(f"ÉXITO: ACL 'PERMIT_DEVASC' creada. Status: {resp.status_code}")
    else:
        print(f"Error {resp.status_code}: {resp.text}")

except Exception as e:
    print(f"Error de conexión: {e}")