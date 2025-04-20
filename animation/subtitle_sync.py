import re

def parse_srt_with_colors(srt_file):
    with open(srt_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Divide o arquivo em blocos de legendas
    subtitle_blocks = content.strip().split('\n\n')
    subtitles = []

    for block in subtitle_blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue

        # Extrai o número da legenda, tempo e texto
        try:
            subtitle_number = int(lines[0])
        except ValueError:
            continue

        time_line = lines[1]
        text_lines = '\n'.join(lines[2:]).strip()

        # Extrai metadados do texto (cor, LaTeX, tamanho da fonte)
        color = 'WHITE'
        use_latex = False
        font_size = None

        color_match = re.search(r'\[color=([a-zA-Z]+)\]', text_lines)
        if color_match:
            color = color_match.group(1).upper()
            text_lines = re.sub(r'\[color=[a-zA-Z]+\]', '', text_lines)

        latex_match = re.search(r'\[latex\]', text_lines)
        if latex_match:
            use_latex = True
            text_lines = re.sub(r'\[latex\]', '', text_lines)

        size_match = re.search(r'\[size=(\d+)\]', text_lines)
        if size_match:
            font_size = int(size_match.group(1))
            text_lines = re.sub(r'\[size=\d+\]', '', text_lines)

        # Remove espaços extras do texto
        text = text_lines.strip()

        subtitles.append({
            'number': subtitle_number,
            'time': time_line,
            'text': text,
            'color': color,
            'use_latex': use_latex,
            'font_size': font_size
        })

    return subtitles

def get_subtitle_timings(time_line):
    # Extrai tempos de início e fim no formato '00:00:00,000 --> 00:00:10,000'
    start, end = time_line.split(' --> ')
    
    def time_to_seconds(time_str):
        h, m, s = time_str.replace(',', ':').split(':')
        return int(h) * 3600 + int(m) * 60 + float(s)
    
    start_time = time_to_seconds(start)
    end_time = time_to_seconds(end)
    return start_time, end_time