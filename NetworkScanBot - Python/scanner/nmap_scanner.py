import subprocess
import config

def scan_rede():
    resultado = subprocess.run(
        [config.NMAP_PATH, "-sn", "-PR", config.NETWORK],
        capture_output=True,
        text=True
    )

    return resultado.stdout