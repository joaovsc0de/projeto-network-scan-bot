
import telebot

from scanner.nmap_scanner import scan_rede
from scanner.parser import parse_scan
from monitor.monitor_rede import registrar_dispositivos
from database.Network_db import listar_dispositivos, listar_dispositivos_conectados, resetar_conexoes
from utils.network_utils import get_rede_atual
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=["scan"])
def scan(msg):

    resetar_conexoes()

    args = msg.text.split()

    network = None
    tipo = "basico"

    # 🔹 Interpretar argumentos
    if len(args) > 1:
        if "/" in args[1]:  # é rede
            network = args[1]

            if len(args) > 2:
                tipo = args[2]
        else:
            tipo = args[1]

    if not network:
        network = get_rede_atual()

    if not network:
        bot.reply_to(msg, "Não foi possível detectar a rede automaticamente.")
        return

    bot.reply_to(msg, f"Escaneando rede: {network} (modo: {tipo})...")

    # 🔥 chama scan com tipo
    saida = scan_rede(network, tipo)

    dispositivos = parse_scan(saida)

    registrar_dispositivos(dispositivos)

    bot.reply_to(
        msg,
        f"Scan finalizado\nDispositivos encontrados: {len(dispositivos)}"
    )

bot.infinity_polling()