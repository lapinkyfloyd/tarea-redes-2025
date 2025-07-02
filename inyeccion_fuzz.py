
from scapy.all import IP, TCP, Raw, send
import random
import time

ip_destino = "172.18.0.3"
puerto_destino = 3306

print("Enviando paquetes de fuzzing...")
for i in range(2):
    carga_falsa = "@@@FAKE_SQL_COMMAND@@@"
    paquete = IP(dst=ip_destino)/TCP(dport=puerto_destino, sport=random.randint(1024,65535))/Raw(load=carga_falsa)
    send(paquete)
    print(".\nSent 1 packets.")
    time.sleep(1)

print("Paquetes enviados.")
