
from scapy.all import sniff, IP, TCP, Raw

def mostrar_paquete(pkt):
    if pkt.haslayer(Raw):
        print(pkt.summary())

print("Escuchando tráfico MySQL en puerto 3306...")
sniff(filter="tcp port 3306", prn=mostrar_paquete)
