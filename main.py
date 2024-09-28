from customtkinter import *
from agenda import Agenda
import json
import urllib.parse
import winreg as reg
import os
from shutil import copy

class Interface:
    def __init__(self):
        # Definindo variáveis universais
        self.checkbox_var = []
        self.time_var = []
        self.repeat_var = []
        self.semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        self.appdata = os.environ['APPDATA']
        self.program_path = os.getcwd()

        # Definindo a aparência
        set_appearance_mode('dark')
        set_default_color_theme('dark-blue')

        # Definindo propriedades da janela
        self.app = CTk()
        self.app.title('WPP SCHEDULER')

        self.title()
        self.number_message()
        self.week_day()
        self.buttons()
        self.aviso()

        # Verifica se as dependências ja foram estabelecidas
        try:
            # Verifica se já há uma entrada no registro
            key = r'Software\Microsoft\Windows\CurrentVersion\Run'
            user = reg.ConnectRegistry(None, reg.HKEY_CURRENT_USER)
            key = reg.OpenKey(user, key)
            query = reg.QueryValueEx(key, 'sendMsgWPP')
            print('Registro Existe')
        except:
            # Cria data.json em APPDATA
            os.mkdir(self.appdata + r'\sendMsgWPP')
            with open(self.appdata + r'\sendMsgWPP\data.json', 'w') as file:
                file.write('[]')
            print('Diretório e data.json criados')

            # Copia e abre schedule_process.exe
            copy(self.program_path + r'\schedule_process.exe', self.appdata + r'\sendMsgWPP')
            os.startfile(self.appdata + r'\sendMsgWPP\schedule_process.exe')

            # Cria no registro uma chave para o schedule_process.exe caso não haja
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, reg.KEY_ALL_ACCESS)
            reg.SetValueEx(key, 'sendMsgWPP', 0, reg.REG_SZ, f'{self.appdata}\\sendMsgWPP\\schedule_process.exe')
            print('Registro criado')

        self.app.mainloop()

    def destroy_message(self, variable):
        variable.destroy()

    def title(self):
        label = CTkLabel(self.app, text='WPP SCHEDULER', font=("Arial Bold", 24))
        label.grid(column=0, row=0, padx=10, pady=(40, 20), columnspan=2)

    def number_message(self):
        # Frame
        frame = CTkFrame(self.app)
        frame.grid(padx=20, pady=20, column=0, row=1, sticky='nsw')

        # Adicionar label titulo
        label_titulo = CTkLabel(frame, text='Destinatário', font=('Arial Bold', 16))
        label_titulo.grid(column=0, row=0, padx=20, pady=(20,0), columnspan=2)

        # Adicionar label número
        label_numero = CTkLabel(frame, text='Número:')
        label_numero.grid(column=0, row=1, sticky='w', padx=(20, 0), pady=(20, 20))

        # Adicionar caixa de texto para o número
        self.entry_number = CTkEntry(frame, placeholder_text='Exemplo: +5515999999999', width=200)
        self.entry_number.grid(column=1, row=1, padx=(0, 20))

        # Adicionar Label para mensagens
        label_text = CTkLabel(frame, text='Mensagem:')
        label_text.grid(column=0, row=2, sticky='w', padx=20)

        # Adicionar caixa de texto
        self.txtbox_message = CTkTextbox(frame, height=300)
        self.txtbox_message.grid(column=0, row=3, sticky='nsew', columnspan=2, padx=20, wrap=None)

    def week_day(self):
        # Frame da Agenda
        frame_sch = CTkFrame(self.app)
        frame_sch.grid(padx=20, pady=20, ipady = 10, column=1, row=1, sticky='ns')

        # Adicionar Label Agenda
        label_sch = CTkLabel(frame_sch, text='Agendar', font=('Arial Bold', 16))
        label_sch.grid(column=0, row=0, padx=20, pady=20, columnspan=2)

        for i in range(len(self.semana)):
            dia = self.semana[i]

            chk_var = IntVar(value=0)  # Cria uma variável para as checkboxes
            self.checkbox_var.append(chk_var)

            timeVar = StringVar(value='00:00')  # Cria uma variável para a hora
            self.time_var.append(timeVar)

            repVar = IntVar(value=0)  # Cria uma variável para a repetição
            self.repeat_var.append(repVar)

            # Cria um frame para os dias e checkboxes
            frame_dia = CTkFrame(frame_sch)
            frame_dia.grid(padx=20, pady=(5, 5), column=0, row=i + 1)

            # Cria as checkboxes
            chk1 = CTkCheckBox(frame_dia, text=dia, variable=chk_var)
            chk1.grid(column=0, row=0, padx=(10, 0), pady=10)

            # Cria o entry para o horário
            hr = CTkEntry(frame_dia, placeholder_text='11:30', textvariable=timeVar)
            hr.grid(column=1, row=0, sticky='ew', padx=10, pady=10)

            # Cria as checkboxes para a repetição
            chk2 = CTkCheckBox(frame_dia, text='Repetir', variable=repVar)
            chk2.grid(column=2, row=0, padx=10, pady=10)

    def buttons(self):
        #Frane
        self.frame_buttons = CTkFrame(self.app)
        self.frame_buttons.grid(column=0, row=2, columnspan=2, pady=(0,20))

        # Cria um botão para agendar
        button = CTkButton(self.frame_buttons, text='Agendar', command=self.button_action)
        button.grid(column=0, row=0, padx=20, pady=20)

        # Cria um botão para ver os agendamentos
        button_agenda = CTkButton(self.frame_buttons, text='Agendamentos', command=Agenda)
        button_agenda.grid(column=1, row=0, padx=20, pady=20)

    def open_json(self):
        with open(self.appdata + r'\sendMsgWPP\data.json', 'r') as file:
            data = json.load(file)
        return data

    def add_data(self):
        data = self.open_json()
        counter = 0

        for i in range(len(self.semana)):
            if self.checkbox_var[i].get() == 1:
                # Variáveis
                numero_cel = self.entry_number.get().strip()
                mensagem = urllib.parse.quote( self.txtbox_message.get('1.0', END) ).strip()
                dia_semana = self.semana[i]
                horario = self.time_var[i].get().strip()
                repetir = self.repeat_var[i].get()

                # Verifica se o número está digitado corretamente:
                numero_lista = []
                wrong = 0
                for n in range(len(numero_cel)):
                    torf_num = numero_cel[n].isdigit()
                    if torf_num == True:
                        numero_lista.append(numero_cel[n])
                    else:
                        if numero_cel[n] != '+':
                            wrong = 1
                if len(numero_lista) != 13 or wrong == 1 or len(numero_cel) != 14:
                    error = CTkLabel(self.frame_buttons, text='Erro! Por favor, verifique as informações e tente novamente')
                    error.grid(column=0, row=1, padx=20, pady=(0, 20), columnspan=2)
                    error.after(3000, lambda: self.destroy_message(error))
                    break

                # Verifica se o horário está digitado corretamente:
                hora_lista = []
                wrong = 0
                for h in range(len(horario)):
                    torf = horario[h].isdigit()
                    if torf:
                        hora_lista.append(horario[h])
                    else:
                        if horario[h] != ':':
                            wrong = 1
                if int(''.join(hora_lista)[:2]) > 23 or int(''.join(hora_lista)[2:4]) > 59 or wrong == 1 or len(horario) != 5:
                    error = CTkLabel(self.frame_buttons, text='Erro! Por favor, verifique as informações e tente novamente')
                    error.grid(column=0, row=1, padx=20, pady=(0, 20), columnspan=2)
                    error.after(3000, lambda: self.destroy_message(error))
                    break

                # Se tudo estiver certo ele adicionará no data.json
                traduz_dia = {
                    'Segunda': 'monday',
                    'Terça': 'tuesday',
                    'Quarta': 'wednesday',
                    'Quinta': 'thursday',
                    'Sexta': 'friday',
                    'Sábado': 'saturday',
                    'Domingo': 'sunday'
                }
                adicionar = {
                    "num": numero_cel,
                    "message": mensagem,
                    "day": traduz_dia.get(dia_semana),
                    "time": horario,
                    "repeat": repetir
                }

                data.append(adicionar)

                with open(self.appdata + r'\sendMsgWPP\data.json', 'w') as file:
                    json.dump(data, file, indent=4)

                # Mensagem de sucesso
                sucesso = CTkLabel(self.frame_buttons, text='Mensagem agendada!')
                sucesso.grid(column=0, row=1, padx=20, pady=(0, 20), columnspan=2)
                sucesso.after(5000, lambda: self.destroy_message(sucesso))

            else:
                counter += 1

        if counter == 7:
            nenhuma_mensagem = CTkLabel(self.frame_buttons, text='Nenhum dia foi selecionado')
            nenhuma_mensagem.grid(column=0, row=1, padx=20, pady=(0, 20), columnspan=2)
            nenhuma_mensagem.after(3000, lambda: self.destroy_message(nenhuma_mensagem))

    def button_action(self):
        self.add_data()

    def aviso(self):
        aviso = CTkLabel(self.app, text_color='#737373', text='WPP SCHEDULER v1.0.0\nAVISO: Não mude de aba após a abertura do WhatsApp no navegador.')
        aviso.grid(column=0, row=3, columnspan=2, padx=20, pady=(0, 20))

if __name__ == '__main__':
    Interface()

# pyinstaller --onefile --icon=logo.ico --noconsole main.py
