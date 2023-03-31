from flask import Flask, request, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <form method="POST" action="/upload">
            <label for="url">URL:</label>
            <input type="text" id="url" name="url">
            <input type="submit" value="Start Upload">
        </form>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    url = request.form['url']
    process_id = str(uuid.uuid4())
    json_path = f'/home/data/{process_id}.json'
    with open(json_path, 'w') as f:
        f.write(json.dumps({'url': url}))
    subprocess.Popen(['/bin/bash', '/home/script.sh', json_path])
    return jsonify({'process_id': process_id})

@app.route('/process/<string:process_id>')
def process(process_id):
    log_path = f'/home/logs/{process_id}.log'
    if not os.path.exists(log_path):
        return jsonify({'error': 'Process not found'})
    with open(log_path) as f:
        return f.read()

if __name__ == '__main__':
    app.run(port=8081)
