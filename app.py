
import sys,os,re, os.path  
from flask import Flask, render_template, request, redirect, flash, send_file, abort
from config import *
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='')
app.secret_key = 'secret'

@app.route("/")
def index():
    return render_template('index.html')

# @app.route('/upload')
# def upload_form():
#     return render_template('upload.html')

@app.route('/', defaults={'req_path': ''})
@app.route('/<req_path>')
def dir_listing(req_path):

    BASE_DIR = '/home/pipemun/flaskFileSystem'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)    

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', files=files)

if not os.path.isdir(upload_dest):
    os.mkdir(upload_dest)

app.config['MAX_CONTENT_LENGTH'] = file_mb_max * 1024 * 1024

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')
    
    if request.method == 'POST':
        if 'files[]' not in request.files:
                flash('Archivos no encontrados, intenta de nuevo')
                return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join( upload_dest, filename))
        flash('Archivo(s) cargado')
        return redirect('/upload')

if __name__ == '__main__':
    app.run(debug=True)