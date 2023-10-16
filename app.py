import os
from flask import Flask, request, render_template,redirect, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ROOT_URL='http://localhost:8000/app/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__, static_folder=UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cdn_assets = {}  # Dictionary to store uploaded assets


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET','POST'])
def upload_asset():
    if request.method == 'POST':
      # check if the post request has the file part
      if 'file' not in request.files:
          return "No file part", 400
      file = request.files['file']
      # If the user does not select a file, the browser submits an
      # empty file without a filename.
      if file.filename == '':
          return "No selected file", 400
      
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          # return redirect(url_for('download_file', name=filename))
      
          cdn_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
          cdn_assets[filename] = cdn_url
          # redirect to root path
          return redirect(ROOT_URL), 201
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <span> file formats 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' </span> <br/><br/>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
# create a root route to say hello
@app.route('/')
def home():
    return render_template('home.html', cdn_assets=cdn_assets, ROOT_URL=ROOT_URL)

@app.route('/retrieve/<filename>', methods=['GET'])
def retrieve_asset(filename):
    print( 'assests: ', cdn_assets, filename)
    if filename in cdn_assets:
        cdn_url = cdn_assets[filename]
        # Simulate the retrieval process
        return jsonify({'cdn_url': cdn_url})
    else:
        return "Asset not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
