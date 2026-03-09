from datetime import datetime

import mysql.connector
import config

def conectar():

    try:

        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASS,
            database=config.DB_NAME
        )

        return conn

    except Exception as e:

        print("Erro ao conectar no banco:")
        print(e)

def salvar_dispositivo(dispositivo, conn):

    cursor = conn.cursor()

    cursor.execute("""
    INSERT IGNORE INTO dispositivos (ip, mac, fabricante)
    VALUES (%s,%s,%s)
    """,(dispositivo["ip"], dispositivo["mac"], dispositivo["fabricante"]))

    atualizar_conexao(dispositivo["mac"], conn)  

def listar_dispositivos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dispositivos")

    dispositivos = cursor.fetchall()
    conn.close()

    return dispositivos

def listar_dispositivos_conectados():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT ip, mac, fabricante FROM dispositivos
                      WHERE conectado = 1""")

    dispositivos = cursor.fetchall()
    conn.close()

    return dispositivos

def resetar_conexoes():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("UPDATE dispositivos SET conectado = 0")

    conn.commit()
    conn.close()    

def atualizar_conexao(mac, conexao):

    cursor = conexao.cursor()

    cursor.execute("""UPDATE dispositivos 
                      SET conectado = 1, ultimo_scan = %s
                      WHERE mac = %s""", (datetime.now(), mac))
