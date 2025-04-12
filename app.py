from flask import Flask, request, render_template, send_file, flash, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        flash("Por favor, insira uma URL válida.")
        return redirect(url_for('index'))

    if "youtube.com" not in url and "youtu.be" not in url:
        flash("Erro: Insira uma URL válida do YouTube.")
        return redirect(url_for('index'))

    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'video')
            video_filename = ydl.prepare_filename(info)
            video_path = video_filename if os.path.exists(video_filename) else os.path.join(DOWNLOAD_FOLDER, f"{video_title}.mp4")

        if not os.path.exists(video_path):
            flash("Erro: O vídeo não pôde ser salvo corretamente.")
            return redirect(url_for('index'))

        flash(f"Vídeo '{video_title}' baixado com sucesso!")
        return send_file(video_path, as_attachment=True, download_name=os.path.basename(video_path))

    except Exception as e:
        flash(f"Erro ao baixar o vídeo: {str(e)}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)