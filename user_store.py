# user_store.py
import json
import os

ARQUIVO = "user_store.json"

def carregar_usuarios():
    if not os.path.exists(ARQUIVO):
        return {}
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_usuarios(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2)

def registrar_usuario(chat_id, moedas=None):
    usuarios = carregar_usuarios()
    if str(chat_id) not in usuarios:
        usuarios[str(chat_id)] = {
            "moedas": moedas or []  # antes era ["solana"]
        }
        salvar_usuarios(usuarios)

def obter_moedas_do_usuario(chat_id):
    usuarios = carregar_usuarios()
    return usuarios.get(str(chat_id), {}).get("moedas", [])

def adicionar_moeda(chat_id, moeda):
    usuarios = carregar_usuarios()
    chat_id = str(chat_id)
    if chat_id not in usuarios:
        usuarios[chat_id] = {"moedas": [moeda]}
    else:
        if moeda not in usuarios[chat_id]["moedas"]:
            usuarios[chat_id]["moedas"].append(moeda)
    salvar_usuarios(usuarios)

def remover_moeda(chat_id, moeda):
    usuarios = carregar_usuarios()
    chat_id = str(chat_id)
    if chat_id in usuarios and moeda in usuarios[chat_id]["moedas"]:
        usuarios[chat_id]["moedas"].remove(moeda)
        salvar_usuarios(usuarios)

def listar_moedas(chat_id):
    return obter_moedas_do_usuario(chat_id)
