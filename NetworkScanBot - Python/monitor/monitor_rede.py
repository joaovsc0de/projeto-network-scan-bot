from database.Network_db import conectar, salvar_dispositivo

def registrar_dispositivos(lista):

    print("Dispositivos recebidos:", lista)

    conn = conectar()

    if conn is None:
        print("Erro: conexão com banco falhou")
        return

    for dispositivo in lista:
        salvar_dispositivo(dispositivo, conn)

    conn.commit()
    conn.close()