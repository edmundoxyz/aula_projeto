import pysrt

class SubtitleSync:
    def __init__(self, subtitle_path):
        self.subtitle_path = subtitle_path

    def get_timings(self):
        subtitles = pysrt.open(self.subtitle_path, encoding='utf-8')  # Força UTF-8
        timings = []
        for subtitle in subtitles:
            start_time = subtitle.start.seconds + subtitle.start.milliseconds / 1000.0
            end_time = subtitle.end.seconds + subtitle.end.milliseconds / 1000.0
            text = subtitle.text.strip()
            timings.append((start_time, end_time, text))
        return timings