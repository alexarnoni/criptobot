# schedule.py
import schedule
import time
from main import executar_para_todos_usuarios

print("⏱️ Agendador iniciado... Botovsky está em vigília 👁️")

# Executa nos minutos exatos: 00 e 30
schedule.every().hour.at(":00").do(executar_para_todos_usuarios)
schedule.every().hour.at(":30").do(executar_para_todos_usuarios)

# Loop principal
while True:
    schedule.run_pending()
    time.sleep(1)
