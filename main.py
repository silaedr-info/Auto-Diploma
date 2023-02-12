import file_reform
from flask import Flask, request, render_template, send_file, redirect

app = Flask(__name__)


@app.route('/')
def start():
    return ''


@app.route('/api/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['data']
        if f:
            f.save('data.csv')
            file_reform.file_reform_from_csv()
        else:
            f = request.form
            if f['project'] is not None:
                file_reform.make_diploma(f['template'], int(f['have_project']), 'special', f['name'], f['project'])
            else:
                file_reform.make_diploma(f['template'], int(f['have_project']), 'special', f['name'])
        return redirect('../send')
    return render_template('index.html')


@app.route('/send', methods=['POST', 'GET'])
def send():
    return send_file('diplomas.zip')


app.run()
