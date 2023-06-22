import customtkinter as ct, keyboard, time, pyperclip, win32clipboard
from textwrap import wrap
from PIL import ImageGrab, ImageTk
from io import BytesIO

clipboard = []
buttons = []

class Button():
    def __init__(self, main_target, target, text, img, index):
        self.target = target
        self.main_target = main_target
        self.text = text
        self.index = index
        self.img = img
        self.btn = ct.CTkButton(self.target, text=self.text, image=self.img, command=self.copy_text, width=250, height=50, anchor='nw', border_spacing=5, fg_color='#515151', hover_color='#202020')

    def copy_text(self):
        if (isinstance(clipboard[self.index], str)) == True:
            pyperclip.copy(clipboard[self.index])
            self.main_target.destroy()
            keyboard.press('ctrl+v')
            keyboard.release('ctrl+v')
        else:
            self.send_to_clipboard(win32clipboard.CF_DIB, clipboard[self.index])
            self.main_target.destroy()
            keyboard.press('ctrl+v')
            keyboard.release('ctrl+v')

    def send_to_clipboard(self, clip_type, image):
        output = BytesIO()
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()

    def update_btn(self):
        self.btn.grid(pady=(10, 0), padx=10, column=0)

class App(ct.CTk):
    def __init__(self):
        super().__init__()

        ct.set_appearance_mode('System')
        ct.set_default_color_theme('blue')
        self.title('ClipBoard')
        self.geometry('300x410')
        self.resizable(False, False)
        self.maxsize(300, 400)
        self.minsize(300, 400)

        self.frame = ct.CTkScrollableFrame(self, height=400)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky="ew")

        self.set_plates()
        self.mainloop()

    def set_plates(self):
        buttons.clear()
        for i in range(0, len(clipboard)):
            if isinstance(clipboard[i], str) == False:
                w, h = clipboard[i].size
                img = clipboard[i].resize((round((230 / w) * w), round((230 / w) * h)))
                ph = ImageTk.PhotoImage(img)
                buttons.append(Button(self, self.frame, '', ph, i))
            else:
                buttons.append(Button(self, self.frame, clipboard[i], None, i))
            buttons[i].update_btn()
        self.update()
        for i in range(0, len(clipboard)):
            if isinstance(clipboard[i], str) == True:
                width = (buttons[i].btn).winfo_width()
                if (width > 270):
                    char_width = width / len(clipboard[i])
                    chars_per_line = int(270 / char_width)
                    while (buttons[i].btn).winfo_width() > 270:
                        wraped_text = '\n'.join(wrap(clipboard[i], chars_per_line))
                        (buttons[i].btn).configure(text=wraped_text)
                        self.update()
                        chars_per_line -= 5

def set_clipboard(data):
    global clipboard
    clipboard.insert(0, data)
    temp = []
    for i in clipboard:
        if i not in temp:
            temp.append(i)
    clipboard = temp

def main():
    global app
    recent_value = ""
    while True:
        try:
            image = ImageGrab.grabclipboard()
        except Exception:
            pass
        tmp_value = pyperclip.paste()
        if tmp_value != recent_value and image == None:
            recent_value = tmp_value
            set_clipboard(recent_value)
        if tmp_value != recent_value and image:
            set_clipboard(image)
        if (keyboard.is_pressed('win+v')):    
            app = App()
        if (keyboard.is_pressed('ctrl+alt+p')):
            break

        time.sleep(0.05)

if __name__ == '__main__':
    main()
