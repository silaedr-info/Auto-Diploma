import file_reform
from flask import Flask, request, render_template, send_file, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        api_upload = dict(request.args)
        if 'project' in api_upload:
            file_reform.make_diploma(api_upload['template'], int(api_upload['have_project']),
                                     'special', api_upload['name'],
                                     api_upload['project'])
        else:
            file_reform.make_diploma(api_upload['template'], int(api_upload['have_project']),
                                     'special', api_upload['name'])
        return redirect('../send')
    elif request.method == 'POST':
        if 'file' in request.files:
            request.files['file'].save('data.csv')
            file_reform.file_reform_from_csv()
        return redirect('../send')
    return render_template('index.html')


@app.route('/send', methods=['POST', 'GET'])
def send():
    return send_file('diplomas.zip')


app.run()
