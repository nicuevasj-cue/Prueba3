from ncclient import manager
import xml.dom.minidom

# 1. Datos de conexión al Router CSR1000v
router = {
    "host": "192.168.56.102",
    "port": 830,                   # Puerto estándar de NETCONF
    "username": "cisco",
    "password": "cisco123!",
    "hostkey_verify": False
}

# 2. Configuración XML para cambiar el Hostname y crear la Loopback 2
# Nota: Reemplaza APELLIDO-APELLIDO con tus datos reales.
netconf_config = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    
    <hostname>APELLIDO-APELLIDO</hostname>
    
    <interface>
      <Loopback>
        <name>2</name>
        <ip>
          <address>
            <primary>
              <address>2.2.2.2</address>
              <mask>2.5.5.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>

  </native>
</config>
"""

print("Conectando al router mediante NETCONF en el puerto 830...")

try:
    # 3. Establecer la sesión NETCONF de forma segura
    with manager.connect(**router) as m:
        print("¡Conexión SSH NETCONF establecida con éxito!")
        print("Enviando configuración (Cambio de Hostname y Loopback 2)...")
        
        # 4. Enviar la configuración al running-config
        response = m.edit_config(target='running-config', config=netconf_config)
        
        # 5. Validar si el router aceptó los cambios
        if "<ok/>" in str(response):
            print("\n--------------------------------------------------")
            print("STATUS: ¡ÉXITO! (Se recibió la etiqueta <ok/>)")
            print("El Hostname se cambió y la Loopback 2 fue creada.")
            print("--------------------------------------------------")
        else:
            print("Hubo un problema con la configuración:")
            print(xml.dom.minidom.parseString(response.xml).toprettyxml())

except Exception as e:
    print(f"Error al conectar o configurar el dispositivo: {e}")