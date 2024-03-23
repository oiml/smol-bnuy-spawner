import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import configparser
import threading
import time
import socket
import pathlib
import os
from emoji import demojize

MonsterDB = {}
SpawnDB = []

Write_Timer = 0
Write_Timer_interval = 1

Twitch_EvalTimer = 0
Twitch_EvalTimer_interval = 0.5
Socket_Buffersize = 2048

#defaults
input_file_path = "monster db.ini"
output_file_path = ""

Twitch_server = "irc.chat.twitch.tv"
Twitch_port = 6667
Twitch_nickname = ""
Twitch_token = ""
Twitch_channel = ""

quit = False

def write_spawnfile():
    # Write spawns every Write_Timer_interval seconds
    global quit, SpawnDB
    while(True):
        if(quit):
            print("Exiting Spawner")
            return
        save_spawnfile()
        time.sleep(Write_Timer_interval)

def evaluate_GREASEGOBLINS(): # AKA Twitch chat
    global quit
    global Twitch_server, Twitch_port, Twitch_nickname, Twitch_token, Twitch_channel
    # read grease goblins from twitch chat
    configuration_fail = True
    while(configuration_fail):
        if(Twitch_server == "" or Twitch_nickname == "" or Twitch_token == "" or Twitch_channel == ""):
            print("Config Error, retrying in 5 seconds...")
            return
        else:
            configuration_fail = False
    
    sock = socket.socket()

    sock.settimeout(10)
    sock.connect((Twitch_server, Twitch_port))
    sock.settimeout(None)
    sock.send(f"PASS {Twitch_token}\n".encode('utf-8'))
    sock.send(f"NICK {Twitch_nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {Twitch_channel}\n".encode('utf-8'))
    sock.setblocking(False)
    
    while(True):
        if(quit):
            sock.close()
            print("Quitting Twitch...")
            return
        try:
            resp = sock.recv(Socket_Buffersize).decode('utf-8')

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))

            elif len(resp) > 0: #proper message, get username
                username, message = resp.split("!",1)
                username = username.replace(":","") 
                #got username, now eval message
                try:
                    crap, message = message.lower().split(Twitch_channel,1)
                    # write into output DB here
                    if "!spawn " in message:
                            substr1, substr2 = message.split("!spawn ",1)
                            add_to_spawn_list(substr2)
                            print("SPAWN DETECTED" + substr2)
                except:
                    print(resp)
        except:
            pass
            
        time.sleep(Twitch_EvalTimer_interval)

def save_config():
    config = configparser.ConfigParser()
    config['FILES'] = {'DB_file': entry_file_path.get().rsplit('\\',1)[1], 'Spawnfile': entry_save_path.get()}
    config['TWITCH'] = {'Twitch_server': Twitch_server, 'Twitch_port': Twitch_port, 'Twitch_nickname': Twitch_nickname, 'Twitch_token':Twitch_token, 'Twitch_channel': Twitch_channel}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def load_config():
    config = configparser.ConfigParser()
    try:
        config.read(os.path.join(os.getcwd(),'config.ini'))
    except KeyError:
        if os.path.exists(os.path.join(os.getcwd(),'config.ini')):
            print("Config file error.")
        else:
            status_label.config(text="No config found. Creating..")
            save_config()
    try:
        global Twitch_server, Twitch_port, Twitch_nickname, Twitch_token, Twitch_channel
        input_file_path = config['FILES']['DB_file']
        input_file_path = os.path.join(os.getcwd(),input_file_path)
        output_file_path = config['FILES']['Spawnfile']
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(tk.END, input_file_path)
        entry_save_path.delete(0, tk.END)
        entry_save_path.insert(tk.END, output_file_path)
        Twitch_server = config['TWITCH']['Twitch_server']
        Twitch_port = int(config['TWITCH']['Twitch_port'])
        Twitch_nickname = config['TWITCH']['Twitch_nickname']
        Twitch_token = config['TWITCH']['Twitch_token']
        Twitch_channel = config['TWITCH']['Twitch_channel']
        read_file(input_file_path)
    except KeyError:
        pass

    

def read_file(file_path):
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(tk.END, file_path)
        try:
            with open(file_path, 'r') as file:
                text = file.readlines()
                listbox.delete(0, tk.END)
                for line in text:
                    Monster_name, Monster_uuid = line.strip().split(',')
                    MonsterDB[Monster_name.lower()] = Monster_uuid
                    listbox.insert(tk.END,Monster_name)
        except FileNotFoundError:
            status_label.config(text="File not found.")

def load_file():
    file_path = filedialog.askopenfilename()
    read_file(file_path)

def move_selected(): #not needed anymore, testing remnant
    selected_indices = listbox.curselection()
    if len(selected_indices) == 1:
        line = listbox.get(selected_indices[0])
        option = selected_option.get()
        if option == "now":
            line += " now"
        elif option == "next combat":
            line += " combat"
        add_to_spawn_list(line)
        print("adding " + line)
        #listbox_selected.insert(tk.END, line)
    elif len(selected_indices) > 1:
        status_label.config(text="Please select only one item.")
    else:
        status_label.config(text="No item selected.")

def save_spawnfile():
    global SpawnDB
    file_path = entry_save_path.get()
    if (file_path != ""):
        spawnstring = ""
        for entry in SpawnDB:
          print("Spawning: "+entry+"\n")
          spawnstring = spawnstring + entry + "\n"
    
        SpawnDB = []
        with open(file_path, 'a') as file:
            file.write(spawnstring)

    #listbox_selected.delete(0, tk.END)
    #status_label.config(text="Spawnfile saved successfully.")

def spawnfileselector():
    entry_save_path.delete(0, tk.END)
    entry_save_path.insert(tk.END, filedialog.asksaveasfilename())

def add_to_spawn_list(monster):
    try:
        name, spawntype = monster.split(" ",1)
        name = "".join(filter(str.isalpha, name))
        spawntype = "".join(filter(str.isalpha, spawntype))
        print(name + " " + spawntype)
    except:
        print("wut")
        pass
    if(spawntype == "now"):
        try:
            # monster exists in DB
            SpawnDB.append(MonsterDB[name.lower()] + ",now")
            print("UUID " + MonsterDB[name.lower()] + ",now inserted into SpawnDB")
            listbox_selected.insert(tk.END, name+",now")
        except: #doesn't exist
            pass
    if(spawntype == "later"):
        try:
            SpawnDB.append(MonsterDB[name.lower()] + ",combat")
            print("UUID " + MonsterDB[name.lower()] + ",combat inserted into SpawnDB")
            listbox_selected.insert(tk.END, name+",combat")
        except:
            pass

def on_closing():
    global quit
    quit = True
    save_config()
    Write_Thread.join()
    Twitch_Thread.join()
    root.quit()

# Create main window
root = tk.Tk()
root.title("SMOL BNUY SPAWNER")

root.protocol("WM_DELETE_WINDOW", on_closing)

# Frame for saving file
frame_save = tk.Frame(root)
frame_save.pack(pady=0)

frame_save_helper = tk.Frame(root)
frame_save_helper.pack(pady=0)

label_save_path_helper = tk.Label(frame_save_helper, text="Usually in %localappdata%\Larian Studios\Baldur's Gate 3\Script Extender")
label_save_path_helper.pack(side=tk.LEFT)

label_save_path = tk.Label(frame_save, text="Spawning File:")
label_save_path.pack(side=tk.LEFT)

entry_save_path = tk.Entry(frame_save, width=50)
entry_save_path.pack(side=tk.LEFT, padx=10)

btn_save_browse = tk.Button(frame_save, text="Browse", command=spawnfileselector)
btn_save_browse.pack(side=tk.LEFT)

# Frame for loading file
frame_load = tk.Frame(root)
frame_load.pack(pady=10)

label_file_path = tk.Label(frame_load, text="Monster DB:")
label_file_path.pack(side=tk.LEFT)

entry_file_path = tk.Entry(frame_load, width=50)
entry_file_path.pack(side=tk.LEFT, padx=10)

btn_browse = tk.Button(frame_load, text="Browse", command=load_file)
btn_browse.pack(side=tk.LEFT)

# Frame for displaying file content
frame_display = tk.Frame(root)
frame_display.pack(pady=10, fill=tk.BOTH, expand=True)

# Original content listbox
frame_original = tk.Frame(frame_display)
frame_original.pack(side=tk.LEFT, padx=10)

btn_reload = tk.Button(root, text="Reload DB", command=load_config)
btn_reload.pack(side=tk.LEFT, padx=10)

label_original = tk.Label(frame_original, text="Available Enemies")
label_original.pack()

scrollbar_original = tk.Scrollbar(frame_original, orient=tk.VERTICAL)
scrollbar_original.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame_original, yscrollcommand=scrollbar_original.set, selectmode=tk.SINGLE, width=60, height=40)
listbox.pack(fill=tk.BOTH, expand=True)
scrollbar_original.config(command=listbox.yview)

# Move Selected button
btn_move = tk.Button(frame_display, text="➡", command=move_selected)
btn_move.pack(side=tk.LEFT, padx=10)

# Dropdown menu for append options
append_options = ["now", "next combat"]
selected_option = tk.StringVar()
selected_option.set(append_options[0])  # Default value

append_menu = ttk.Combobox(frame_display, textvariable=selected_option, values=append_options)
append_menu.pack(side=tk.LEFT)

# Selected content listbox
frame_selected = tk.Frame(frame_display)
frame_selected.pack(side=tk.RIGHT, padx=10)

label_selected = tk.Label(frame_selected, text="Queued Enemies")
label_selected.pack()

scrollbar_selected = tk.Scrollbar(frame_selected, orient=tk.VERTICAL)
scrollbar_selected.pack(side=tk.RIGHT, fill=tk.Y)

listbox_selected = tk.Listbox(frame_selected, yscrollcommand=scrollbar_selected.set, selectmode=tk.MULTIPLE, width=60, height=40)
listbox_selected.pack(fill=tk.BOTH, expand=True)
scrollbar_selected.config(command=listbox_selected.yview)

# Frame for buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

# Status label
status_label = tk.Label(root, text="", fg="green")
status_label.pack(pady=10)

load_config()

Write_Thread = threading.Thread(target=write_spawnfile)
Twitch_Thread = threading.Thread(target=evaluate_GREASEGOBLINS)

Write_Thread.start()
Twitch_Thread.start()

root.mainloop()
