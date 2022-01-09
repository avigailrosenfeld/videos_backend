from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({'status': 'ok'})


@app.route('/users', methods=['POST'])
def better_name():
    return jsonify({})

if __name__ == '__main__':
    app.run()
