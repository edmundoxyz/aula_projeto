import tkinter as tk
from tkinter import colorchooser

class SettingsPanel:
    def __init__(self, root, config):
        self.root = root
        self.config = config

        # Tamanho da fonte
        tk.Label(root, text="Tamanho da Fonte:").pack(pady=5)
        self.font_size = tk.Entry(root)
        self.font_size.insert(0, str(self.config.font_size))
        self.font_size.pack(pady=5)
        self.font_size.bind("<Return>", self.update_font_size)

        # Cor do texto
        self.color_button = tk.Button(root, text="Escolher Cor", command=self.choose_color)
        self.color_button.pack(pady=5)

        # Opção de LaTeX
        # Verifica se o atributo is_latex existe, caso contrário usa False
        initial_latex = getattr(self.config, 'is_latex', False)
        self.is_latex_var = tk.BooleanVar(value=initial_latex)
        tk.Checkbutton(root, text="Usar LaTeX", variable=self.is_latex_var, command=self.update_latex).pack(pady=5)

    def update_font_size(self, event):
        try:
            self.config.font_size = int(self.font_size.get())
        except ValueError:
            pass

    def choose_color(self):
        color = colorchooser.askcolor(title="Escolher Cor")[1]
        if color:
            self.config.text_color = color

    def update_latex(self):
        self.config.is_latex = self.is_latex_var.get()