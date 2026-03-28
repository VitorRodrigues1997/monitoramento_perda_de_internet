# Monitor de Perda de Internet

Monitor de rede em tempo real com API REST integrada.

## O que faz

- Monitora perda de pacote e latência a cada 30 segundos
- Alerta quando a rede está ruim
- Salva histórico em log com data e hora
- API REST para consultar o status de qualquer lugar

## Tecnologias

- Python 3
- FastAPI
- Uvicorn
- Bash / Linux

## Como rodar

### Monitor
```bash
python3 monitor.py
```

### API
```bash
uvicorn api:app --reload
```

### Consultar status
```bash
curl http://127.0.0.1:8000/status
```

## Rotas da API

| Método | Rota | O que faz |
|--------|------|-----------|
| GET | /status | retorna status atual da rede |
| GET | /historico | retorna últimos 20 registros |
| POST | /atualizar | monitor envia dados para API |
