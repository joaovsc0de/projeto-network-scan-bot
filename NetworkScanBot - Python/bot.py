
import telebot

from scanner.nmap_scanner import scan_rede
from scanner.parser import parse_scan
from monitor.monitor_rede import registrar_dispositivos
from database.Network_db import listar_dispositivos, listar_dispositivos_conectados, resetar_conexoes
from utils.network_utils import get_rede_atual
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['scan'])
def scan(msg):

    resetar_conexoes()

    args = msg.text.split()

    # 👇 se usuário passou rede
    if len(args) > 1:
        network = args[1]
    else:
        network = get_rede_atual()

    if not network:
        bot.reply_to(msg, "Não foi possível detectar a rede automaticamente.")
        return

    bot.reply_to(msg, f"Escaneando rede: {network}...")

    saida = scan_rede(network)

    dispositivos = parse_scan(saida)

    registrar_dispositivos(dispositivos)

    bot.reply_to(
        msg,
        f"Scan finalizado\nDispositivos encontrados: {len(dispositivos)}"
    )

@bot.message_handler(commands=['dispositivos'])
def dispositivos(msg):  

    lista = listar_dispositivos()

    resposta = ""

    for dispositivo in lista:
        resposta += f"Ip: {dispositivo[1]}\n - MAC: {dispositivo[2]}\n - Fabricante: {dispositivo[3]}\n - Primeiro Scan: {dispositivo[5]}\n - Último Scan: {dispositivo[6]}\n - Conectado: {'Sim' if dispositivo[4] else 'Não'}\n\n"

    if not resposta:
        resposta = "Nenhum dispositivo encontrado."

    bot.reply_to(msg, resposta)


@bot.message_handler(commands=['dispositivos_conectados'])
def dispositivos_conectados(msg):  

    lista = listar_dispositivos_conectados()

    resposta = ""

    for dispositivo in lista:
        resposta += f"Ip: {dispositivo[0]}\n - MAC: {dispositivo[1]}\n - Fabricante: {dispositivo[2]}\n\n"

    if not resposta:
        resposta = "Nenhum dispositivo conectado encontrado."

    bot.reply_to(msg, resposta)

bot.infinity_polling()