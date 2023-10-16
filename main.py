import tkinter as tk
from tkinter import ttk
import time
import random


class TypingTestApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Test")

        self.target_label = ttk.Label(master, text="", wraplength=600, justify="center")
        self.target_label.pack(pady=20)

        self.typing_area = tk.Text(master, wrap=tk.WORD, width=60, height=5, font=("Arial", 12))
        self.typing_area.pack(pady=20)
        self.typing_area.config(state=tk.DISABLED)  # Disable until the test starts

        self.wpm_label = ttk.Label(master, text="WPM: 0")
        self.wpm_label.pack(pady=10)

        self.start_button = ttk.Button(master, text="Start", command=self.start_test)
        self.start_button.pack(pady=20)

        self.retry_button = ttk.Button(master, text="Retry", command=self.retry_test, state=tk.DISABLED)
        self.retry_button.pack(pady=20)

        self.master.bind('<Return>', self.start_test)  # Bind the Enter key to start the test

        self.start_time = None
        self.load_text()

    def load_text(self):
        with open("text.txt", "r") as f:
            lines = f.readlines()
        self.target_sentence = random.choice(lines).strip()
        self.target_label.config(text=self.target_sentence)

    def start_test(self, event=None):
        if self.start_time is None:  # Only start the test if it hasn't been started
            self.typing_area.config(state=tk.NORMAL)  # Enable typing
            self.start_time = time.time()
            self.typing_area.bind('<KeyRelease>', self.check_text)  # Bind to check text on each key release
            self.start_button.config(state=tk.DISABLED)  # Disable the start button

    def check_text(self, event=None):
        typed_text = self.typing_area.get(1.0, tk.END).strip()
        correct_text = self.target_sentence[:len(typed_text)]

        # Highlighting text
        self.typing_area.tag_remove("correct", "1.0", tk.END)
        self.typing_area.tag_remove("wrong", "1.0", tk.END)

        for i, (typed_char, correct_char) in enumerate(zip(typed_text, correct_text)):
            tag = "correct" if typed_char == correct_char else "wrong"
            self.typing_area.tag_add(tag, f"1.{i}", f"1.{i + 1}")

        # Define the colors for the tags
        self.typing_area.tag_config("correct", background="green", foreground="white")
        self.typing_area.tag_config("wrong", background="red", foreground="white")

        # Check for test completion
        if typed_text == self.target_sentence:
            elapsed_time = time.time() - self.start_time
            wpm = round(len(typed_text.split()) / (elapsed_time / 60))
            self.wpm_label.config(text=f"WPM: {wpm}")
            self.typing_area.config(state=tk.DISABLED)
            self.retry_button.config(state=tk.NORMAL)
            self.typing_area.unbind('<KeyRelease>')  # Unbind the event after test completion

    def retry_test(self):
        self.typing_area.config(state=tk.DISABLED)
        self.typing_area.delete(1.0, tk.END)
        self.start_button.config(state=tk.NORMAL)
        self.retry_button.config(state=tk.DISABLED)
        self.load_text()
        self.wpm_label.config(text="WPM: 0")
        self.start_time = None


if __name__ == '__main__':
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()
