import file_reform
import os
from flask import Flask, request, render_template, send_file, redirect

app = Flask(__name__)


@app.route('/api/upload', methods=['GET', 'POST'])
def upload():
    if request.args:
        api_upload = dict(request.args)
        if 'project' in api_upload:
            file_reform.make_diploma(api_upload['template'], int(api_upload['have_project']),
                                     'special', api_upload['name'],
                                     api_upload['project'])
        else:
            file_reform.make_diploma(api_upload['template'], int(api_upload['have_project']),
                                     'special', api_upload['name'])
        return redirect('../send')
    else:
        if request.files:
            request.files['data'].save('data.csv')
            file_reform.file_reform_from_csv()
            return redirect('../send')
        return render_template('index.html')


@app.route('/send', methods=['POST', 'GET'])
def send():
    return send_file('diplomas.zip')


@app.route('/add_new_template', methods=['GET', 'POST'])
def add_template():
    template = request.args.get("name_of_template")
    if request.method == 'POST':
        if not os.path.exists('templates_pdf'):
            os.mkdir('templates_pdf')
        request.files.get('new_template').save(f'templates_pdf/{template}.pdf')
    return render_template('add_template.html')


@app.route('/delete_zip_file')
def delete_zip():
    if os.path.exists('diplomas.zip'):
        os.remove('diplomas.zip')
    return ''


app.run()
