from flask import Flask, request, send_file
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
            'cookiefile': 'cookies.txt',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)

            if os.path.exists(filename):
                return send_file(filename, as_attachment=True)
            else:
                return "❌ Error: Downloaded file not found."

        except Exception as e:
            return f"❌ Error: {str(e)}"

    # For GET requests, serve the nice mobile UI
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Video Downloader</title>
    <style>
      body {
        background: #121212;
        color: #eee;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        margin: 0;
        padding: 20px;
      }
      form {
        background: #1e1e1e;
        padding: 25px 20px;
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.6);
        width: 100%;
        max-width: 400px;
        box-sizing: border-box;
      }
      input[name="url"] {
        width: 100%;
        padding: 14px 16px;
        margin-bottom: 18px;
        font-size: 1.1rem;
        border-radius: 8px;
        border: none;
        outline: none;
        box-sizing: border-box;
        background: #2a2a2a;
        color: #eee;
      }
      input[name="url"]::placeholder {
        color: #bbb;
      }
      input[type="submit"] {
        width: 100%;
        background: #0d6efd;
        color: white;
        padding: 14px 0;
        font-size: 1.2rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        font-weight: 600;
      }
      input[type="submit"]:hover {
        background: #0b5ed7;
      }
      @media (max-width: 400px) {
        form {
          padding: 20px 15px;
        }
        input[name="url"], input[type="submit"] {
          font-size: 1rem;
          padding: 12px 14px;
        }
      }
    </style>
    </head>
    <body>
      <form method="post" autocomplete="off">
        <input name="url" placeholder="Paste video URL here" required />
        <input type="submit" value="Download" />
      </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
