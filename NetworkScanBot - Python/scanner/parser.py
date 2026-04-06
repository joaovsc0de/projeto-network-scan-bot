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

        portas = []

        for linha in linhas:
            # Ex: 22/tcp open ssh OpenSSH 8.2
            match_porta = re.match(
                r"(\d+)\/(tcp|udp)\s+(open|closed|filtered)\s+([\w\-\?]+)\s*(.*)",
                linha
            )

            if match_porta:
                porta = int(match_porta.group(1))
                protocolo = match_porta.group(2)
                estado = match_porta.group(3)
                servico = match_porta.group(4)
                versao = match_porta.group(5).strip()

                portas.append({
                    "porta": porta,
                    "protocolo": protocolo,
                    "estado": estado,
                    "servico": servico,
                    "versao": versao if versao else None
                })

        dispositivos.append({
            "ip": ip,
            "mac": mac,
            "fabricante": fabricante,
            "portas": portas
        })

    return dispositivos