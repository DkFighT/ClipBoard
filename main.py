import customtkinter as ct, keyboard, time, pyperclip
from tkinter import Tk

clipboard = []
buttons = []

class Button():
    def __init__(self, main_target, target, text):
        self.target = target
        self.main_target = main_target
        self.text = text
        self.btn = ct.CTkButton(self.target, text=self.text, command=self.copy_text, width=280, height=50, anchor='nw', border_spacing=5)

    def copy_text(self):
        pyperclip.copy(self.btn.cget('text'))
        self.main_target.destroy()
        keyboard.press('ctrl+v')
        keyboard.release('ctrl+v')

    def update_btn(self):
        self.btn.pack(pady=(10, 0), padx=10)

class App(ct.CTk):
    def __init__(self):
        super().__init__()

        ct.set_appearance_mode('System')
        ct.set_default_color_theme('blue')
        self.title('ClipBoard')
        self.geometry('300x410')
        self.resizable(True, False)
        self.maxsize(1000, 400)
        self.minsize(300, 400)

        self.frame = ct.CTkScrollableFrame(self, height=400)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky="ew")

        self.set_plates()
        self.mainloop()

    def set_plates(self):
        buttons.clear()
        for i in range(len(clipboard)):
            buttons.append(Button(self, self.frame, clipboard[i]))
            buttons[i].update_btn()

def set_clipboard():
    global clipboard
    a = Tk()
    data = a.clipboard_get()
    a.destroy()
    print(type(data))
    clipboard.append(data)
    temp = []
    for i in clipboard:
        if i not in temp:
            temp.append(i)
    clipboard = temp
    print(clipboard)

def main():
    global app
    recent_value = ""
    while True:
        tmp_value = pyperclip.paste()
        if tmp_value != recent_value:
            recent_value = tmp_value
            set_clipboard()
        if (keyboard.is_pressed('win+v')):    
            app = App()
        time.sleep(0.05)

if __name__ == '__main__':
    main()
