from flask import Flask, render_template, request
import codecs
import json
from datetime import datetime
import pytz

app = Flask(__name__)


def pythagoras_algorithm(locations: list[dict], longitude: float, latitude: float) -> list[dict] | str:
    try:
        return sorted(locations,
                      key=lambda x: ((x['latitude'] - latitude) ** 2 + (x['longitude'] - longitude) ** 2) ** 0.5)
    except Exception:
        return 'data error'


@app.route('/', methods=['get', 'post'])
def index():
    with open('data/answer3.0.json', 'r',) as f:
        data = json.load(f)
    f.close()

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
    now = datetime.now().astimezone(pytz.timezone('Europe/Moscow'))
    time = now.hour * 60 + now.minute
    data_dicts = []
    for atm in data:
        try:
            if features2 and not features1:
                const_time = atm['open_hours_ind'][now.weekday()]["hours"]
            else:
                const_time = atm['open_hours_ent'][now.weekday()]["hours"]
            if const_time.lower() != 'выходной':
                if int(const_time.split('-')[0].split(':')[0])*60 < time < int(const_time.split('-')[1].split(':')[0])*60:
                    if features1 <= atm["entrepreneurs"] and features2 <= atm["citizen"] and features4 <= atm["has_ramp"]:
                            data_dicts.append(atm)
        except Exception:
            ...

    locations = {}
    for i in data_dicts:
        wait = i['peps']*(0.25*visit0 + 0.37*visit1 + 0.57*visit2 + 0.57*visit3 + 0.37*visit4 + 0.67*visit5 +0.67*visit6 + 0.07*visit7 + 0.37*visit8)
        if wait != 0: wait += 0.37 * i['peps']  # фактор бабки
        i['wait'] = wait

    ans = f'Найдено отделений: {len(data_dicts)}'
    locations = [{'name': d['name'], 'adr': d['address'], 'lat': d['latitude'], 'lon': d['longitude'], 'pep': d['peps'], 'time': d['wait']} for d in
                 data_dicts]
    print(locations)

    return render_template('index.html', message=ans,
                           checked1=visit0, checked2=visit1, checked3=visit2, checked4=visit3, checked5=visit4,
                           checked6=visit5, checked7=visit6, checked8=visit7, checked9=visit8, checked10=features1,
                           checked11=features2, checked12=features3, checked13=features4,
                           locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
