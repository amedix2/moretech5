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
    with codecs.open('data/answer3.0.json', 'r', 'utf-8-sig') as f:
        data = json.load(f)
    # print(data)

    # print(locations)

    if request.method == 'POST':
        visit0 = 'visit0' in request.form  # atm
        visit1 = 'visit1' in request.form  # операции с счетами
        visit2 = 'visit2' in request.form  # платежи
        visit3 = 'visit3' in request.form  # переводы вне рф
        visit4 = 'visit4' in request.form  # оформление карты
        visit5 = 'visit5' in request.form  # получение ипотеки
        visit6 = 'visit6' in request.form  # получение кредита
        visit7 = 'visit7' in request.form  # обмен валют
        visit8 = 'visit8' in request.form  # покупка автивов
        features1 = 'features1' in request.form  # юл
        features2 = 'features2' in request.form  # фл
        features3 = 'features3' in request.form  # аренда банковских ячеек
        features4 = 'features4' in request.form  # пандус
    else:
        visit0 = False
        visit1 = False
        visit2 = False
        visit3 = False
        visit4 = False
        visit5 = False
        visit6 = False
        visit7 = False
        visit8 = False
        features1 = False
        features2 = False
        features3 = False
        features4 = False
    ans = f'{visit1}, {visit2}, {visit3}, {visit4}, {visit5}, {visit6}, {visit7}, {visit8}, {features1}, {features2}, {features3}, {features4}'
    print(ans)

    data_dicts = []
    for i in data:
        if features1 == i['entrepreneurs'] and features2 != i['citizen']:
            data_dicts.append(i)
    print(data_dicts)

    locations = [{'name': d['name'], 'adr': d['address'], 'lat': d['latitude'], 'lon': d['longitude']} for d in data_dicts]

    return render_template('index.html', message=ans,
                           checked1=visit0, checked2=visit1, checked3=visit2, checked4=visit3, checked5=visit4,
                           checked6=visit5, checked7=visit6, checked8=visit7, checked9=visit8, checked10=features1,
                           checked11=features2, checked12=features3, checked13=features4,
                           locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
