from flask import Flask, render_template, request
import codecs


app = Flask(__name__)


@app.route('/', methods=['get', 'post'])
def index():
    data = ''
    if request.method == 'POST':
        data = request.form.get('data')
    print(data)
    return render_template('index.html', message=data)


if __name__ == '__main__':
    app.run()