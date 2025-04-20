import tkinter as tk
from tkinter import filedialog
from gui.settings_panel import SettingsPanel
from gui.export_button import ExportButton

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Video Dashboard")
        self.config = {}  # Configurações gerais
        self.srt_file = None  # Arquivo .srt selecionado
        self.text_input = None  # Mantido para compatibilidade, mas não usado
        
        # Título
        self.label = tk.Label(self.root, text="Edmundo Mendes da Silva")
        self.label.pack(pady=10)
        
        # Botão para carregar legenda
        self.load_button = tk.Button(self.root, text="Carregar Legenda (.srt)", command=self.load_srt)
        self.load_button.pack(pady=5)
        
        # Painel de configurações
        self.settings_panel = SettingsPanel(self.root, self.config)
        self.settings_panel.pack(pady=5)
        
        # Botão de exportação (restaurado)
        self.export_button = ExportButton(self.root, self.config, self.text_input, self.settings_panel)
        self.export_button.pack(pady=5)

    def load_srt(self):
        file_path = filedialog.askopenfilename(filetypes=[("SRT files", "*.srt")])
        if file_path:
            self.srt_file = file_path
            self.export_button.set_srt_file(file_path)  # Informa o arquivo .srt ao ExportButton