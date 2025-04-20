import re
from manim import BLUE, GREEN, WHITE, RED, YELLOW

def parse_srt_with_colors(srt_file):
    """
    Lê um arquivo .srt e extrai texto, timestamps, cores, LaTeX e tamanho da fonte.
    Suporta tags [color=<cor>], [latex], [size=<numero>] no texto.
    """
    subtitles = []
    color_map = {
        'blue': BLUE,
        'green': GREEN,
        'white': WHITE,
        'red': RED,
        'yellow': YELLOW,
    }
    
    with open(srt_file, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        i = 0
        while i < len(lines):
            if lines[i].strip().isdigit():  # Índice da legenda
                index = lines[i]
                i += 1
                time = lines[i]  # Linha de tempo
                i += 1
                text = lines[i]  # Texto da legenda
                i += 1
                
                # Parsear tags [color=<cor>], [latex], [size=<numero>]
                color = WHITE  # Cor padrão
                use_latex = False
                font_size = None  # Tamanho da fonte (None significa usar valor padrão da GUI)
                clean_text = text
                
                # Verificar [latex]
                if '[latex]' in text:
                    use_latex = True
                    clean_text = clean_text.replace('[latex]', '').strip()
                
                # Verificar [color=<cor>]
                color_match = re.match(r'\[color=(\w+)\](.+)', clean_text)
                if color_match:
                    color_name = color_match.group(1).lower()
                    clean_text = color_match.group(2).strip()
                    color = color_map.get(color_name, WHITE)
                
                # Verificar [size=<numero>]
                size_match = re.match(r'\[size=(\d+)\](.+)', clean_text)
                if size_match:
                    font_size = int(size_match.group(1))
                    clean_text = size_match.group(2).strip()
                
                subtitles.append({
                    'index': index,
                    'time': time,
                    'text': clean_text,
                    'color': color,
                    'use_latex': use_latex,
                    'font_size': font_size
                })
            else:
                i += 1
    return subtitles

def get_subtitle_timings(time_str):
    """
    Converte a linha de tempo do .srt em segundos.
    """
    start, end = time_str.split(' --> ')
    start_secs = sum(float(x) * 60 ** i for i, x in enumerate(reversed(start.replace(',', '.').split(':'))))
    end_secs = sum(float(x) * 60 ** i for i, x in enumerate(reversed(end.replace(',', '.').split(':'))))
    return start_secs, end_secs