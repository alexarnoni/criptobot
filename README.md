# 🪙 CryptoBot – Monitoramento e Alertas de Criptomoedas

**CryptoBot** é um bot em Python desenvolvido para monitorar pares de criptomoedas em tempo real e enviar **alertas automáticos via Telegram** com base em condições pré-definidas. Ele utiliza dados da API da Binance (ou outra exchange) para acompanhar variações de preço, volume e indicadores de mercado.

## ⚙️ Funcionalidades principais

- 📊 **Monitoramento em tempo real** de pares como `BTC/USDT`, `ETH/USDT`, etc.
- 🔔 **Alertas personalizados via Telegram** ao atingir:
  - Limiares de preço (ex: "BTC caiu abaixo de $60.000")
  - Variações percentuais (ex: "+5% em 1h")
  - Condições de candle (ex: pump/dump, martelo, engolfo)

- 🧠 **Configuração simples por JSON ou diretamente no código**:
  - Escolha dos pares
  - Intervalos de tempo (ex: 1m, 5m, 1h)
  - Critérios de alerta

- 📈 Suporte a múltiplos pares simultaneamente, com leitura assíncrona e envio individualizado de alertas

## 🛠️ Tecnologias utilizadas

- Python 3
- Binance API (REST/WS)
- Telegram Bot API
- `requests`, `json`, `schedule`, `asyncio`

## 🚧 Status do projeto

- ✅ MVP funcional rodando localmente com alertas por preço e variação
- 🔜 Em desenvolvimento:
  - Suporte a indicadores técnicos (RSI, EMA, Bollinger Bands)
  - Interface interativa
