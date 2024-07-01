from flask import Flask, request
from requests import get
from urllib.parse import unquote

app = Flask(__name__)

@app.route('/')
def index():
    url = unquote(request.args.get('url', ''))
    if not url: return 'Usage: /?url=<subtitle-url>'
    r = get(url)
    return r.text


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)