from flask import Flask, request, send_file, abort
import yt_dlp
import os
import glob

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        os.makedirs("downloads", exist_ok=True)

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'cookiefile': 'cookies.txt',  # ✅ Use cookies to bypass bot checks
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                # Get the downloaded filename from yt-dlp info
                filename = ydl.prepare_filename(info_dict)
            
            # Check if file exists and send it as download
            if os.path.exists(filename):
                return send_file(filename, as_attachment=True)
            else:
                return "❌ Error: Downloaded file not found on server."

        except Exception as e:
            return f"❌ Error: {str(e)}"

    return '''
        <form method="post">
            <input name="url" placeholder="Paste video URL here" required>
            <input type="submit" value="Download">
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
