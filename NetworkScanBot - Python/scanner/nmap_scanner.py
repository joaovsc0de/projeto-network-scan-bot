import subprocess
import config

def scan_rede(network=None):

    if not network:
        network = config.NETWORK

    resultado = subprocess.run(
        [config.NMAP_PATH, "-sn", "-PR", network],
        capture_output=True,
        text=True
    )

    return resultado.stdout