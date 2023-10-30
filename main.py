# Import the required Libraries
import os
import threading
import uuid
from tkinter import *
from tkinter import ttk, filedialog
from ffmpeg_progress_yield import FfmpegProgress
from awesometkinter.bidirender import render_text


class WinGUI:
    def __init__(self) -> None:
        if not os.path.exists("output"):
            os.mkdir("output")
        self.WIN = Tk()
        self.WIN.geometry("700x350")
        # Add a Label widget
        self.filepath = ""
        title = Label(self.WIN, text=render_text("فایل مورد نظر خود را انتخاب کنید"),
                      font=('Georgia 13'))
        title.pack(pady=10)

        self.NEW_lable = Label(self.WIN, text=render_text("فایلی انتخاب نشده است : ..."),
                               font=('Aerial 8'))
        self.NEW_lable.pack()
        # Create a Button
        ttk.Button(self.WIN, text=render_text("انتخاب فایل"),
                   command=self.open_file).pack(pady=20)

        # Create a Button
        ttk.Button(self.WIN, text=render_text("تبدیل"),
                   command=self.create_thread).pack(pady=20)

        self.Prog = ttk.Progressbar(self.WIN, orient='horizontal',
                                    mode='determinate', length=300)
        self.Prog['value'] = 0
        self.Prog.pack()

        self.Done = Label(self.WIN, text=".....", font=('Aerial 8'))

        self.WIN.mainloop()

    def create_thread(self):

        m = threading.Thread(target=self.convert_file)
        m.start()

    def open_file(self):
        file = filedialog.askopenfile(
            mode='r', filetypes=[('Video Files', '*.mp4'), ('Video Files', '*.mkv'), ('Video Files', '*.avi')])
        if file:
            self.filepath = os.path.abspath(file.name)

            self.NEW_lable.config(
                text=render_text(" : فایل انتخاب شده ") + str(self.filepath))
        self.Done.config(text=render_text(""))

    def convert_file(self):
        print("hi")
        name = os.path.basename(self.filepath)[:-4]

        if os.path.isfile(f"./output/{name}.ts"):
            name = f"{name}_{uuid.uuid4()}"
        cmd = [
            "ffmpeg", "-i", self.filepath, "-vf", "scale=-1:720", "-crf", "0" f"./output/{name}.ts",
        ]

        ff = FfmpegProgress(cmd)
        for progress in ff.run_command_with_progress():
            print(f"{progress}/100")
            if progress == 100:
                self.Done.config(text=render_text("پایان"))
                self.Done.pack()
                self.Prog['value'] = 0
            self.Prog['value'] = progress
        print("done")


WinGUI()
