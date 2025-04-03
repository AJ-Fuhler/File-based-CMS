from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return 'Getting started.'

if __name__ == '__main__':
    app.run(debug=True, port=5003)