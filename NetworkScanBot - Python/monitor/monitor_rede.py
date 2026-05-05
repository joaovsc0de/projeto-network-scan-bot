from database.Network_db import (
    conectar,
    salvar_dispositivo,
    deletar_portas,
    salvar_porta
)

def registrar_dispositivos(lista):

    conn = conectar()

    if conn is None:
        print("Erro: conexão com banco falhou")
        return 0

    novos = 0

    for dispositivo in lista:

        dispositivo_id, eh_novo = salvar_dispositivo(dispositivo, conn)

        if eh_novo:
            novos += 1

        if not dispositivo_id:
            continue

        portas = dispositivo.get("portas", [])

        if portas:
            deletar_portas(dispositivo_id, conn)

            for porta in portas:
                salvar_porta(dispositivo_id, porta, conn)

    conn.commit()
    conn.close()

    return novos