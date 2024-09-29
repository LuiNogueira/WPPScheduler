import schedule as sc
import time
import json
import os
import send_message
import logging
# WatchDog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta

# Possível problema: E se tivermos duas instancias com o mesmo horário e dia?

# Universal Variables
appdata = os.environ['APPDATA'] + r'\WPPScheduler'

logging.basicConfig(filename=appdata+r'\schedule_process_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def open_json():
    try:
        with open(appdata+r'\data.json', 'r') as file:
            data = json.load(file)
        logging.info('Arquivo JSON carregado com sucesso')
        return data
    except Exception as e:
        logging.error(f'Erro ao carregar o arquivo JSON: {e}')
        return []

def execute(text, num, repeat, index):
    send_message.Job(text, num, repeat, index)
    logging.info(f'script send_message executado com sucesso, com as informações msg: {text}, num: {num}, repeat: {repeat}, index: {index}')
    print(f'{num}, {text}')

# Função para agendar as tarefas
def schedule_tasks(data):
    sc.clear()
    for i, task in enumerate(data):
        # Variáveis
        num = task["num"]
        text = task["message"]
        time_str = task["time"]
        day = task["day"]
        repeat = task["repeat"]
        index = i

        # Executa o agendamento
        job = getattr(sc.every(), day).at(time_str).do(execute, text, num, repeat, index)

# Função para verificar se o JSON é modificado
class JsonChangeHandler(FileSystemEventHandler):
    def __init__(self, reload_module):
        self.reload_module = reload_module
        self.last_modified = datetime.now()

    def on_modified(self, event):
        file = appdata + r'\data.json'
        if file == event.src_path and datetime.now() - self.last_modified > timedelta(seconds=1):
            self.reload_module()
            self.last_modified = datetime.now()

def reload_tasks():
    logging.info('JSON atualizado')
    data = open_json()
    schedule_tasks(data)

# Inicializa WatchDog
handler = JsonChangeHandler(reload_tasks)
observer = Observer()
observer.schedule(handler, path=appdata, recursive=False)
observer.start()

# Inicializando o loop
try:
    while True:
        sc.run_pending()
        time.sleep(1)
        # jobs = sc.get_jobs()
        # print(jobs)
except KeyboardInterrupt:
    observer.stop()

observer.join()

# pyinstaller --onefile --icon=logo.ico --noconsole schedule_process.py