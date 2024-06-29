#!/usr/bin/python3
#Author: TLuisillo_o

import sys
import signal

# Definición de colores
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"

def def_handler(sig, frame):
    print(f"\n\n{RED}[!] Saliendo...{RESET}\n")
    sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT, def_handler)

def validar_ip(ip):
    if '/' in ip:
        partes = ip.split('/')
        if len(partes) != 2:
            return False
        ip = partes[0]
        try:
            cidr = int(partes[1])
            if cidr < 0 or cidr > 32:
                return False
        except ValueError:
            return False

    partes_ip = ip.split('.')
    if len(partes_ip) != 4:
        return False
    
    for parte in partes_ip:
        try:
            num = int(parte)
            if num < 0 or num > 255:
                return False
        except ValueError:
            return False
    
    return True

def obtener_clase(ip):
    primer_octeto = int(ip.split('.')[0])
    if 1 <= primer_octeto <= 126:
        return 'A'
    elif 128 <= primer_octeto <= 191:
        return 'B'
    elif 192 <= primer_octeto <= 223:
        return 'C'
    else:
        return 'Desconocida'

def calcular_info_red(ip, cidr):
    ip_parts = list(map(int, ip.split('.')))
    bin_ip = ''.join(f'{part:08b}' for part in ip_parts)
    network_bin = bin_ip[:cidr] + '0' * (32 - cidr)
    broadcast_bin = bin_ip[:cidr] + '1' * (32 - cidr)

    network_ip = '.'.join(str(int(network_bin[i:i+8], 2)) for i in range(0, 32, 8))
    broadcast_ip = '.'.join(str(int(broadcast_bin[i:i+8], 2)) for i in range(0, 32, 8))

    wildcard = '.'.join(str(255 - int(network_bin[i:i+8], 2)) for i in range(0, 32, 8))

    netmask_bin = '1' * cidr + '0' * (32 - cidr)
    netmask = '.'.join(str(int(netmask_bin[i:i+8], 2)) for i in range(0, 32, 8))

    if cidr < 31:
        host_min_bin = network_bin[:31] + '1'
        host_max_bin = broadcast_bin[:31] + '0'
        host_min_ip = '.'.join(str(int(host_min_bin[i:i+8], 2)) for i in range(0, 32, 8))
        host_max_ip = '.'.join(str(int(host_max_bin[i:i+8], 2)) for i in range(0, 32, 8))
        num_hosts = (2 ** (32 - cidr)) - 2
    else:
        host_min_ip = "N/A"
        host_max_ip = "N/A"
        num_hosts = 0

    return {
        "Address": ip,
        "Netmask": netmask,
        "Class": obtener_clase(ip),
        "Network": f"{network_ip}/{cidr}",
        "Broadcast": broadcast_ip,
        "HostMin": host_min_ip,
        "HostMax": host_max_ip,
        "Hosts/Net": num_hosts
    }

def main():
    if len(sys.argv) != 2:
        print(f"{YELLOW}\n[!] Uso: python3 netinfo.py <IP/CIDR>{RESET}")
        sys.exit(1)
    
    ip_cidr = sys.argv[1]
    
    if '/' in ip_cidr:
        ip, cidr = ip_cidr.split('/')
        cidr = int(cidr)
    else:
        ip = ip_cidr
        cidr = 24  # Default CIDR

    if not validar_ip(f"{ip}/{cidr}"):
        print(f"\n{RED}[!] IP introducida no válida: {ip_cidr}{RESET}")
        sys.exit(1)

    info_red = calcular_info_red(ip, cidr)

    print(f"\n{GREEN}[+] IP introducida válida: {ip_cidr}{RESET}")
    print(f"\n{BLUE}Información de la red:{RESET}")
    for key, value in info_red.items():
        print(f"{MAGENTA}{key}: {RESET}{value}")

if __name__ == '__main__':
    main()
