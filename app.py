from flask import Flask, render_template_string, request
import yt_dlp

app = Flask(__name__)

url_input_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Powerful WebTool For Download Video</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
        body {
            background: #000000; color: #eee;
            font-family: sans-serif; padding: 220px;
            margin: auto;
            box-sizing: content-box;
            height: 30vh;
            display: flex; flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 1.2rem;
            line-height: 1.6;
            word-wrap: break-word;
            white-space: normal;
        }
        form {
            background: #1e1e1e; padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 12px #000;
            max-width: 600px;
            margin: auto;
            width: 100%;
            box-sizing: border-box;
            display: flex; flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        h1 {
            font-size: 1.8rem; text-align: center;
            color: #0d6efd; margin-bottom: 20px;
            width: 100vw; max-width: 100%;
            margin-left: calc(-20vw + 50%);
            word-wrap: break-word; white-space: normal;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: bold;
            text-shadow: 0 0 4px rgba(13, 110, 253, 0.5);
            font-family: 'Arial', sans-serif;
            margin-top: 0;
        }
        p {
            font-size: 1.2rem; text-align: center;
            color: #33ff008f; margin-bottom: 20px;
            width: 100vw; max-width: 100%;
            margin-left: calc(-20vw + 50%);
            font-family: 'Arial', sans-serif;
            margin-top: 0;
            font-weight: 300;
            text-shadow: 0 0 2px rgba(204, 204, 204, 0.5);
        }
        input, button {
            width: 100%; padding: 12px;
            margin-top: 12px; border-radius: 6px;
            border: none; font-size: 1rem;
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.2);
            font-family: 'Arial', sans-serif;
            font-weight: 500;
            background: #2c2c2c; color: #eee;
            border: 1px solid #444;
            box-sizing: border-box;
            text-align: center;
            cursor: pointer;
        }
        button {
            background: #0d6efd; color: #fff;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <!-- Ad banner top -->
    <div style="text-align:center; margin-bottom: 20px;">
        <script type="text/javascript">
            atOptions = {
                'key': 'ba09d112d910a6f2a95c3ae735a9ff9b',
                'format': 'iframe',
                'height': 90,
                'width': 728,
                'params': {}
            };
        </script>
        <script type="text/javascript" src="//testtubeabilityinvited.com/ba09d112d910a6f2a95c3ae735a9ff9b/invoke.js"></script>
    </div>

    <h1>PowerFul WebTool For Download Video</h1>
    <p>Auto Detected Url</p>

    <form method="post">
        <input name="url" placeholder="Paste YouTube Video URL" required>
        <button type="submit">Get Qualities</button>
    </form>
</body>
</html>
'''

quality_selection_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Choose Quality</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
        body {
            background: #000000; color: #eee;
            font-family: sans-serif; padding: 220px;
            margin: auto;
            box-sizing: content-box;
            height: 30vh;
            display: flex; flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 1.2rem;
            line-height: 1.6;
            word-wrap: break-word;
            white-space: normal;
        }
        form {
            background: #1e1e1e; padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 12px #000;
            max-width: 600px;
            margin: auto;
            width: 100%;
            box-sizing: border-box;
            display: flex; flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        h2 {
            font-size: 0.9rem;
            color: #0d6efd;
            margin-bottom: 20px;
            text-align: center;
            width: 100vw;
            max-width: 100%;
            margin-left: calc(-20vw + 50%);
            word-wrap: break-word;
            white-space: normal;
        }
        select, button {
            width: 100%; padding: 12px;
            margin-top: 12px; border-radius: 6px;
            border: none; font-size: 1rem;
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.2);
            font-family: 'Arial', sans-serif;
            font-weight: 500;
            background: #2c2c2c; color: #eee;
            border: 1px solid #444;
            box-sizing: border-box;
            text-align: center;
            cursor: pointer;
        }
        select { background: #333; color: #fff; }
        button { background: #0d6efd; color: #fff; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <!-- Ad banner top -->
    <div style="text-align:center; margin-bottom: 20px;">
        <script type="text/javascript">
            atOptions = {
                'key': 'ba09d112d910a6f2a95c3ae735a9ff9b',
                'format': 'iframe',
                'height': 90,
                'width': 728,
                'params': {}
            };
        </script>
        <script type="text/javascript" src="//testtubeabilityinvited.com/ba09d112d910a6f2a95c3ae735a9ff9b/invoke.js"></script>
    </div>

    <form method="post">
        <h2>{{ title }}</h2>
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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        try:
            with yt_dlp.YoutubeDL({'cookiefile': 'cookies.txt'}) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = [f for f in info['formats'] if f.get('vcodec') != 'none' and f.get('height')]
                formats = sorted(formats, key=lambda x: x.get('height', 0), reverse=True)
                return render_template_string(quality_selection_template, formats=formats, url=url, title=info.get('title'))
        except Exception as e:
            return f"<h3 style='color:red'>❌ Error: {str(e)}</h3>"
    return render_template_string(url_input_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
