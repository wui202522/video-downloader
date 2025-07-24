from flask import Flask, request
import yt_dlp
import os

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
                ydl.download([url])
            return "✅ Download complete!"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    return '''
        <form method="post">
            <input name="url" placeholder="Paste video URL here">
            <input type="submit" value="Download">
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
