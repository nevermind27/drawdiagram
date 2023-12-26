import PySimpleGUI as sg
import random
import os.path
import interface
import random
import glob

sg.theme('BlueMono')
langs=['Python','C++']
types=['Объектный','Функциональный']
column = [[sg.Image(key="-IMAGE-")]]
right_part=[[sg.Frame('Вывод диаграммы',[
    [sg.Column(column, size=(500, 500), scrollable=True, key='Column')]],size=(500,500))]]
left_part=[[sg.Frame('Ввод кода',[
     [sg.Text("Выбрать существующий файл"),
     sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
     sg.FolderBrowse("Обзор"),],
     [sg.Multiline(key='text', size=(60,20), autoscroll=True)],
     [sg.Text("Введите название функции"),sg.In(size=(25, 1), enable_events=True, key="function")],
     [sg.Text("Выберите язык"),sg.Combo(langs,expand_x=True, enable_events=True,  readonly=False, key='-COMBO-')],
     [sg.Text("Выберите подход"),sg.Combo(types,expand_x=True, enable_events=True,  readonly=False, key='-COMBO2-')],
     [sg.Button('Построить диаграмму', enable_events=True, key='-FUNCTION-', font='Helvetica 16')]],size=(500,500))]]

layout = [
    [sg.Column(left_part), sg.VSeperator(), sg.Column(right_part)],
]

# рисуем окно
window = sg.Window('drawdiagram', layout)
file=0
# запускаем основной бесконечный цикл
while True:
    # получаем события, произошедшие в окне
    event, values = window.read()
    # если нажали на крестик
    if event in (sg.WIN_CLOSED, 'Exit'):
        # выходим из цикла
        break
    # если нажали на кнопку
    if event == '-FUNCTION-':
        # запускаем связанную функцию
        name =str(random.randint(1,1000))
        #if file:
         #   interface.read_code(values['FOLDER'],values['function'],name,values['-COMBO2-'],values['-COMBO-'])
        #else:
        interface.read_code(values['text'],values['function'],name,values['-COMBO2-'],values['-COMBO-'])
        file1=r'C:\Users\User\Downloads\py'
        end='.png'
        filename=file1+name+end
        list_of_files = glob.glob(r'C:\Users\User\Downloads\*')
        latest_file = max(list_of_files, key=os.path.getctime)
        os.rename(latest_file,filename)
        window["-IMAGE-"].update(filename=filename)
        window.refresh()
        # Update for scroll area of Column element
        window['Column'].contents_changed()
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
            file=1
        except:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".py"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
            window["-TEXT-"].update(filename)

        except:
            pass
# закрываем окно и освобождаем используемые ресурсы
window.close()
