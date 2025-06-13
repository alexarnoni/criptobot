import requests
import pandas as pd
from datetime import datetime
import logging

# Configuração do logger
logger = logging.getLogger(__name__)

# Mapeamento de nomes amigáveis para símbolos reais da Binance
MOEDA_TO_SYMBOL = {
    "solana": "SOLUSDT",
    "bitcoin": "BTCUSDT",
    "ethereum": "ETHUSDT"
    # Você pode expandir essa lista conforme necessário
}

def obter_historico_preco(moeda: str, quantidade: int = 30, intervalo: str = "1d"):
    """
    Busca histórico de preços da Binance para uma moeda em um dado intervalo.

    :param moeda: Nome da moeda (ex: 'solana', 'bitcoin')
    :param quantidade: Quantidade de candles
    :param intervalo: Intervalo (ex: '1d', '1h', '15m', '5m')
    """
    symbol = MOEDA_TO_SYMBOL.get(moeda.lower())
    if not symbol:
        logger.error(f"Moeda '{moeda}' não mapeada.")
        raise ValueError(f"Moeda '{moeda}' não mapeada para símbolo Binance.")

    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": intervalo,
        "limit": quantidade
    }

    logger.info(f"[API Binance] Requisição: {symbol}, Intervalo: {intervalo}, Candles: {quantidade}")
    resp = requests.get(url, params=params)

    if resp.status_code != 200:
        logger.error(f"Erro ao buscar dados da Binance para {symbol}: {resp.text}")
        raise Exception(f"Erro ao buscar dados da API Binance: {resp.text}")

    dados = resp.json()

    df = pd.DataFrame([{
        "date": datetime.fromtimestamp(item[0] / 1000),
        "price": float(item[4])  # preço de fechamento
    } for item in dados])

    df = df.set_index("date")
    logger.info(f"[{moeda.upper()}] {len(df)} registros recebidos da Binance.")
    return df

# Teste rápido
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    df = obter_historico_preco("solana", quantidade=48, intervalo="1h")
    print(df.tail())
