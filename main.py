#imports all libraries
import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import os
from google import genai

#checks and gets the api key in the .env file
apikey = ""

def useGemini(message):
    if apikey:
        client = genai.Client(api_key=apikey)
    else:
        print("API key not found. Please set the APIKEY environment variable.")
        client = None
    if client:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=str(message),
        )
        return response.text
    else:
        return "API key not configured."

#manages video playback
def play_video(video_path, canvas, scale_factor=0.5, next_video_callback=None):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        return

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            width = int(frame_rgb.shape[1] * scale_factor)
            height = int(frame_rgb.shape[0] * scale_factor)
            resized_frame = cv2.resize(frame_rgb, (width, height), interpolation=cv2.INTER_AREA)
            img = Image.fromarray(resized_frame)
            img_tk = ImageTk.PhotoImage(image=img)
            canvas.img_tk = img_tk
            canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)
            canvas.after(30, update_frame)
        else:
            cap.release()
            print(f"Video playback finished: {video_path}")
            if next_video_callback:
                next_video_callback()

    update_frame()

#main loop of the app
class App:
    def __init__(self):
        #window intialization
        self.root = tk.Tk()
        self.root.geometry("500x600")
        self.root.title("CALCulator")
        self.root.iconphoto(False, tk.PhotoImage(file="Images/ScrapyardIcon.png"))

        #backgroun detail initialization
        self.mainframe = tk.Frame(self.root, background="white")
        self.mainframe.pack(fill='both', expand=True)

        #user input box
        self.text_input = ttk.Label(self.mainframe, text="input an equation", background="white", font=("arial black", 20), wraplength=400, justify="left")
        self.text_input.grid(row=1, column=0, columnspan=2)

        #solve button
        self.set_text_field = ttk.Entry(self.mainframe, font=("arial black", 20), width="10")
        self.set_text_field.grid(row=2, column=0, pady=10, sticky="NWES")
        set_text_button = ttk.Button(self.mainframe, text="Solve", width="10", command=self.set_text)
        set_text_button.grid(row=2, column=1)

        #number buttons
        self.number1 = ttk.Button(self.mainframe, text="1", width="3", command=self.set_input)
        self.number1.grid(row=3, column=0)

        self.number2 = ttk.Button(self.mainframe, text="2", width="3", command=self.set_input)
        self.number2.grid(row=3, column=1)

        self.number3 = ttk.Button(self.mainframe, text="3", width="3", command=self.set_input)
        self.number3.grid(row=3, column=2)
        
        self.number4 = ttk.Button(self.mainframe, text="4", width="3", command=self.set_input)
        self.number4.grid(row=4, column=0)

        self.number5 = ttk.Button(self.mainframe, text="5", width="3", command=self.set_input)
        self.number5.grid(row=4, column=1)

        self.number6 = ttk.Button(self.mainframe, text="6", width="3", command=self.set_input)
        self.number6.grid(row=4, column=2)

        self.number7 = ttk.Button(self.mainframe, text="7", width="3", command=self.set_input)
        self.number7.grid(row=5, column=0)

        self.number8 = ttk.Button(self.mainframe, text="8", width="3", command=self.set_input)
        self.number8.grid(row=5, column=1)

        self.number9 = ttk.Button(self.mainframe, text="9", width="3", command=self.set_input)
        self.number9.grid(row=5, column=2)

        #key input
        self.set_key_field = ttk.Entry(self.mainframe, font=("arial black", 20), width="10")
        self.set_key_field.grid(row=6, column=0, pady=10, sticky="NWES")
        set_key_button = ttk.Button(self.mainframe, text="Enter Gemini Key", width="15", command=self.set_key)
        set_key_button.grid(row=6, column=1)

        #top text
        self.text = ttk.Label(self.mainframe, text="Remember, Calc means CALCulator", background="white", font=("arial black", 20))
        self.text.grid(row=7, column=0, columnspan=2)

        #video canvas setup
        self.video_canvas = tk.Canvas(self.mainframe, width=320, height=200)
        self.video_canvas.grid(row=8, column=0, columnspan=2, pady=10)

        #video playback
        self.video_files = ["Videos/ad1.mp4", "Videos/ad2.mp4", "Videos/ad3.mp4", "Videos/ad3.mp4"]  # List of video files
        self.current_video_index = 0


        #code execution
        self.play_current_video()

        self.root.mainloop()

    #manages playing video during the loop
    def play_current_video(self):
        if self.current_video_index < len(self.video_files):
            video_file = self.video_files[self.current_video_index]
            self.current_video_index += 1
            play_video(video_file, self.video_canvas, 0.5, next_video_callback=self.play_current_video)
        else:
            print("All videos finished.")

    #allows for the top text to be changed
    def set_text(self):
        newtext = self.set_text_field.get()
        newertext = str(useGemini("give only a complicated calculus equation that leads to the same answer of this equation and say nothing else: " + newtext))
        self.text_input.config(text=newtext + ' = ' + newertext)

    #allows for the top text to be changed
    def set_input(self):
        newertext = str(useGemini("give an insult about being too lazy to use a keyboard to use a keyboard on a calculator and nothing else and no quotes"))
        self.text_input.config(text=newertext)
    
    def set_key(self):
        global apikey
        apikey = str(self.set_key_field.get())
        

#plays the app
if __name__ == "__main__":
    app = App()


