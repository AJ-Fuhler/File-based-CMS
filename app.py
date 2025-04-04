import secrets
import os
from markdown import markdown
from flask import (Flask,
                   render_template,
                   send_from_directory,
                   flash,
                   redirect,
                   request,
                   url_for)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

def get_data_path():
    if app.config['TESTING']:
        return os.path.join(os.path.dirname(__file__), 'tests', 'data')
    else:
        return os.path.join(os.path.dirname(__file__), 'cms', 'data')

@app.route("/")
def index():
    data_dir = get_data_path()
    files = [os.path.basename(path) for path in os.listdir(data_dir)]
    return render_template('index.html', files=files)

@app.route("/<filename>")
def file_content(filename):
    data_dir = get_data_path()
    file_path = os.path.join(data_dir, filename)
    if os.path.isfile(file_path):
        if filename.endswith('.md'):
            with open(file_path, 'r') as file:
                content = file.read()
            return markdown(content)
        else:
            return send_from_directory(data_dir, filename)
    else:
        flash(f"{filename} does not exist.")
        return redirect(url_for('index'))

@app.route("/<filename>/edit")
def edit_file(filename):
    data_dir = get_data_path()
    file_path = os.path.join(data_dir, filename)
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            content = file.read()
        return render_template('edit.html',
                               filename=filename,
                               content=content)
    else:
        flash(f"{filename} does not exist.")
        return redirect(url_for('index'))

@app.route("/<filename>", methods=["POST"])
def save_file(filename):
    data_dir = get_data_path()
    file_path = os.path.join(data_dir, filename)

    content = request.form['content']
    with open(file_path, "w") as file:
        file.write(content)
    
    flash(f"{filename} has been updated.")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5003)