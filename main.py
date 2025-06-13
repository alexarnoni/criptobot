from crypto_data import obter_historico_preco
from analysis import analisar_variacoes
from telegram_bot import enviar_alerta
from user_store import carregar_usuarios
from moedas_disponiveis import obter_nome_completo
from cache import alerta_ja_enviado
from dotenv import load_dotenv
import os
import time
import logging

# === Configura Logging ===
logging.basicConfig(
    filename="main.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

load_dotenv()

INTERVALO = "1h"
QUANTIDADE = 48

def executar_para_todos_usuarios():
    usuarios = carregar_usuarios()

    for chat_id, dados in usuarios.items():
        moedas = dados.get("moedas", [])
        if not moedas:
            continue

        for moeda in moedas:
            try:
                logging.info(f"Analisando {moeda.upper()} para usuário {chat_id}")
                df = obter_historico_preco(moeda, quantidade=QUANTIDADE, intervalo=INTERVALO)

                resultado = analisar_variacoes(df, moeda)
                if not resultado["alertas"] or resultado["alertas"] == ["Sem sinais relevantes hoje"]:
                    logging.info(f"Nenhum sinal relevante para {moeda.upper()}")
                    continue

                mensagem = (
                    f"📡 *Botovsky Alerta*\n"
                    f"Moeda: *{moeda.upper()} ({obter_nome_completo(moeda)})*\n"
                    f"🕒 Intervalo: {INTERVALO} (últimos {QUANTIDADE} candles)\n"
                    f"💵 Preço atual: ${resultado['preco_hoje']}\n"
                    f"📈 Variação recente: {resultado['retorno_hoje']}%\n"
                    f"📉 Acumulado período: {resultado['retorno_30d']}%\n"
                    f"\n" + "\n".join(f"🔔 *{a}*" for a in resultado["alertas"])
                )

                if alerta_ja_enviado(str(chat_id), moeda, mensagem):
                    logging.info(f"Alerta repetido ignorado para {moeda.upper()}")
                    continue

                enviar_alerta(chat_id, mensagem)
                logging.info(f"Alerta enviado para {moeda.upper()} - usuário {chat_id}")
                time.sleep(1)

            except Exception as e:
                logging.error(f"Erro ao processar {moeda.upper()} para usuário {chat_id}: {e}")

if __name__ == "__main__":
    executar_para_todos_usuarios()
