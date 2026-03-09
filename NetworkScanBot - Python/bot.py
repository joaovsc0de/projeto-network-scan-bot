
import telebot

from scanner.nmap_scanner import scan_rede
from scanner.parser import parse_scan
from monitor.monitor_rede import registrar_dispositivos
from database.mysql_db import listar_dispositivos, listar_dispositivos_conectados, resetar_conexoes

import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['scan'])
def scan(msg):

    resetar_conexoes()
    saida = scan_rede()

    dispositivos = parse_scan(saida)

    registrar_dispositivos(dispositivos)

    bot.reply_to(msg,"Scan finalizado")

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