import tkinter as tk
from tkinter import Frame, Text, Scrollbar, Entry, Button, END
import threading

# Dummy functions for testing
def handle_command(cmd): return False
def get_ai_response(cmd): return "Test response"
def speak(text): pass
def recognize_speech(): return "Test voice input"

class AuroraGUI:
    def __init__(self, master):
        self.master = master
        master.title("Aurora - Your Personal AI Assistant")
        master.geometry("600x600")

        # Custom ScrolledText widget
        self.chat_frame = Frame(master)
        self.chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_display = Text(self.chat_frame, wrap=tk.WORD, state='disabled', font=("Segoe UI", 11))
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = Scrollbar(self.chat_frame, command=self.chat_display.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.config(yscrollcommand=scrollbar.set)

        self.entry = tk.Entry(master, font=("Segoe UI", 12))
        self.entry.pack(padx=10, pady=5, fill=tk.X)
        self.entry.bind("<Return>", self.process_user_input)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=5)

        self.send_button = tk.Button(self.button_frame, text="Send", command=self.process_user_input)
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.voice_button = tk.Button(self.button_frame, text="🎤 Speak", command=self.start_voice_input_thread)
        self.voice_button.pack(side=tk.LEFT, padx=5)

    def add_to_chat(self, sender, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')

    def process_user_input(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        self.add_to_chat("You", user_input)
        self.entry.delete(0, tk.END)

        threading.Thread(target=self.handle_command_wrapper, args=(user_input,), daemon=True).start()

    def handle_command_wrapper(self, command):
        handled = handle_command(command)
        
        if not handled:  # Fallback to LLM response
            ai_reply = get_ai_response(command)
            self.add_to_chat("Aurora", ai_reply)
            speak(ai_reply)

    def start_voice_input_thread(self):
        threading.Thread(target=self.voice_input_thread, daemon=True).start()

    def voice_input_thread(self):
        self.add_to_chat("Aurora", "Listening...")
        voice_text = recognize_speech()
        if voice_text:
            self.add_to_chat("You (Voice)", voice_text)
            self.handle_command_wrapper(voice_text)
        else:
            self.add_to_chat("Aurora", "Sorry, I didn't catch that.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = AuroraGUI(root)
    root.mainloop()