# 🤖 OpenCommit + Groq + Llama 4 Scout

> Gere mensagens de commit inteligentes e automáticas usando IA diretamente no seu terminal — de graça e em milissegundos.

---

## 📌 Conceito

### O que é o OpenCommit?

O **OpenCommit** (`oco`) é uma ferramenta de linha de comando que analisa o `git diff` do seu stage e usa uma IA para gerar automaticamente mensagens de commit seguindo boas práticas (como o padrão [Conventional Commits](https://www.conventionalcommits.org/)).

Em vez de escrever `git commit -m "fix stuff"`, você roda `oco` e a IA descreve o que você realmente mudou.

### O que é o Groq?

O **Groq** é uma plataforma de inferência de LLMs com hardware proprietário (LPU) que entrega velocidades absurdas — acima de 400 tokens por segundo. É gratuito para uso pessoal com limites generosos.

### O que é o Llama 4 Scout?

O **Llama 4 Scout** é um modelo da Meta disponível no Groq. Com arquitetura MoE (Mixture of Experts) de 17 bilhões de parâmetros ativos, ele é rápido, preciso e extremamente barato — ideal para tarefas de código como geração de commits.

### Por que essa combinação?

| Critério | Resultado |
|---|---|
| Velocidade | ~460 tokens/segundo (quase instantâneo) |
| Custo | $0.11 por milhão de tokens (praticamente zero) |
| Qualidade | Excelente para contexto de código |
| Setup | < 5 minutos |

---

## 🛠️ Pré-requisitos

- [Node.js](https://nodejs.org) v18 ou superior
- [Git](https://git-scm.com) instalado e configurado
- Conta no [Groq Console](https://console.groq.com)

---

## 🔑 Passo 1 — Criar sua API Key no Groq

1. Acesse [console.groq.com](https://console.groq.com) e crie sua conta (gratuita)
2. No menu lateral, clique em **API Keys**
3. Clique em **Create API Key**
4. Dê um nome (ex: `opencommit`) e copie a chave gerada

> ⚠️ **Atenção:** A chave começa com `gsk_`. Guarde-a com segurança. Nunca compartilhe em chats, commits ou arquivos públicos.

---

## 📦 Passo 2 — Instalar o OpenCommit

```bash
npm install -g opencommit
```

Verifique a instalação:

```bash
oco --version
```

---

## ⚙️ Passo 3 — Configurar o OpenCommit

Execute os comandos abaixo no terminal, substituindo `gsk_SUA_CHAVE_AQUI` pela sua chave real:

```bash
# Define o provider como Groq
oco config set OCO_AI_PROVIDER=groq

# Sua API key do Groq
oco config set OCO_API_KEY=gsk_SUA_CHAVE_AQUI

# Modelo: Llama 4 Scout (melhor custo-benefício)
oco config set OCO_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
```

### Configurações opcionais recomendadas

```bash
# Adiciona emojis nas mensagens de commit (estilo gitmoji)
oco config set OCO_EMOJI=true

# Inclui explicação do "porquê" da mudança no commit
oco config set OCO_WHY=true

# Idioma das mensagens (pt para português, en para inglês)
oco config set OCO_LANGUAGE=pt
```

Verifique tudo que foi configurado:

```bash
oco config get
```

---

## 🚀 Passo 4 — Usar no dia a dia

```bash
# 1. Faça suas alterações nos arquivos

# 2. Adicione ao stage normalmente
git add .

# 3. Deixa a IA gerar o commit
oco
```

A IA vai analisar o diff, gerar uma mensagem de commit e perguntar se você quer confirmar antes de commitar.

---

## 🔄 Modelos disponíveis no Groq

Caso queira trocar o modelo, use um dos IDs abaixo:

| Modelo | ID para o `OCO_MODEL` | Velocidade | Custo (input) |
|---|---|---|---|
| **Llama 4 Scout** ⭐ | `meta-llama/llama-4-scout-17b-16e-instruct` | ~460 TPS | $0.11/M |
| Llama 4 Maverick | `meta-llama/llama-4-maverick-17b-128e-instruct` | ~297 TPS | $0.50/M |
| Llama 3.3 70B | `llama-3.3-70b-versatile` | rápido | $0.59/M |

Para trocar:

```bash
oco config set OCO_MODEL=meta-llama/llama-4-maverick-17b-128e-instruct
```

---

## 🔐 Boas práticas de segurança

- **Nunca** commite sua `OCO_API_KEY` no código
- **Nunca** compartilhe sua chave em chats, issues ou PRs
- Se suspeitar que a chave foi exposta, **revogue imediatamente** em [console.groq.com/keys](https://console.groq.com/keys) e gere uma nova
- Opcional: armazene a chave em variável de ambiente no seu sistema:

```bash
# No ~/.bashrc ou ~/.zshrc
export GROQ_API_KEY=gsk_SUA_CHAVE_AQUI
```

---

## 🐛 Problemas comuns — OpenCommit

| Erro | Solução |
|---|---|
| `Invalid API Key` | Verifique se a chave está correta com `oco config get` |
| `Model not found` | Confirme o nome exato do modelo no [Groq Console](https://console.groq.com/docs/models) |
| `No staged changes` | Rode `git add .` antes do `oco` |
| `oco: command not found` | Verifique se o npm global está no PATH: `npm config get prefix` |

---

---

# 📝 Notes Agent — LangChain + Groq + Firebase MCP (Python)

Agente de notas via chat no terminal usando **LangChain (Python)**, **Groq (Llama 4 Scout)** e **Firebase MCP**.

## 🏗️ Arquitetura

```
Terminal (input/asyncio)
         │
         ▼
  LangChain Agent (ReAct)
  • Model: Llama 4 Scout (via Groq)
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
- Conta no [Groq Console](https://console.groq.com) com API Key
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
# Edite o .env e adicione sua GROQ_API_KEY
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
│   ├── agent.py       # Agente LangChain (ReAct + Groq/Llama)
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
| `langchain-groq` | >=0.1 | Integração com Groq/Llama |
| `langgraph` | >=0.2 | Agente ReAct (orquestração) |
| `langchain-mcp-adapters` | >=0.1 | Bridge MCP → LangChain tools |
| `firebase-tools` (Node) | latest | Firebase MCP Server |
| Firebase Firestore | — | Banco de dados |

## ❓ Troubleshooting — Notes Agent

**`ModuleNotFoundError`**
```bash
pip install -r requirements.txt
```

**`GROQ_API_KEY not found`**
Verifique se o `.env` existe e tem a chave correta (começa com `gsk_`).

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

---

## 📚 Links úteis

- [OpenCommit — GitHub](https://github.com/di-sukharev/opencommit)
- [Groq Console](https://console.groq.com)
- [Groq — Documentação de modelos](https://console.groq.com/docs/models)
- [Conventional Commits](https://www.conventionalcommits.org/pt-br/)
- [Meta Llama 4](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)
- [LangChain Python](https://python.langchain.com)
- [Firebase Console](https://console.firebase.google.com)

---

## 📝 Licença

MIT — use, modifique e distribua à vontade.
