from database.Network_db import (
    conectar,
    salvar_dispositivo,
    deletar_portas,
    salvar_porta
)

def registrar_dispositivos(lista):

    print("Dispositivos recebidos:", lista)

    conn = conectar()

    if conn is None:
        print("Erro: conexão com banco falhou")
        return

    for dispositivo in lista:

        # 🔹 salva dispositivo e pega ID
        dispositivo_id = salvar_dispositivo(dispositivo, conn)

        # 🔥 NOVO: salvar portas (se existirem)
        if "portas" in dispositivo and dispositivo["portas"]:

            # evita duplicação
            deletar_portas(dispositivo_id, conn)

            for porta in dispositivo["portas"]:
                salvar_porta(dispositivo_id, porta, conn)

    conn.commit()
    conn.close()