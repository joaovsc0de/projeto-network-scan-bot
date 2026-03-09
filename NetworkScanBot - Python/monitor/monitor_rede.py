from database.mysql_db import conectar, salvar_dispositivo

def registrar_dispositivos(lista):

    conn = conectar()

    for dispositivo in lista:
        salvar_dispositivo(dispositivo, conn)

    conn.commit()
    conn.close()