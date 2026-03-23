import re

def parse_scan(saida):

    dispositivos = []

    blocos = saida.split("Nmap scan report for ")

    for bloco in blocos[1:]:

        linhas = bloco.split("\n")
        ip = linhas[0].strip()

        mac_match = re.search(r"MAC Address: ([A-F0-9:]+) \((.*?)\)", bloco)

        if mac_match:
            mac = mac_match.group(1)
            fabricante = mac_match.group(2)
        else:
            mac = None
            fabricante = None

        dispositivos.append({
            "ip": ip,
            "mac": mac,
            "fabricante": fabricante
        })

    return dispositivos