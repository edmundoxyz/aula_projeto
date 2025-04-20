import tkinter as tk
from gui.text_input import TextInput
from gui.settings_panel import SettingsPanel
from gui.export_button import ExportButton
from models.config import Config

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Video Dashboard")
        self.config = Config()

        # Componentes da interface
        self.text_input = TextInput(self.root, self.config)
        self.settings_panel = SettingsPanel(self.root, self.config)
        self.export_button = ExportButton(self.root, self.config, self.text_input, self.settings_panel)