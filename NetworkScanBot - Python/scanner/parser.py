import re

def parse_scan(saida):

    dispositivos = []

    ips = re.findall(r"Nmap scan report for (.*)", saida)
    macs = re.findall(r"MAC Address: ([A-F0-9:]+) \((.*?)\)", saida)

    for i in range(len(macs)):

        dispositivos.append({
            "ip": ips[i],
            "mac": macs[i][0],
            "fabricante": macs[i][1]
            
        })
        
    return dispositivos