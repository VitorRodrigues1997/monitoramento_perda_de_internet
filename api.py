from fastapi import FastAPI
import os

app = FastAPI()

ARQUIVO_LOG = "relatorio_rede.txt"

ultimo_status = {
    "perda": None,
    "latencia": None,
    "status": "aguardando primeira medicao",
    "horario": None
}

@app.get("/status")
def ver_status():
    return ultimo_status

@app.post("/atualizar")
def atualizar(dados: dict):
    ultimo_status["perda"] = dados["perda"]
    ultimo_status["latencia"] = dados["latencia"]
    ultimo_status["status"] = dados["status"]
    ultimo_status["horario"] = dados["horario"]
    return {"mensagem": "atualizado"}

@app.get("/historico")
def ver_historico():
    if not os.path.exists(ARQUIVO_LOG):
        return {"erro": "nenhum log encontrado"}
    with open(ARQUIVO_LOG, "r") as f:
        linhas = f.readlines()
    return {"total": len(linhas), "registros": linhas[-20:]}
