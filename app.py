from flask import Flask, request, Response
from requests import get
from urllib.parse import unquote

app = Flask(__name__)

@app.route('/')
def index():
    print('User-agent:', request.user_agent, flush=True)
    url = unquote(request.args.get('url', ''))
    if not url: return 'Usage: /?url={subtitle-url}'
    print(url)
    r = get(url)
    return Response(r.content, r.status_code, content_type=r.headers.get('Content-Type'))


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)