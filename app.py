import secrets
import os
from markdown import markdown
from flask import (Flask,
                   render_template,
                   send_from_directory,
                   flash,
                   redirect,
                   url_for)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route("/")
def index():
    root = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(root, "cms", "data")
    files = [os.path.basename(path) for path in os.listdir(data_dir)]
    return render_template('index.html', files=files)

@app.route("/<filename>")
def file_content(filename):
    root = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(root, "cms", "data")
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
    


if __name__ == '__main__':
    app.run(debug=True, port=5003)