import json
from customtkinter import *
from urllib.parse import unquote
import time
import psutil

class Agenda:
    def __init__(self):
        self.delete = []
        self.appdata = os.environ['APPDATA'] + r'\sendMsgWPP'

        # Definindo a aparência
        set_appearance_mode('dark')
        set_default_color_theme('dark-blue')

        self.root = CTk()
        self.root.title('Agenda')

        self.title = CTkLabel(self.root, text='AGENDA', font=('Arial Bold', 24))
        self.title.grid(column=0, row=0, padx=20, pady=(20,0))

        self.read_data()
        self.execute_button()

        self.root.mainloop()

    def open_json(self):
        with open(self.appdata + r'\data.json', 'r') as file:
            data = json.load(file)
        return data

    def delete_msgs(self):
        data = self.open_json()
        new_data = []
        tobe_deleted = []

        # Filtra as mensagens a serem deletadas
        for i, element in enumerate(self.delete):
            info = element.get()
            tobe_deleted.append(info)

        # Cria um novo banco de dados com apenas os elementos que irão permanecer
        for i, entry in enumerate(data):
            if tobe_deleted[i] == 1:
                pass
            else:
                new_data.append(entry)

        with open(self.appdata + r'\data.json', 'w') as file:
            json.dump(new_data, file, indent=4)

        self.root.destroy()
        time.sleep(1)
        Agenda()

    def read_data(self):
        data = self.open_json()
        traduz_dia = {
            'monday': 'Segunda',
            'tuesday': 'Terça',
            'wednesday': 'Quarta',
            'thursday': 'Quinta',
            'friday': 'Sexta',
            'saturday': 'Sábado',
            'sunday': 'Domingo'
        }

        if len(data) > 0:
            frame_scrl = CTkScrollableFrame(self.root, width=780, height=440, fg_color="#292929")
            frame_scrl.grid(column=0, row=1, padx=20, pady=20)

            for i, element in enumerate(data):
                numero = element['num']
                msg = unquote(element['message'])
                time_sc = element['time']
                day = traduz_dia.get(element['day'])
                repeat = element['repeat']
                
                frame = CTkFrame(frame_scrl)
                frame.grid(column=0, row=i, padx=10, pady=10, sticky='we')
                
                # Number Label
                num_label = CTkLabel(frame, text=numero)
                num_label.grid(column=0, row=0, padx=10, pady=10)
                
                # Message box
                msg_txtbox = CTkTextbox(frame, width=200, height=50)
                msg_txtbox.insert('0.0', msg)
                msg_txtbox.configure(state='disabled')
                msg_txtbox.grid(column=1, row=0, padx=10, pady=10)
                
                # Time Day
                time_label = CTkLabel(frame, text=f'{day} às {time_sc}', width=120, anchor='w')
                time_label.grid(column=2, row=0, padx=10, pady=10)
                
                # Repeat
                repetir_checkbox = CTkCheckBox(frame, text='Repetir')
                repetir_checkbox.grid(column=3, row=0, padx=10, pady=10)
                if repeat == 1:
                    repetir_checkbox.select()
                repetir_checkbox.configure(state='disabled')
                
                # Delete Button
                delete_var = IntVar(value=0)
                self.delete.append(delete_var)

                frame_delete = CTkFrame(frame_scrl)
                frame_delete.grid(column=1, row=i, padx=10, pady=10)
                delete_checkbox = CTkCheckBox(frame_delete, text='Deletar', variable=delete_var)
                delete_checkbox.grid(column=0, row=0, padx=20, pady=23)

        else:
            frame_empty = CTkFrame(self.root)
            frame_empty.grid(column=0, row=1, padx=20, pady=20)
            empty_label = CTkLabel(frame_empty, text='Não há mensagens agendadas', font=('Arial Bold', 16))
            empty_label.grid(column=0, row=0, padx=40, pady=40)

    def execute_button(self):
        data = self.open_json()
        if len(data) > 0:
            button_delete = CTkButton(self.root, text='DELETAR SELECIONADOS', font=('Arial Bold', 16), command=self.delete_msgs)
            button_delete.grid(column=0, row=2, padx=20, pady=(0,20), ipadx=10, ipady=10)
