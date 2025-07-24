from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os

app = Flask(__name__)
VIDEO_INFO = {}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        format_id = request.form.get('format_id')

        # Step 3: Download selected format
        if format_id and 'info' in VIDEO_INFO:
            info = VIDEO_INFO['info']
            video_id = info.get('id')
            ext = 'mp4'  # Default extension
            os.makedirs("downloads", exist_ok=True)

            ydl_opts = {
                'format': format_id,
                'outtmpl': f'downloads/{video_id}.%(ext)s',  # ✅ Use video ID
                'cookiefile': 'cookies.txt',
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    result = ydl.download([info['webpage_url']])

                # Find downloaded file
                for file in os.listdir("downloads"):
                    if file.startswith(video_id):
                        return send_file(os.path.join("downloads", file), as_attachment=True)

                return "❌ File not found after download."

            except Exception as e:
                return f"❌ Error during download: {str(e)}"

        # Step 2: Extract available formats
        elif url:
            try:
                with yt_dlp.YoutubeDL({'cookiefile': 'cookies.txt'}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    VIDEO_INFO['info'] = info
                    formats = [
                        f for f in info['formats']
                        if f.get('vcodec') != 'none' and f.get('height')
                    ]
                    formats = sorted(formats, key=lambda x: x.get('height'), reverse=True)

                return render_template_string(quality_selection_template, formats=formats, url=url, title=info.get('title'))

            except Exception as e:
                return f"❌ Error extracting formats: {str(e)}"

    # Step 1: Show form
    return render_template_string(url_input_template)

# Step 1 UI
url_input_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Video Downloader</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
        body {
            background: #121212; color: #eee;
            font-family: sans-serif; display: flex;
            align-items: center; justify-content: center;
            height: 100vh; margin: 0; padding: 20px;
        }
        form {
            background: #1e1e1e; padding: 20px;
            border-radius: 10px; width: 100%;
            max-width: 400px; box-shadow: 0 0 12px #000;
        }
        input, button {
            width: 100%; padding: 12px;
            margin-top: 12px; border-radius: 6px;
            border: none; font-size: 1rem;
        }
        input { background: #333; color: #fff; }
        button { background: #0d6efd; color: #fff; font-weight: bold; }
    </style>
</head>
<body>
    <form method="post">
        <input name="url" placeholder="Paste video URL" required />
        <button type="submit">Get Video Qualities</button>
    </form>
</body>
</html>
'''

# Step 2 UI (with video title shown)
quality_selection_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Choose Quality</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
        body {
            background: #121212; color: #eee;
            font-family: sans-serif; display: flex;
            align-items: center; justify-content: center;
            height: 100vh; margin: 0; padding: 20px;
        }
        form {
            background: #1e1e1e; padding: 20px;
            border-radius: 10px; width: 100%;
            max-width: 400px; box-shadow: 0 0 12px #000;
        }
        h2 {
            font-size: 1.1rem; margin-bottom: 10px;
            color: #0d6efd;
        }
        select, button {
            width: 100%; padding: 12px;
            margin-top: 12px; border-radius: 6px;
            border: none; font-size: 1rem;
        }
        select { background: #333; color: #fff; }
        button { background: #0d6efd; color: #fff; font-weight: bold; }
    </style>
</head>
<body>
    <form method="post">
        <h2>🎬 {{ title }}</h2>
        <input type="hidden" name="url" value="{{ url }}">
        <label for="format_id">Choose Video Quality:</label>
        <select name="format_id" required>
            {% for f in formats %}
                <option value="{{ f.format_id }}">
                    {{ f.resolution or f.height|string + 'p' }} - {{ f.ext }} - {{ (f.filesize or 0) // 1024 // 1024 }}MB
                </option>
            {% endfor %}
        </select>
        <button type="submit">Download</button>
    </form>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
