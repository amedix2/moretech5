from flask import Flask, render_template, request
import codecs
import json


app = Flask(__name__)


@app.route('/', methods=['get', 'post'])
def index():
    with codecs.open('data/offices.json', 'r', 'utf-8-sig') as f:
        data = json.load(f)
    print(data)

    locations = [{'name': d['salePointName'], 'lat': d['latitude'], 'lon': d['longitude']} for d in data]
    print(locations)

    if request.method == 'POST':
        checkbox1 = 'checkbox1' in request.form
        checkbox2 = 'checkbox2' in request.form
        checkbox3 = 'checkbox3' in request.form
    else:
        checkbox1 = False
        checkbox2 = False
        checkbox3 = False
    ans = f'{checkbox1}, {checkbox2}, {checkbox3}'
    return render_template('index.html', message=ans,
                           checked1=checkbox1, checked2=checkbox2, checked3=checkbox3,
                           locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
