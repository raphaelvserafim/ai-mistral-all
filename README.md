## MISTRAL AI API (STREAMING CHAT)
===============================

API leve e eficiente para comunicação com o modelo Mistral 7B Instruct (GGUF), 
com suporte a streaming de mensagens e armazenamento de histórico via SQLite.

Requisitos
----------

- Python 3.10+
- Flask
- SQLite3
- PM2 (opcional)
- Modelo GGUF (ex: mistral-7b-instruct)

Baixando o modelo
-----------------

mkdir -p models
```sh
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf \
  -O models/mistral.gguf
```

Inicializando o servidor
------------------------

Com PM2:
  ```sh
  pm2 start server.py --interpreter python3
  ```

Ou diretamente:
```sh
  python3 server.py
```

Endpoints
---------

1. Criar nova conversa:

```sh
  curl -X POST http://localhost:3000/api/conversation
```

### Exemplo de resposta:
  ```json
  {
    "status": 200,
    "conversation_id": "ff30bf0d8a9ca863bc21"
  }
```

2. Enviar mensagem (stream):

```sh
  curl -N -H "Content-Type: application/json" \
       -X POST http://localhost:3000/api/ask \
       -d '{"conversation_id": "ff30bf0d8a9ca863bc21", "content": "Olá, tudo bem?"}'
```

3. Buscar mensagens de uma conversa:

```sh
  curl http://localhost:3000/api/conversation/ff30bf0d8a9ca863bc21
```

4. Listar todas as conversas:

```sh
  curl http://localhost:3000/api/conversation
```

Estrutura de pastas (exemplo)
-----------------------------
```sh
.
├── app/
│   ├── ai.py
│   ├── db/
│   │   ├── db.py
│   │   └── queries.py
│   └── routes/
│       └── api.py
├── models/
│   └── mistral.gguf
├── server.py
├── README.txt
```
Licença
-------

Este projeto está sob a licença MIT. Use, modifique e contribua como quiser.
