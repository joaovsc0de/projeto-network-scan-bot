
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

    novos = registrar_dispositivos(dispositivos)
    

    bot.reply_to(
    msg,
    f"Scan finalizado\n"
    f"Dispositivos encontrados: {len(dispositivos)}\n"
    f"Novos dispositivos: {novos}"
)

@bot.message_handler(commands=["dispositivos"])
def listar(msg):

        dados = listar_dispositivos()

        if not dados:
            bot.reply_to(msg, "Nenhum dispositivo encontrado.")
            return

        resposta = "📡 Dispositivos:\n\n"

        for d in dados:
            id, ip, mac, fabricante, conectado, primeiro, ultimo = d

            status = "🟢 Online" if conectado else "🔴 Offline"

            resposta += (
                f"IP: {ip}\n"
                f"MAC: {mac}\n"
                f"Fabricante: {fabricante}\n"
                f"Status: {status}\n"
                f"Primeiro scan: {primeiro}\n"
                f"Último scan: {ultimo}\n\n"
            )

        bot.reply_to(msg, resposta)

@bot.message_handler(commands=["conectados"])
def listar_conectados(msg):

    dados = listar_dispositivos_conectados()

    if not dados:
        bot.reply_to(msg, "Nenhum dispositivo conectado no momento.")
        return

    resposta = "🟢 Dispositivos conectados:\n\n"

    for d in dados:
        ip, mac, fabricante = d

        resposta += (
            f"IP: {ip}\n"
            f"MAC: {mac}\n"
            f"Fabricante: {fabricante}\n\n"
        )

    bot.reply_to(msg, resposta)

bot.infinity_polling()