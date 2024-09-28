import os
import shutil
import time
import psutil
import winreg as reg
from customtkinter import *

appdata = os.environ['APPDATA']
key = reg.OpenKey(reg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, reg.KEY_ALL_ACCESS)

class Uninstall:
    def __init__(self):
        self.app = CTk()
        self.app.title('WPP SCHEDULER UNINSTALLER')
        self.app.grid_columnconfigure(0, weight=1)
        self.frame = CTkFrame(self.app)
        self.frame.grid(column=0, row=0, padx=20, pady=20)

        if verify_registry() == 0 and verify_appdata() == 0:
            self.deleted()
        else:
            self.label()
            self.button()

        self.app.mainloop()

    def label(self):
        label = CTkLabel(self.frame, text='Deseja mesmo remover as dependências do programa?')
        label.grid(column=0, row=0, padx=20, pady=(20,0))
        return label

    def button(self):
        button = CTkButton(self.frame, text='Uninstall', command=self.button_task)
        button.grid(column=0, row=1, padx= 20, pady=20)
        return button

    def deleted(self):
        msg = CTkLabel(self.frame, text='Parece que todas as dependências já foram deletadas.')
        msg.grid(column=0, row=0, padx=20, pady=20)

    def button_task(self):
        kill_sp()
        remove_registry()
        time.sleep(2)
        del_appdata_folder()

        self.app.destroy()
        time.sleep(1)
        Uninstall()

    def delete_widget(self, widget):
        widget.destroy()

def verify_registry():
    try:
        reg.QueryValueEx(key, 'sendMsgWPP')
        return 1
    except:
        return 0

def verify_appdata():
    try:
        os.listdir(appdata + r'/sendMsgWPP')
        return 1
    except:
        return 0

def kill_sp(): # kill schedule-process
    for process in psutil.process_iter():
        if process.name() == 'schedule_process.exe':
            process.kill()
            print('schedule_process.exe killed')

def del_appdata_folder():
    try:
        path = appdata + r'/sendMsgWPP'
        shutil.rmtree(path)
        print('Diretório removido')
    except:
        print('Erro ao deletar diretório')

def remove_registry():
    try:
        reg.DeleteValue(key, 'sendMsgWPP')
        print('Registro removido')
    except:
        print('Erro ao remover o registro')

if __name__ == '__main__':
    Uninstall()

# pyinstaller --onefile --icon=logo.ico --noconsole uninstall.py