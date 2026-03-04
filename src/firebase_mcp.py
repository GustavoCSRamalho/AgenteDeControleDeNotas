# import json
# from pathlib import Path
# from langchain_mcp_adapters.client import MultiServerMCPClient


# def load_mcp_config() -> dict:
#     config_path = Path(__file__).parent / "mcp_config.json"
#     with open(config_path, "r") as f:
#         return json.load(f)


# async def create_firebase_mcp_client():
#     config = load_mcp_config()
#     client = MultiServerMCPClient(config)
#     all_tools = await client.get_tools()

#     # Filtra apenas ferramentas do Firestore
#     tools = [t for t in all_tools if "firestore" in t.name.lower()]

#     print(f"\n✅ Firebase MCP conectado! {len(tools)} ferramentas carregadas:")
#     for tool in tools:
#         print(f"   🔧 {tool.name}")
#     print()

#     return client, tools

import json
from pathlib import Path
from datetime import datetime, timezone
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import tool

PROJECT_ID = "nota-e0322"
DATABASE_ID = "(default)"
COLLECTION = "notes"
BASE_PATH = f"projects/{PROJECT_ID}/databases/{DATABASE_ID}/documents"
PARENT = BASE_PATH


def load_mcp_config() -> dict:
    config_path = Path(__file__).resolve().parent.parent / "mcp_config.json"
    print(config_path)
    with open(config_path, "r") as f:
        return json.load(f)


def to_firestore_fields(data: dict) -> dict:
    """Converte dict Python para formato Firestore Value."""
    fields = {}
    for key, value in data.items():
        if isinstance(value, str):
            fields[key] = {"stringValue": value}
        elif isinstance(value, bool):
            fields[key] = {"booleanValue": value}
        elif isinstance(value, int):
            fields[key] = {"integerValue": str(value)}
        elif isinstance(value, float):
            fields[key] = {"doubleValue": value}
    return fields


def from_firestore_doc(doc: dict) -> dict:
    """Converte documento Firestore para dict Python legível."""
    result = {"id": doc.get("name", "").split("/")[-1]}
    for key, value in doc.get("fields", {}).items():
        for vtype, vval in value.items():
            result[key] = vval
    return result

def parse_result(result):
    """Normaliza o resultado do MCP para dict."""
    if isinstance(result, dict):
        return result
    if isinstance(result, list):
        # MCP retorna lista de content blocks
        text = "".join(item.get("text", "") if isinstance(item, dict) else str(item) for item in result)
        return json.loads(text) if text.strip() else {}
    if isinstance(result, str):
        return json.loads(result) if result.strip() else {}
    return {}


async def create_firebase_mcp_client():
    config = load_mcp_config()
    client = MultiServerMCPClient(config)
    all_tools = await client.get_tools()
    mcp = {t.name: t for t in all_tools}

    print(f"\n✅ Firebase MCP conectado!")

    @tool
    async def add_note(title: str, content: str) -> str:
        """Cria uma nota no Firestore com título e conteúdo."""
        now = datetime.now(timezone.utc).isoformat()
        result = await mcp["firestore_add_document"].ainvoke({
            "parent": PARENT,
            "collectionId": COLLECTION,
            "document": {
                "fields": to_firestore_fields({
                    "title": title,
                    "content": content,
                    "createdAt": now,
                    "updatedAt": now,
                })
            }
        })
        doc = from_firestore_doc(parse_result(result))
        return f"Nota criada com ID: {doc['id']}"

    @tool
    async def list_notes() -> str:
        """Lista todas as notas do Firestore."""
        result = await mcp["firestore_list_documents"].ainvoke({
            "parent": PARENT,
            "collectionId": COLLECTION,
        })
        data = parse_result(result)
        docs = data.get("documents", [])
        if not docs:
            return "Nenhuma nota encontrada."
        notes = [from_firestore_doc(d) for d in docs]
        lines = [f"ID: {n['id']} | {n.get('title','(sem título)')} — {n.get('content','')}" for n in notes]
        return "\n".join(lines)

    @tool
    async def update_note(document_id: str, title: str, content: str) -> str:
        """Atualiza uma nota existente pelo ID."""
        now = datetime.now(timezone.utc).isoformat()
        name = f"{BASE_PATH}/{COLLECTION}/{document_id}"
        await mcp["firestore_update_document"].ainvoke({
            "document": {
                "name": name,
                "fields": to_firestore_fields({
                    "title": title,
                    "content": content,
                    "updatedAt": now,
                })
            },
            "updateMask": {
                "fieldPaths": ["title", "content", "updatedAt"]  # só esses campos são tocados
            }
        })
        return f"Nota {document_id} atualizada com sucesso."

    @tool
    async def delete_note(document_id: str) -> str:
        """Deleta uma nota pelo ID."""
        name = f"{BASE_PATH}/{COLLECTION}/{document_id}"
        await mcp["firestore_delete_document"].ainvoke({"name": name})
        return f"Nota {document_id} deletada com sucesso."

    return client, [add_note, list_notes, update_note, delete_note]