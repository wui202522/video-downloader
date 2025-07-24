from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Copy Video Title</title>
      <style>
        body {
          background: #121212;
          color: #ffffff;
          font-family: Arial, sans-serif;
          margin: 0;
          padding: 20px;
        }

        .container {
          max-width: 500px;
          margin: auto;
          padding: 20px;
          background: #1e1e1e;
          border-radius: 12px;
          box-shadow: 0 0 10px rgba(0,0,0,0.5);
        }

        .ad-top {
          text-align: center;
          margin-bottom: 20px;
        }

        .copy-btn {
          display: block;
          width: 100%;
          padding: 14px;
          background-color: #007bff;
          color: #fff;
          border: none;
          border-radius: 8px;
          font-size: 16px;
          cursor: pointer;
          transition: background-color 0.3s ease;
        }

        .copy-btn:hover {
          background-color: #0056b3;
        }

        .title-text {
          display: none;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <!-- Top Ad -->
        <div class="ad-top">
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

        <!-- Hidden Title and Copy Button -->
        <div class="title-text" id="videoTitle">
          🎬 ฟาโรห์pharaoh🐍⚰️ I went to the mall.#pharaoh #ฟาโรห์ #เทรนวันนี้ #tiktok
        </div>
        <button class="copy-btn" onclick="copyTitle()">Copy Full Title</button>
      </div>

      <script>
        function copyTitle() {
          const title = document.getElementById("videoTitle").innerText;
          navigator.clipboard.writeText(title)
            .then(() => alert("✅ Title copied to clipboard!"))
            .catch(err => alert("❌ Failed to copy: " + err));
        }
      </script>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
