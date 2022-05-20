import datetime
import os
import subprocess as sub
from tkinter import *
import threading as tr
import keyboard
import pyttsx3
import pywhatkit
import speech_recognition as sr
import wikipedia
from PIL import Image, ImageTk
from pygame import mixer

import color
import whatsapp as whapp

# Titulo y geometria del programa
main_window = Tk()
main_window.title("Juanita")
main_window.geometry("700x400")
main_window.resizable(False, False)
main_window.configure(bg='#00B4DB')
# Texto que aparece para saber que se puede hacer
comandos = """
- Comandos que se pueden usar:
    - Reproduce... (canción)
    - Busca... (información)
    - Abre... (Página web / App)
    - Alarma... (hora en 24hrs)
    - Archivo...(nombre)
    - Colores...(Reconocer color)
    - Escribe...(Block de notas)
    - Mensaje....(mensaje whatsapp)
    - Termina...(Deja de escuchar)
    - Cierra...(Cierra una app)
    - Ciérrate..(Cierra juanita)
"""
# Nombre que aparece del programa
label_title = Label(main_window, text="Juanita", bg="#6DD5FA",
                    fg="#2c3e50", font=('Arial', 30, 'bold'))
label_title.pack(pady=10)
# Dimensión para el texto de los comandos
canvas_comandos = Canvas(bg="#6dd5ed", height=210, width=205)
canvas_comandos.place(x=0, y=0)
canvas_comandos.create_text(100, 100, text=comandos,
                            fill="black", font='Arial 10')
# Dimensión para la caja de texto donde aparece lo que se busca
text_info = Text(main_window, bg="#00B4DB", fg="black")
text_info.place(x=0, y=200, height=250, width=210)
# Foto que aparece del programa
juanita_photo = ImageTk.PhotoImage(Image.open("juanita.jpg"))
windows_photo = Label(main_window, image=juanita_photo)
windows_photo.pack(pady=5)
engine = pyttsx3.init()

# Propiedades de las voces
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
engine.setProperty('rate', 125)
engine.setProperty('volume', 1)


# Función para cargar datos en los diccionarios
def charge_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                (key, val) = line.split(",")
                val = val.rstrip("\n")
                name_dict[key] = val
    except FileNotFoundError:
        pass


# Diccionarios de guardar
sites = dict()
charge_data(sites, "pages.txt")
files = dict()
charge_data(files, "archivos.txt")
programs = dict()
charge_data(programs, "apps.txt")
contacts = dict()
charge_data(contacts, "contacts.txt")


# Función para hablar

def talk(text):
    engine.say(text)
    engine.runAndWait()


# Función para escuchar

def listen(phrase=None):
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        talk(phrase)
        pc = listener.listen(source)
    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
    except sr.UnknownValueError:
        print("no entendí lo que dijiste, repitelo por favor")
    except sr.RequestError as e:
        print(
            "El servicio de Google no puede resolver la petición; {0}".format(e))
    return rec


# Funciones asociadas a las palabras claves

def reproduce(rec):
    music = rec.replace('reproduce', '')
    print("Reproduciendo" + music)
    talk("Reproduciendo" + music)
    pywhatkit.playonyt(music)


def busca(rec):
    search = rec.replace('busca', '')
    wikipedia.set_lang("es")
    wiki = wikipedia.summary(search, 1)
    talk(wiki)
    write_text(search + ": " + wiki)


def thread_alarma(rec):
    t = tr.Thread(target=clock, args=(rec,))
    t.start()


def colores(rec):
    talk("Enseguida")
    #color.capture() 
    t = tr.Thread(target=color.capture)


def abre(rec):
    task = rec.replace('abre', '').strip()

    if task in sites:
        for task in sites:
            if task in rec:
                sub.call(f'start chrome.exe {sites[task]}', shell=True)
                talk(f'Abriendo {task}')
    elif task in programs:
        for task in programs:
            if task in rec:
                talk(f'Abriendo {task}')
                os.startfile(programs[task])
    else:
        talk("perdón pero no tienes agregada la página, agregala")


def archivo(rec):
    file = rec.replace('archivo', '').strip()
    if file in files:
        for file in files:
            if file in rec:
                sub.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
    else:
        talk("perdón pero no tienes agregado el archivo , agregalo")


def escribe(rec):
    try:
        with open("nota.txt", 'a') as f:
            write(f)
    except FileNotFoundError:
        file = open("nota.txt", 'a')
        write(file)


def enviar_mensaje(rec):
    talk("¿A quién se le enviará el mensaje?")
    contact = listen("te escucho...")
    contact = contact.strip()
    print(contact)
    if contact in contacts:
        for cont in contacts:
            if cont == contact:
                contact = contacts[cont]
                talk("¿qué mensaje quieres enviar?")
                message = listen("te escucho..")
                talk("enviando mensaje...")
                whapp.send_message(contact, message)
    else:
        talk("parece que aún no haz agregado a este contacto, favor de agregarlo")


def cierra(rec):
    for task in programs:
        kill_task = programs[task].split('\\')
        kill_task = kill_task[-1]
        if task in rec:
            sub.call(f"TASKKILL /IM {kill_task} /F", shell=True)
            talk(f'Cerrando {task}')
    if 'ciérrate' in rec:
        talk("hasta luego")
        sub.call(f"TASKKILL /IM juanita.exe /F", shell=True)


def clock(rec):
    num = rec.replace('alarma', '')
    num = num.strip()
    talk("Alarma activada a las" + num + "horas")
    if num[0] != '0' and len(num) < 5:
        num = '0' + num
    print(num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            print("Despierta")
            mixer.init()
            mixer.music.load("la_bomba.mp3")
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == "s":
            mixer.music.stop()
            break


# Diccionario con palabras claves
key_words = {
    'reproduce': reproduce,
    'busca': busca,
    'alarma': thread_alarma,
    'colores': colores,
    'abre': abre,
    'archivo': archivo,
    'escribe': escribe,
    'mensaje': enviar_mensaje,
    'cierra': cierra,
    'ciérrate': cierra
}


# Función principal

def run_juanita():
    while True:
        try:
            rec = listen("te escucho...")
        except UnboundLocalError:
            talk("no entendí lo que dijiste, repitelo")
            continue
        if 'busca' in rec:
            key_words['busca'](rec)
        else:
            for word in key_words:
                if word in rec:
                    key_words[word](rec)
        if 'termina' in rec:
            talk("adios")
            break
    main_window.update()


def write(f):
    talk("¿Qué desea escribir?")
    rec_write = listen("te escucho...")
    f.write(rec_write + os.linesep)
    f.close()
    talk("Se ha escrito correctamente")
    sub.Popen("nota.txt", shell=True)


# Funciones para las voces
def mexican_voice():
    change_voice(0)


def spanish_voice():
    change_voice(1)


def english_voice():
    change_voice(2)


# Función para cambiar las voces
def change_voice(id):
    engine.setProperty('voices', voices[id].id)
    engine.setProperty('rate', 125)
    engine.setProperty('volume', 1)
    talk("hola soy juanita")


def read_and_talk():
    text = text_info.get("1.0", "end")
    talk(text)


def write_text(text_wiki):
    text_info.insert(INSERT, text_wiki)


# Funciones para abrir nuevas ventanas

def open_w_files():
    global namefile_entry, pathf_entry
    windows_files = Toplevel()
    windows_files.title("Agregar archivos")
    windows_files.configure(bg="#434343")
    windows_files.geometry("300x200")
    windows_files.resizable(False, False)
    main_window.eval(f'tk::PlaceWindow {str(windows_files)} center')

    title_label = Label(windows_files, text="Agrega un archivo", fg="white", bg="#434342", font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)
    name_label = Label(windows_files, text="Nombre del archivo", fg="white", bg="#434342", font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)

    namefile_entry = Entry(windows_files)
    namefile_entry.pack(pady=1)

    path_label = Label(windows_files, text="Ruta del archivo", fg="white", bg="#434342", font=('Arial', 10, 'bold'))
    path_label.pack(pady=2)

    pathf_entry = Entry(windows_files, width=35)
    pathf_entry.pack(pady=1)

    save_button = Button(windows_files, text="Guardar", bg='#16222A', fg="white", width=8, height=1, command=add_files)
    save_button.pack(pady=4)


def open_w_apps():
    global nameapp_entry, patha_entry
    windows_apps = Toplevel()
    windows_apps.title("Agregar apps")
    windows_apps.configure(bg="#434343")
    windows_apps.geometry("300x200")
    windows_apps.resizable(False, False)
    main_window.eval(f'tk::PlaceWindow {str(windows_apps)} center')

    title_label = Label(windows_apps, text="Agrega una app", fg="white", bg="#434342", font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)
    name_label = Label(windows_apps, text="Nombre de la app", fg="white", bg="#434342", font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)

    nameapp_entry = Entry(windows_apps)
    nameapp_entry.pack(pady=1)

    path_label = Label(windows_apps, text="Ruta de la app", fg="white", bg="#434342", font=('Arial', 10, 'bold'))
    path_label.pack(pady=2)

    patha_entry = Entry(windows_apps, width=35)
    patha_entry.pack(pady=1)

    save_button = Button(windows_apps, text="Guardar", bg='#16222A', fg="white", width=8, height=1, command=add_apps)
    save_button.pack(pady=4)


def open_w_pages():
    global namepages_entry, pathp_entry
    windows_pages = Toplevel()
    windows_pages.title("Agregar páginas")
    windows_pages.configure(bg="#434343")
    windows_pages.geometry("300x200")
    windows_pages.resizable(False, False)
    main_window.eval(f'tk::PlaceWindow {str(windows_pages)} center')

    title_label = Label(windows_pages, text="Agrega una página web", fg="white", bg="#434342", font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)
    name_label = Label(windows_pages, text="Nombre de la página", fg="white", bg="#434342", font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)

    namepages_entry = Entry(windows_pages)
    namepages_entry.pack(pady=1)

    path_label = Label(windows_pages, text="Ruta de la página", fg="white", bg="#434342", font=('Arial', 10, 'bold'))
    path_label.pack(pady=2)

    pathp_entry = Entry(windows_pages, width=35)
    pathp_entry.pack(pady=1)

    save_button = Button(windows_pages, text="Guardar", bg='#16222A', fg="white", width=8, height=1, command=add_pages)
    save_button.pack(pady=4)


def open_w_contacts():
    global namecontact_entry, phone_entry
    windows_contacts = Toplevel()
    windows_contacts.title("Agregar Contactos")
    windows_contacts.configure(bg="#434343")
    windows_contacts.geometry("300x200")
    windows_contacts.resizable(False, False)
    main_window.eval(f'tk::PlaceWindow {str(windows_contacts)} center')

    title_label = Label(windows_contacts, text="Agrega un contacto", fg="white", bg="#434342", font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)
    name_label = Label(windows_contacts, text="Nombre del contacto:", fg="white", bg="#434342", font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)

    namecontact_entry = Entry(windows_contacts)
    namecontact_entry.pack(pady=1)

    path_label = Label(windows_contacts, text="Número del contacto:", fg="white", bg="#434342", font=('Arial', 10, 'bold'))
    path_label.pack(pady=2)

    phone_entry = Entry(windows_contacts, width=35)
    phone_entry.pack(pady=1)

    save_button = Button(windows_contacts, text="Guardar", bg='#16222A', fg="white", width=8, height=1, command=add_contacts)
    save_button.pack(pady=4)


# Funciones para añadir cosas

def add_files():
    name_file = namefile_entry.get().strip()
    path_file = pathf_entry.get().strip()

    files[name_file] = path_file
    save_data(name_file, path_file, "archivos.txt")
    namefile_entry.delete(0, "end")
    pathf_entry.delete(0, "end")


def add_apps():
    name_file = nameapp_entry.get().strip()
    path_file = patha_entry.get().strip()

    programs[name_file] = path_file
    save_data(name_file, path_file, "apss.txt")
    nameapp_entry.delete(0, "end")
    patha_entry.delete(0, "end")


def add_pages():
    name_pages = namepages_entry.get().strip()
    url_pages = pathp_entry.get().strip()

    sites[name_pages] = url_pages
    save_data(name_pages, url_pages, "pages.txt")
    namepages_entry.delete(0, "end")
    pathp_entry.delete(0, "end")


def add_contacts():
    name_contacts = namecontact_entry.get().strip()
    phone = phone_entry.get().strip()

    contacts[name_contacts] = phone
    save_data(name_contacts, phone, "contacts.txt")
    namecontact_entry.delete(0, "end")
    phone_entry.delete(0, "end")


# Función para guardar datos en los archivos

def save_data(key, value, filename):
    try:
        with open(filename, 'a') as f:
            f.write(key + "," + value + "\n")
    except FileNotFoundError:
        file = open(filename, 'a')
        file.write(key + "," + value + "\n")


# Funciones para decir que se tiene agregado

def talk_pages():
    if bool(sites):
        talk("Haz agregado las siguientes páginas web")
        for site in sites:
            talk(site)
    else:
        talk("Aún no haz agregado páginas web")


def talk_apps():
    if bool(programs):
        talk("Haz agregado las siguientes aplicaciones")
        for program in programs:
            talk(program)
    else:
        talk("Aún no haz agregado aplicaciones")


def talk_files():
    if bool(files):
        talk("Haz agregado los siguientes archivos")
        for file in files:
            talk(file)
    else:
        talk("Aún no haz agregado archivos")


def talk_contacts():
    if bool(contacts):
        talk("Haz agregado los siguientes contactos")
        for contact in contacts:
            talk(contact)
    else:
        talk("Aún no haz agregado contactos")


# Funciones para saludar al inicio

def give_me_name():
    talk("Hola, ¿cúal es tu nombre?")
    nombe = listen("Te escucho...")
    nombe = nombe.strip()
    talk(f"Bienvenido{nombe}")
    try:
        with open("name.txt", 'w') as f:
            f.write(nombe)
    except FileNotFoundError:
        file = open("name.txt", 'w')
        file.write(nombe)


def say_hello():
    if os.path.exists("name.txt"):
        with open("name.txt") as f:
            for line in f:
                talk(f"Hola, bienvenido {line}")
    else:
        give_me_name()


def thread_hello():
    t = tr.Thread(target=say_hello)
    t.start()


thread_hello()

# Botones para las voces

button_voice_mx = Button(main_window, text="Voz México", fg="white", bg="#45a247", font=("Arial", 12, "bold"), command=mexican_voice)
button_voice_mx.place(x=500, y=10, width=100, height=30)
button_voice_es = Button(main_window, text="Voz España", fg="white", bg="#f12711", font=("Arial", 12, "bold"), command=spanish_voice)
button_voice_es.place(x=500, y=45, width=100, height=30)
button_voice_us = Button(main_window, text="Voz USA", fg="white", bg="#4286f4", font=(
    "Arial", 12, "bold"), command=english_voice)
button_voice_us.place(x=500, y=80, width=100, height=30)

# Boton principal

button_listen = Button(main_window, text="Escuchar", fg="white", bg="#1565C0", font=("Arial", 15, "bold"), width=20, height=1, command=run_juanita)
button_listen.pack(side=BOTTOM, pady=5)

# Boton para hablar

button_speak = Button(main_window, text="Hablar", fg="white", bg="#00B4DB", font=("Arial", 12, "bold"), command=read_and_talk)
button_speak.place(x=500, y=120, width=100, height=30)

# Botones para agregar cosas

button_add_files = Button(main_window, text="Agregar archivos", fg="white", bg="#4286f4", font=("Arial", 9, "bold"), width=20, height=3, command=open_w_files)
button_add_files.place(x=500, y=160, width=100, height=30)
button_add_apss = Button(main_window, text="Agregar apps", fg="white", bg="#4286f4", font=("Arial", 10, "bold"), width=20, height=3, command=open_w_apps)
button_add_apss.place(x=500, y=200, width=100, height=30)
button_add_pages = Button(main_window, text="Agregar paginas", fg="white", bg="#4286f4", font=("Arial", 9, "bold"), width=20, height=3, command=open_w_pages)
button_add_pages.place(x=500, y=240, width=100, height=30)
button_add_contacts = Button(main_window, text="Agregar contactos", fg="white", bg="#4286f4", font=("Arial", 7, "bold"), width=20, height=3, command=open_w_contacts)
button_add_contacts.place(x=500, y=280, width=100, height=30)

# Botones para saber que se tiene agregado

button_tell_pages = Button(main_window, text="Páginas agregadas", fg="white", bg="#2c3e50", font=("Arial", 6, "bold"), width=20, height=3, command=talk_pages)
button_tell_pages.place(x=210, y=280, width=90, height=30)

button_tell_apps = Button(main_window, text="Aplicaciones agregadas", fg="white", bg="#2c3e50", font=("Arial", 6, "bold"), width=20, height=3, command=talk_apps)
button_tell_apps.place(x=300, y=280, width=100, height=30)

button_tell_files = Button(main_window, text="Archivos agregados", fg="white", bg="#2c3e50", font=("Arial", 6, "bold"), width=20, height=3, command=talk_files)
button_tell_files.place(x=400, y=280, width=90, height=30)
button_tell_contacts = Button(main_window, text="Contactos agregados", fg="white", bg="#2c3e50", font=("Arial", 6, "bold"), width=15, height=2, command=talk_contacts)
button_tell_contacts.pack(side=BOTTOM, pady=1)

main_window.mainloop()
