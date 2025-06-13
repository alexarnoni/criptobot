# telegram_bot.py
import os
import requests
from dotenv import load_dotenv
from user_store import registrar_usuario, adicionar_moeda, remover_moeda, listar_moedas
from moedas_disponiveis import get_moedas_binance, formatar_lista_moedas, obter_nome_completo
import time

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# moedas mais populares primeiro
PRIORITARIAS = ["btc", "eth", "usdt", "bnb", "sol", "xrp", "ada", "doge"]
MOEDAS_VALIDAS = get_moedas_binance()
MOEDAS_FILTRADAS = [m for m in MOEDAS_VALIDAS if m in PRIORITARIAS or len(m) <= 5]  # filtro básico por nome curto/popular
MOEDAS_ORDENADAS = sorted(set(PRIORITARIAS + MOEDAS_FILTRADAS), key=lambda x: (x not in PRIORITARIAS, x))

def enviar_alerta(chat_id: str, mensagem: str):
    try:
        url = f"{BASE_URL}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": mensagem,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def processar_mensagem(chat_id, text):
    text = text.strip().lower()

    try:
        if text == "/start":
            registrar_usuario(chat_id)
            enviar_alerta(chat_id, "👋 Botovsky ativado! Use /listar para ver moedas disponíveis e /add <moeda> para acompanhar.")

        elif text.startswith("/add"):
            partes = text.split()
            if not partes[1:]:
                enviar_alerta(chat_id, "⚠️ Nenhuma moeda informada. Ex: `/add sol eth`")
                return

            moedas_atuais = set(listar_moedas(chat_id))
            adicionadas = []
            ja_adicionadas = []
            invalidas = []

            for moeda in partes[1:]:
                if moeda not in MOEDAS_VALIDAS:
                    invalidas.append(moeda)
                elif moeda in moedas_atuais:
                    ja_adicionadas.append(moeda)
                else:
                    adicionar_moeda(chat_id, moeda)
                    adicionadas.append(moeda)

            if adicionadas:
                enviar_alerta(chat_id, f"✅ Adicionadas: {', '.join(adicionadas)}")
            if ja_adicionadas:
                enviar_alerta(chat_id, f"ℹ️ Já estavam adicionadas: {', '.join(ja_adicionadas)}")
            if invalidas:
                enviar_alerta(chat_id, f"⚠️ Inválidas: {', '.join(invalidas)}")

        elif text.startswith("/remove"):
            partes = text.split()
            if len(partes) == 2:
                remover_moeda(chat_id, partes[1])
                enviar_alerta(chat_id, f"🗑️ Moeda *{partes[1]}* removida.")
            else:
                enviar_alerta(chat_id, "⚠️ Use `/remove sol` para remover uma moeda.")

        elif text == "/minhas":
            moedas = listar_moedas(chat_id)
            if moedas:
                nomes = [f"{moeda.upper()} ({obter_nome_completo(moeda)})" for moeda in moedas]
                enviar_alerta(chat_id, "📌 Suas moedas: " + ", ".join(nomes))
            else:
                enviar_alerta(chat_id, "📭 Nenhuma moeda adicionada ainda. Use /add <moeda>")

        elif text == "/listar":
            blocos = formatar_lista_moedas(MOEDAS_ORDENADAS[:50], limite=50)
            enviar_alerta(chat_id, f"💰 Moedas populares disponíveis na Binance ({len(MOEDAS_ORDENADAS[:50])} mostradas):")
            enviar_alerta(chat_id, "🔝 Mais populares primeiro: *btc, eth, usdt, bnb, sol, xrp, ada, doge*\n\nℹ️ Use `/add sigla` para acompanhar uma moeda.\nSe sua moeda não estiver na lista, consulte a sigla na sua corretora/carteira e use `/add sigla`. Exemplo: `/add trx`")
            for bloco in blocos:
                enviar_alerta(chat_id, bloco)

        else:
            enviar_alerta(chat_id, "🤖 Comando não reconhecido. Use /listar ou /ajuda")

    except Exception as e:
        enviar_alerta(chat_id, f"❌ Erro ao processar comando: {e}")

if __name__ == "__main__":
    print("📡 Polling iniciado. Enviando mensagens para Botovsky...")
    offset = None
    while True:
        url = f"{BASE_URL}/getUpdates"
        params = {"timeout": 30, "offset": offset}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            updates = response.json().get("result", [])
            for update in updates:
                offset = update["update_id"] + 1
                message = update.get("message")
                if message:
                    chat_id = message["chat"]["id"]
                    text = message.get("text", "")
                    processar_mensagem(chat_id, text)
        time.sleep(1)
