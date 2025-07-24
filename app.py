from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'

VIDEO_INFO = {}

ad_banner_code = '''
<!-- Ad Banner Start -->
<div style="position: fixed; top: 0; left: 0; width: 100%; height: 90px; background: #000; z-index: 9999; display: flex; justify-content: center; align-items: center;">
  <script type="text/javascript">
    atOptions = {
      'key' : 'ba09d112d910a6f2a95c3ae735a9ff9b',
      'format' : 'iframe',
      'height' : 90,
      'width' : 728,
      'params' : {}
    };
  </script>
  <script type="text/javascript" src="//testtubeabilityinvited.com/ba09d112d910a6f2a95c3ae735a9ff9b/invoke.js"></script>
</div>
<!-- Ad Banner End -->
'''

url_input_template = ''' (เหมือนเดิมในโค้ดคุณ) '''

quality_selection_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Choose Quality</title>
<style>
  * { box-sizing: border-box; }
  body {
    background: #000;
    color: #eee;
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 110px 10px 20px; /* padding-top for fixed ad */
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
  }
  form {
    background: #1e1e1e;
    padding: 15px 20px;
    border-radius: 10px;
    box-shadow: 0 0 12px #000;
    max-width: 600px;
    width: 100%;
    margin-top: 30px;
  }
  h2 {
    font-size: 1rem;
    color: #0d6efd;
    margin: 0 0 12px;
    text-align: center;
    word-wrap: break-word;
  }
  label {
    display: block;
    margin-bottom: 6px;
    font-weight: 600;
  }
  select,
  button {
    width: 100%;
    padding: 10px 12px;
    margin-top: 8px;
    margin-bottom: 12px;
    border-radius: 6px;
    border: 1px solid #444;
    background: #2c2c2c;
    color: #eee;
    font-size: 1rem;
    font-weight: 500;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.2);
    cursor: pointer;
    transition: background 0.3s ease;
    text-align: center;
  }
  select {
    background: #333;
    color: #fff;
  }
  button {
    background: #0d6efd;
    color: #fff;
    font-weight: bold;
  }
  select:focus,
  button:hover {
    background: #0d6efd;
    color: #fff;
    border-color: #0d6efd;
  }
  @media (max-width: 480px) {
    body {
      padding: 120px 8px 20px;
    }
    form {
      padding: 12px 15px;
      margin-top: 20px;
    }
    h2 {
      font-size: 0.9rem;
      margin-bottom: 8px;
    }
    select,
    button {
      padding: 8px 10px;
      font-size: 0.9rem;
      margin-top: 6px;
      margin-bottom: 10px;
    }
  }
</style>
</head>
<body>

''' + ad_banner_code + '''

<form method="post">

  <div id="videoTitle" style="white-space: pre-wrap; word-wrap: break-word; background:#222; padding:10px; margin-bottom: 12px; border-radius:6px; color:#eee;">
    {{ title }}
  </div>

  <button type="button" onclick="copyTitle()" style="margin-bottom: 12px;">
    📋 Copy Full Title
  </button>

<script>
  function copyTitle() {
    const text = document.getElementById('videoTitle').innerText;
    navigator.clipboard.writeText(text).then(function() {
      alert('✅ Title copied to clipboard!');
    }, function(err) {
      alert('❌ Failed to copy title.');
    });
  }
</script>

  <input type="hidden" name="url" value="{{ url }}">
  <label for="format_id">Choose Video Quality:</label>
  <select name="format_id" required>
    {% for f in formats %}
      <option value="{{ f.format_id }}">
        {{ f.resolution or (f.height|string + 'p') }} - {{ f.ext }} - {{ ((f.filesize or 0) // 1024 // 1024) }}MB
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
        # Handle cookies file upload
        if 'cookiesfile' in request.files:
            file = request.files['cookiesfile']
            if file.filename != '':
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'cookies.txt'))
                return "✅ cookies.txt uploaded successfully! Go back and paste your video URL."

        url = request.form.get('url')
        format_id = request.form.get('format_id')

        if format_id and 'info' in VIDEO_INFO:
            info = VIDEO_INFO['info']
            video_id = info.get('id')
            os.makedirs("downloads", exist_ok=True)

            ydl_opts = {
                'format': format_id,
                'outtmpl': f'downloads/{video_id}.%(ext)s',
                'cookiefile': 'cookies.txt',
                'quiet': True,
                'no_warnings': True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([info['webpage_url']])

                for file in os.listdir("downloads"):
                    if file.startswith(video_id):
                        return send_file(os.path.join("downloads", file), as_attachment=True)

                return "❌ File not found after download."
            except Exception as e:
                return f"❌ Error during download: {str(e)}"

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

                # Debug print title
                print("Video title:", info.get('title'))

                return render_template_string(
                    quality_selection_template,
                    formats=formats,
                    url=url,
                    title=info.get('title')
                )
            except Exception as e:
                return f"❌ Error extracting formats: {str(e)}"

    return render_template_string(url_input_template)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
