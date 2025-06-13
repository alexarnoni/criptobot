#!/bin/bash
echo "⛔ Encerrando sessões do Botovsky..."

tmux kill-session -t telegram 2>/dev/null
tmux kill-session -t analise 2>/dev/null

echo "✅ Todas as sessões foram finalizadas."
