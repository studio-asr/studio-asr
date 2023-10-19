from flask import Flask, render_template, request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        flash('No video file uploaded', 'error')
        return redirect(request.url)

    file = request.files['video']
    if file.filename == '':
        flash('No selected video file', 'error')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Video uploaded successfully!', 'success')
        return redirect(url_for('index'))

    flash('Invalid video file', 'error')
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
