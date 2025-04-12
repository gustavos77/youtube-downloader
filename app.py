from flask import Flask, request, send_file, render_template
import yt_dlp
import os

# Cria cookies.txt a partir da variável de ambiente COOKIES_CONTENT
cookies_content = os.getenv("COOKIES_CONTENT")
if cookies_content:
    with open("cookies.txt", "w") as f:
        f.write(cookies_content)

app = Flask(__name__)

# Cria a pasta 'downloads' se não existir
if not os.path.exists('downloads'):
    os.makedirs('downloads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Baixa vídeo em MP4
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Salva na pasta downloads
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',  # Simula navegador
        'referer': 'https://www.youtube.com/',  # Finge que veio do YouTube
        'noplaylist': True,  # Evita baixar playlists
        'cookiefile': 'cookies.txt',  # Usa cookies para autenticação
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Erro ao baixar o vídeo: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)