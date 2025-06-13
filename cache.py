import json
import os
import hashlib

ARQUIVO_CACHE = "cache_alertas.json"

def carregar_cache():
    """Carrega o cache salvo no disco"""
    if not os.path.exists(ARQUIVO_CACHE):
        return {}
    try:
        with open(ARQUIVO_CACHE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def salvar_cache(cache):
    """Salva o cache atualizado no disco"""
    with open(ARQUIVO_CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def gerar_hash_alerta(mensagem: str):
    """Gera um hash único da mensagem (ignora variações estéticas)"""
    return hashlib.sha256(mensagem.strip().lower().encode("utf-8")).hexdigest()

def alerta_ja_enviado(chat_id: str, moeda: str, mensagem: str) -> bool:
    """
    Verifica se uma mensagem de alerta já foi enviada para aquele chat_id e moeda.
    Se não foi, atualiza o cache com o novo hash.
    """
    cache = carregar_cache()
    chave = f"{chat_id}_{moeda.lower()}"
    novo_hash = gerar_hash_alerta(mensagem)
    hash_antigo = cache.get(chave)

    if hash_antigo == novo_hash:
        return True

    cache[chave] = novo_hash
    salvar_cache(cache)
    return False
