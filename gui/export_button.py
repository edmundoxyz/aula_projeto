import tkinter as tk
from tkinter import messagebox
from video.video_exporter import VideoExporter

class ExportButton(tk.Button):
    def __init__(self, parent, config, text_input, settings_panel):
        super().__init__(parent, text="Exportar Vídeo", command=self.export_video)
        self.config = config
        self.text_input = text_input  # Não usado, mantido para compatibilidade
        self.settings_panel = settings_panel
        self.srt_file = None  # Será atualizado via MainWindow

    def set_srt_file(self, srt_file):
        """
        Método para atualizar o arquivo .srt selecionado.
        """
        self.srt_file = srt_file

    def export_video(self):
        try:
            if not self.srt_file:
                messagebox.showerror("Erro", "Nenhum arquivo .srt selecionado!")
                return
            
            # Verificar se o arquivo existe
            import os
            if not os.path.exists(self.srt_file):
                messagebox.showerror("Erro", f"Arquivo .srt não encontrado: {self.srt_file}")
                return
            
            font_size = int(self.settings_panel.font_size.get())  # Tamanho da fonte da GUI
            exporter = VideoExporter(srt_file=self.srt_file, font_size=font_size)
            exporter.export()
            messagebox.showinfo("Sucesso", "Vídeo exportado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar vídeo: {str(e)}")