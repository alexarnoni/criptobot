# moedas_disponiveis.py
import requests

# Dicionário com nomes comuns para exibição (parcial, pode ser expandido)
NOMES_COMPLETOS = {
    "btc": "Bitcoin",
    "eth": "Ethereum",
    "usdt": "Tether",
    "bnb": "Binance Coin",
    "sol": "Solana",
    "xrp": "Ripple",
    "ada": "Cardano",
    "doge": "Dogecoin"
    # Você pode expandir esse dicionário conforme necessário
}

def get_moedas_binance():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("Erro ao buscar moedas disponíveis na Binance")

    data = resp.json()
    symbols = data.get("symbols", [])

    # extrair moedas únicas de todos os pares
    moedas = set()
    for s in symbols:
        moedas.add(s["baseAsset"].lower())
        moedas.add(s["quoteAsset"].lower())

    return sorted(list(moedas))

def formatar_lista_moedas(moedas, limite=100):
    """
    Formata a lista de moedas em blocos para envio no Telegram
    """
    blocos = []
    for i in range(0, len(moedas), limite):
        trecho = ", ".join(moedas[i:i+limite])
        blocos.append(trecho)
    return blocos

def obter_nome_completo(sigla: str):
    return NOMES_COMPLETOS.get(sigla.lower(), sigla.upper())

if __name__ == "__main__":
    moedas = get_moedas_binance()
    print(f"Total: {len(moedas)} moedas disponíveis na Binance\n")
    blocos = formatar_lista_moedas(moedas)
    for bloco in blocos:
        print(bloco)
        print("\n---\n")
