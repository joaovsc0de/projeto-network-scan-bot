import subprocess
import config

def scan_rede(network=None, tipo="basico"):

    if not network:
        network = config.NETWORK

    if tipo == "basico":
        comando = [config.NMAP_PATH, "-sn", "-PR", network]

    elif tipo == "portas":
        comando = [config.NMAP_PATH, "-p-", network]

    elif tipo == "servicos":
        comando = [config.NMAP_PATH, "-sV", "-p-", network]

    elif tipo == "agressivo":
        comando = [config.NMAP_PATH, "-A", network]

    else:
        comando = [config.NMAP_PATH, network]

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True
    )

    return resultado.stdout