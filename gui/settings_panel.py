import tkinter as tk

class SettingsPanel(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.config = config
        
        # Configurações gerais
        self.label = tk.Label(self, text="Configurações do Vídeo")
        self.label.pack(pady=10)
        
        # Campo para tamanho da fonte
        self.font_size_label = tk.Label(self, text="Tamanho da Fonte")
        self.font_size_label.pack(pady=5)
        self.font_size = tk.StringVar(value='40')  # Valor padrão
        self.font_size_entry = tk.Entry(self, textvariable=self.font_size)
        self.font_size_entry.pack(pady=5)
        
        # Outros widgets (exemplo: qualidade)
        self.quality_var = tk.StringVar(value='1080p')
        self.quality_menu = tk.OptionMenu(self, self.quality_var, '720p', '1080p')
        self.quality_menu.pack(pady=5)