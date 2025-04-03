import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    root = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(root, "cms", "data")
    files = [os.path.basename(path) for path in os.listdir(data_dir)]
    return render_template('index.html', files=files)

if __name__ == '__main__':
    app.run(debug=True, port=5003)