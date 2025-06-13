#!/bin/bash
echo "🚀 Iniciando Botovsky..."

# Ativa o ambiente virtual
source .venv/bin/activate

# Inicia o Telegram Bot
tmux new-session -d -s telegram "python3 telegram_bot.py"

# Inicia a análise periódica
tmux new-session -d -s analise "python3 main.py"

echo "✅ Bots rodando em segundo plano com tmux!"
