import openai, time , json, os
from tkinter import filedialog, simpledialog
import ttkbootstrap as ttk
from collections import deque

his_deque = deque(maxlen=10)
last_prompt=""
model = "text-davinci-003"
max_tokens = 512

def status(state="", wait=True):
    status_label.config(text=state)
    window.update()
    if wait: time.sleep(1)
    
def save():
    status("Saving...",False)
    file_path = filedialog.askopenfilename(defaultextension=".json")
    with open(file_path, "w") as f:
        json.dump(list(his_deque), f)
    status()
    
def load():
    status("Loading", False)
    window.update()
    try:
        file_path = filedialog.askopenfilename()
        with open(file_path, 'r') as f:
            his_deque.clear()
            his_deque.extend(json.load(f))
            Update()
        status("Loaded")
        status(wait=False)
    except FileNotFoundError:
        pass
        status(wait=False)

def clear():
    status("Clearing...")
    his_deque.clear()
    Update()
    status(wait=False)
    
def set_api(event= None):
    try:
        file_path = filedialog.askopenfilename()
        with open(file_path,"r") as f:
            openai.api_key = f.read()
        api_button.config(bootstyle="default")
        window.update()
    except FileNotFoundError:
        api_button.config(bootstyle="danger")

def Regenerate():
    status("Regenerating")
    try:
        regenerate_button.config(text="=*=")    
        his_deque.pop()
        Update()
        Chat()  
        Update()
    except IndexError:
        regenerate_button.config(text="There is no request to regenerate yet.")
    status()
    
def Update():
    status_label.config(text="")
    window.update()
    history = "\n\n".join(list(his_deque))
    conversation_box.config(state="normal") 
    conversation_box.delete("1.0","end")
    conversation_box.insert("end",history)
    conversation_box.config(state="disabled")
    regenerate_button.config(text="=*=")
    window.update() 
    
def Send(event=None):
    status("Sending...",wait=False)
    send_button.config(state="disabled")
    global last_prompt
    last_prompt = input_box.get()
    his_deque.append("User: "+ last_prompt)
    input_box.delect(0,"end")
    Update()
    Chat()
    send_button.config(state="normal")
    
def Chat():
    status("Responding", False)
    global generation
    global history
    history = "\n\n".join(list(his_deque))
    time.sleep(2)
    try:
        generation=openai.Completion.create(prompt=history+"Assistant: ", model=model, max_tokens=max_tokens).choices[0].text
        Update()
        his_deque.append("Assistant: "+generation.strip())
        conversation_box.config(state="normal")
        conversation_box.insert("end","\n\n")
        for character in "Assistant: "+generation.strip():
            time.sleep(0.05)
            conversation_box.insert("end",character)
            window.update()
        conversation_box.config(state="disabled")
    except:
        regenerate_button.config(text="There was an error. Try again?")
    status()
    
    
    #Create window
window=ttk.Window(themename="darkly")
window.title("ChatGP3")
top_bar=ttk.Frame(window, height=25).pack(anchor="n", expand=True, fill="both")
save_button=ttk.Button(top_bar, text="Save",command=save).place(relx=0.0,rely=0)
load_button=ttk.Button(top_bar, text="Load", command=load).place(relx=0.1,rely=0)
clear_button=ttk.Button(top_bar, text="Clear", command=clear).place(relx=0.9,rely=0)
api_button=ttk.Button(top_bar, text="Set API Path", command=set_api, bootstyle="default")
api_button.place(relx=0.2,rely=0)
status_label=ttk.Label(top_bar, text="")
status_label.place(relx=0.5,rely=0.0)
conversation_box=ttk.Text(window, wrap="word",state="disabled")
regenerate_button=ttk.Button(window, text="♻️", command=Regenerate)
conversation_box.pack(expand=True)
regenerate_button.place(in_=conversation_box, relx=0.5, rely=1.0, anchor="s")
input_bar=ttk.Frame().pack() 
input_box=ttk.Entry(input_bar)
input_box.pack(side="left",fill="x",expand=True)
send_button=ttk.Button(input_bar, text="Send", command=Send)
window.bind("<Return>",Send)
send_button.pack(side="right")

#set up openAI API KEY
if os.path.exists("openai_key.txt"):
    with open("openai_key.txt","r") as f:
        openai.api_key=f.read()
    api_button.config(bootstyle="default")
else:
    api_button.config(bootstyle="danger")
    
window.mainloop()