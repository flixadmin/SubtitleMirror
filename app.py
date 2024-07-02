from flask import Flask, request, jsonify, url_for, Response
from requests import get
import os, magic

app = Flask(__name__)
upload_dir = os.path.join(os.getcwd(), 'uploads')
try: os.mkdir(upload_dir)
except FileExistsError: pass

def get_mime(file):
    return magic.from_file(file, True)

@app.route('/')
def index():
    return 'Usage: <br>POST /upload/{filename}?key={apikey}&slug={videoslug}&lang={Language} and data={FILE_DATA}'


@app.route('/upload/<filename>', methods=['POST'])
def upload(filename):
    key = request.args.get('key')
    slug = request.args.get('slug')
    lang = request.args.get('lang')
    try:
        path = os.path.join(upload_dir, filename)
        with open(path, 'wb') as f: f.write(request.data)
        dlurl = 'https://' + request.host + '/download/' + filename
        print(dlurl, flush=True)
        r = get(f'https://api.hydrax.net/{key}/subtitle/{slug}', headers={'Content-Type': 'application/json'}, data='{"url":"' + dlurl + '","label":"' + lang + '"}')
        # os.remove(path)
        print(r.text, flush=True)
        return jsonify(r.json())
    except Exception as e:
        return jsonify(dict(status=False, msg='Error while saving file: ' + str(e)))

@app.route('/download/<filename>')
def download(filename):
    try:
        path = os.path.join(upload_dir, filename)
        with open(path, 'rb') as f:
            return Response(f.read(), 200, {'Content-Length': len(f.read())}, get_mime(path))
    except Exception as e:
        return jsonify(dict(success=False, msg='Error while sending file: ' + str(e)))


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)