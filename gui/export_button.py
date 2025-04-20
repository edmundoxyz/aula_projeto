import tkinter as tk
from tkinter import messagebox
from video.video_exporter import VideoExporter

class ExportButton(tk.Button):
    def __init__(self, parent, main_window):
        super().__init__(parent, text="Exportar Vídeo", command=self.export_video)
        self.main_window = main_window

    def export_video(self):
        try:
            srt_file = self.main_window.srt_file  # Arquivo .srt selecionado
            if not srt_file:
                messagebox.showerror("Erro", "Nenhum arquivo .srt selecionado!")
                return
            
            # Verificar se o arquivo existe
            import os
            if not os.path.exists(srt_file):
                messagebox.showerror("Erro", f"Arquivo .srt não encontrado: {srt_file}")
                return
            
            font_size = int(self.main_window.settings_panel.font_size.get())  # Tamanho da fonte da GUI
            exporter = VideoExporter(srt_file=srt_file, font_size=font_size)
            exporter.export()
            messagebox.showinfo("Sucesso", "Vídeo exportado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar vídeo: {str(e)}")