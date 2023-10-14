from typing import List

from flask import Flask, render_template, request
import codecs
import json


app = Flask(__name__)


def pythagoras_algorithm(locations: list[dict], longitude: float, latitude: float) -> list[dict] | str:
    """
    Короче, я написал функцию и долго распинаться не буду.
    На функцию идут три значения:
    1. locations - лист словарей у которых обязательны значения longitude и latitude
    2. longitude - долгота чела 
    3. latitude - широта чела

    Функция сортирует locations по растоянии от чела
    В общем все. Не обосрись!
    """
    try:
        return sorted(locations, key=lambda x: ((x['latitude'] - latitude) ** 2 + (x['longitude'] - longitude) ** 2) ** 0.5)
    except Exception:
        return 'data error'


@app.route('/', methods=['get', 'post'])
def index():
    with codecs.open('data/offices.json', 'r', 'utf-8-sig') as f:
        data = json.load(f)
    # print(data)

    locations = [{'name': d['salePointName'], 'adr': d['address'], 'lat': d['latitude'], 'lon': d['longitude']} for d in data]
    # print(locations)

    if request.method == 'POST':
        checkbox1 = 'checkbox1' in request.form
        checkbox2 = 'checkbox2' in request.form
        visit1 = 'visit1' in request.form
        visit2 = 'visit2' in request.form
        visit3 = 'visit3' in request.form
        visit4 = 'visit4' in request.form
        transport1 = 'transport1'  in request.form
        transport2 = 'transport2'  in request.form
        transport3 = 'transport3'  in request.form
        features1 = 'features1' in request.form
        features2 = 'features2' in request.form
        features3 = 'features3' in request.form
        invalid1 = 'invalid1' in request.form
        invalid2 = 'invalid2' in request.form
    else:
        checkbox1 = False
        checkbox2 = False
        visit1 = False
        visit2 = False
        visit3 = False
        visit4 = False
        transport1 = False
        transport2 = False
        transport3 = False
        features1 = False
        features2 = False
        features3 = False
        invalid1 = False
        invalid2 = False
    ans = f'{checkbox1}, {checkbox2}, {visit1}, {visit2}, {visit3}, {visit4}, {transport1}, {transport2}, {transport3}, {features1}, {features2}, {features3}, {invalid1}, {invalid2}'
    return render_template('index.html', message=ans,
                            checked1=checkbox1, checked2=checkbox2, checked3=visit1, checked4=visit2, checked5=visit3, checked6=visit4, checked7=transport1, checked8=transport2, checked9=transport3, checked10=features1, checked11=features2, checked12=features3, checked13=invalid1, checked14=invalid2,
                            locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
