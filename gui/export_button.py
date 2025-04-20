import tkinter as tk
from tkinter import messagebox
from video.video_exporter import VideoExporter

class ExportButton:
    def __init__(self, root, config, text_input, settings_panel):
        self.root = root
        self.config = config
        self.text_input = text_input
        self.settings_panel = settings_panel
        self.button = tk.Button(root, text="Exportar Vídeo", command=self.export)
        self.button.pack(pady=10)

    def export(self):
        self.button.config(state="disabled")
        self.root.update()
        try:
            # Atualiza o tamanho da fonte antes de exportar
            try:
                self.config.font_size = int(self.settings_panel.font_size.get())
                print(f"Atualizando tamanho da fonte para: {self.config.font_size}")  # Depuração
            except (ValueError, tk.TclError):
                print("Erro ao atualizar o tamanho da fonte, usando valor padrão.")
                pass

            text = self.text_input.get_text()
            if not text and not self.config.subtitle_path:
                messagebox.showwarning("Aviso", "Por favor, insira um texto ou carregue uma legenda antes de exportar.")
                return
            subtitle_path = self.config.subtitle_path
            exporter = VideoExporter(self.config)
            exporter.export(text, subtitle_path)
            messagebox.showinfo("Sucesso", "Vídeo exportado com sucesso: output_video.mp4")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar vídeo: {str(e)}")
        finally:
            self.button.config(state="normal")