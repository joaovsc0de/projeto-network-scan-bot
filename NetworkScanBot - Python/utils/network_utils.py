import socket

def get_rede_atual():
    try:
        # método mais confiável
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()

        base = ".".join(ip.split(".")[:3])
        return base + ".0/24"

    except Exception:
        return None