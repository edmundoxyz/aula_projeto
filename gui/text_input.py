import tkinter as tk
from tkinter import filedialog

class TextInput:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.text_area = tk.Text(root, height=10, width=50)
        self.text_area.pack(pady=10)  # Adiciona espaçamento vertical

        # Botão para carregar arquivo de legenda
        self.subtitle_button = tk.Button(root, text="Carregar Legenda (.srt)", command=self.load_subtitle)
        self.subtitle_button.pack(pady=5)  # Adiciona espaçamento
        self.subtitle_path = None

    def get_text(self):
        return self.text_area.get("1.0", tk.END).strip()

    def load_subtitle(self):
        self.subtitle_path = filedialog.askopenfilename(filetypes=[("SRT files", "*.srt")])
        if self.subtitle_path:
            self.config.subtitle_path = self.subtitle_path