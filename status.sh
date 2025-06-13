#!/bin/bash

echo "🧐 O que você deseja fazer?"
echo "1) Ver logs do Telegram Bot (ao vivo)"
echo "2) Ver logs da Análise de Mercado (ao vivo)"
echo "3) Ver resumo de logs (últimos prints de ambos)"
echo "0) Sair"
echo ""

read -p "Digite a opção: " opcao

case $opcao in
  1)
    tmux attach-session -t telegram
    ;;
  2)
    tmux attach-session -t analise
    ;;
  3)
    echo "📋 Logs Telegram:"
    tmux capture-pane -pt telegram
    echo ""
    echo "📋 Logs Análise:"
    tmux capture-pane -pt analise
    ;;
  0)
    echo "Saindo..."
    ;;
  *)
    echo "❌ Opção inválida."
    ;;
esac
