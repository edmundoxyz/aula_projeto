# Math Video Dashboard

Um aplicativo para criar vídeos de aulas de matemática com texto animado, suporte a LaTeX e sincronização com legendas.

## Instalação
1. Instale as dependências: `pip install -r requirements.txt`
2. Certifique-se de ter o LaTeX instalado (necessário para o Manim).
3. Execute o aplicativo: `python main.py`

## Uso
1. Insira o texto da aula no campo de texto.
2. Carregue um arquivo de legenda (.srt) se desejar sincronização.
3. Ajuste o tamanho da fonte e a cor do texto no painel de configurações.
4. Clique em "Exportar Vídeo" para gerar o arquivo MP4.

## Estrutura
- `gui/`: Interface gráfica.
- `animation/`: Lógica de animação e renderização.
- `video/`: Exportação de vídeos.
- `models/`: Configurações globais.