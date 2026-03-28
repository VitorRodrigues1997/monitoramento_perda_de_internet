import subprocess
import datetime
import time
import urllib.request
import json

HOST = "8.8.8.8"
LIMITE_PERDA = 5
LIMITE_LATENCIA = 80
ARQUIVO_LOG = "relatorio_rede.txt"
API_URL = "http://127.0.0.1:8000/atualizar"

def enviar_para_api(dados):
    try:
        body = json.dumps(dados).encode("utf-8")
        req = urllib.request.Request(
            API_URL,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req)
        print("  Enviado para API: OK")
    except Exception as e:
        print("  Erro ao enviar para API:", e)

def testar_rede():
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    resultado = subprocess.run(
        ["ping", "-c", "10", "-W", "1", HOST],
        capture_output=True,
        text=True
    )

    saida = resultado.stdout
    perda = None
    latencia = None

    for linha in saida.split("\n"):
        if "packet loss" in linha:
            perda = int(linha.split("%")[0].split()[-1])
        if "rtt" in linha:
            latencia = linha.split("/")[4]

    if perda is None:
        perda = 100

    if perda >= LIMITE_PERDA:
        status = "ALERTA - REDE RUIM"
    else:
        status = "OK"

    print(f"\n[{agora}]")
    print(f"  Perda    : {perda}%")
    print(f"  Latencia : {latencia}ms" if latencia else "  Latencia : indisponivel")
    print(f"  Status   : {status}")

    dados = {
        "perda": str(perda) + "%",
        "latencia": str(latencia) + "ms" if latencia else "indisponivel",
        "status": status,
        "horario": agora
    }

    enviar_para_api(dados)

    with open(ARQUIVO_LOG, "a") as log:
        log.write(f"[{agora}] perda={perda}% latencia={latencia}ms status={status}\n")

print("Monitor iniciado. Enviando dados para a API a cada 30s.")

while True:
    testar_rede()
    time.sleep(30)
