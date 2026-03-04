# 📝 Notes Agent — LangChain + Firebase MCP (Python)

Agente de notas via chat no terminal usando **LangChain (Python)** e **Firebase MCP**.

## 🏗️ Arquitetura

```
Terminal (input/asyncio)
         │
         ▼
  LangChain Agent (ReAct)
  • Model: Claude 3.5 Sonnet
  • Framework: LangGraph
         │
         ▼
  langchain-mcp-adapters
  (converte tools MCP → LangChain)
         │
         ▼
  Firebase MCP Server (firebase-tools via Node.js)
         │
         ▼
  Firebase Firestore
  (coleção: "notes")
```

## 📋 Pré-requisitos

- Python >= 3.11
- Node.js >= 18 (necessário para o Firebase MCP)
- Conta na [Anthropic](https://console.anthropic.com) com API Key
- Conta no [Firebase](https://console.firebase.google.com) com Firestore ativado

## 🚀 Instalação

### 1. Crie e ative o ambiente virtual
```bash
cd notes-agent-py
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 2. Instale as dependências Python
```bash
pip3 install -r requirements.txt
```

### 3. Instale o Firebase CLI (Node.js)
```bash
npm install -g firebase-tools
firebase login
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o .env e adicione sua ANTHROPIC_API_KEY
```

### 5. Configure o projeto Firebase
Edite o `mcp_config.json` e substitua `SEU_PROJECT_ID`:

```json
{
  "firebase": {
    "command": "npx",
    "args": ["-y", "firebase-tools@latest", "experimental:mcp", "--project", "meu-projeto-123"]
  }
}
```

> 💡 O ID do projeto está na URL: `console.firebase.google.com/project/SEU_ID`

### 6. Execute o agente
```bash
python main.py
```

## 💬 Exemplos de uso

```
👤 Você: Cria uma nota: Estudar LangChain hoje às 15h

👤 Você: Cria uma nota com título "Reunião" e conteúdo "Apresentar projeto na sexta"

👤 Você: Lista todas as minhas notas

👤 Você: Mostra os detalhes da nota abc123

👤 Você: Atualiza a nota abc123 para: conteúdo atualizado

👤 Você: Deleta a nota abc123

👤 Você: Quantas notas eu tenho?

👤 Você: sair
```

## 📂 Estrutura do projeto

```
notes-agent-py/
├── src/
│   ├── __init__.py
│   ├── agent.py       # Agente LangChain (ReAct + Claude)
│   └── mcp.py         # Conexão com Firebase MCP
├── main.py            # Entry point — chat loop assíncrono
├── mcp_config.json    # Config do servidor MCP
├── requirements.txt   # Dependências Python
├── .env.example       # Exemplo de variáveis de ambiente
└── .env               # Suas variáveis (não commitar!)
```

## 🔧 Tecnologias

| Tecnologia | Versão | Papel |
|---|---|---|
| `langchain` | >=0.3 | Core do framework |
| `langchain-anthropic` | >=0.3 | Integração com Claude |
| `langgraph` | >=0.2 | Agente ReAct (orquestração) |
| `langchain-mcp-adapters` | >=0.1 | Bridge MCP → LangChain tools |
| `firebase-tools` (Node) | latest | Firebase MCP Server |
| Firebase Firestore | — | Banco de dados |

## ❓ Troubleshooting

**`ModuleNotFoundError`**
```bash
pip install -r requirements.txt
```

**`ANTHROPIC_API_KEY not found`**
Verifique se o `.env` existe e tem a chave correta.

**Erro de conexão com Firebase MCP**
```bash
# Teste se o firebase-tools está funcionando
npx firebase-tools@latest --version
firebase login --reauth
```

**Erro de permissão no Firestore (para desenvolvimento)**
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```
> ⚠️ Use apenas em desenvolvimento!
