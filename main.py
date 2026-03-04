import asyncio
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from firebase_mcp import create_firebase_mcp_client
from agent import create_agent

load_dotenv()


def print_separator():
    print("─" * 60)


def print_agent(text: str):
    print(f"\n🤖 Agente: {text}\n")


def print_examples():
    print("""
📖 Exemplos de como usar:

  CRIAR NOTAS:
  • "Cria uma nota: Comprar leite"
  • "Anota: ligar para o médico amanhã"
  • "Cria nota com título 'Reunião' e conteúdo 'Discutir metas do trimestre'"
  • "Nota - Estudos: revisar capítulo 3 do livro de Python"
  • "Salva: título=Receita, conteúdo=2 ovos, farinha e açúcar"

  LISTAR:
  • "Lista todas as minhas notas"
  • "Mostra minhas notas"
  • "Quais notas eu tenho?"

  ATUALIZAR:
  • "Atualiza a nota <ID> com título 'Novo título' e conteúdo 'Novo conteúdo'"
  • "Edita a nota <ID>: título=Compras, conteúdo=leite, ovos e pão"

  DELETAR:
  • "Deleta a nota <ID>"
  • "Remove a nota <ID>"
  • "Apaga todas as notas" (cuidado!)
""")


def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
            if not isinstance(block, dict) or block.get("type") == "text"
        )
    return str(content)


async def chat_loop(agent):
    message_history = []

    print_separator()
    print("💬 Chat iniciado! Digite sua mensagem ou 'sair' para encerrar.")
    print("   Digite 'exemplos' para ver como usar.")
    print_separator()
    print_examples()

    while True:
        try:
            user_input = input("\n👤 Você: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Encerrando. Até mais!")
            break

        if user_input.lower() in ("sair", "exit", "quit"):
            print("\n👋 Encerrando o agente. Até mais!")
            break

        if user_input.lower() == "exemplos":
            print_examples()
            continue

        if not user_input:
            continue

        message_history.append(HumanMessage(content=user_input))

        try:
            print("\n⏳ Processando...")

            result = await agent.ainvoke({"messages": message_history})

            last_message = result["messages"][-1]
            response_text = extract_text(last_message.content)

            message_history.clear()
            message_history.extend(result["messages"][-6:])

            print_agent(response_text)

        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ Erro: {error_msg}")
            if "GROQ_API_KEY" in error_msg:
                print("   Verifique se GROQ_API_KEY está no seu .env")


async def main():
    if not os.getenv("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY não encontrada!")
        print("   Crie sua chave gratuita em: https://console.groq.com")
        return

    print("\n🔥 Notes Agent — LangChain + Firebase MCP (Python)")
    print_separator()
    print("Inicializando conexão com Firebase MCP...\n")

    mcp_client = None

    try:
        mcp_client, tools = await create_firebase_mcp_client()
        agent = create_agent(tools)
        await chat_loop(agent)

    except FileNotFoundError:
        print("❌ mcp_config.json não encontrado!")

    except Exception as e:
        print(f"\n❌ Falha ao inicializar: {e}")
        print("\n💡 Verifique:")
        print("   1. Node.js instalado")
        print("   2. firebase-tools: npm install -g firebase-tools")
        print("   3. Autenticado: firebase login")
        print("   4. PROJECT_ID correto no mcp_config.json")
        print("   5. GROQ_API_KEY no arquivo .env")

    finally:
        pass


if __name__ == "__main__":
    asyncio.run(main())