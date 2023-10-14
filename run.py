from flask import Flask, render_template, request
import codecs


app = Flask(__name__)


@app.route('/', methods=['get', 'post'])
def index():
    if request.method == 'POST':
        checkbox1 = 'checkbox1' in request.form
        checkbox2 = 'checkbox2' in request.form
        checkbox3 = 'checkbox3' in request.form
    else:
        checkbox1 = False
        checkbox2 = False
        checkbox3 = False

    data = f'{checkbox1}, {checkbox2}, {checkbox3}'
    return render_template('index.html', message=data, checked1=checkbox1, checked2=checkbox2, checked3=checkbox3)


if __name__ == '__main__':
    app.run(debug=True)
