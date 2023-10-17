function init () {
    var banks = [];
    for (var i = 0; i < locations.length; i++) {
        banks.push([locations[i]['lat'], locations[i]['lon']]);
    }

    var yourLocation = [55.76, 37.64];

    banks.sort(function (a, b) {
        let pidor = function (x) {
          return Math.pow(
            Math.pow(x[0] - yourLocation[0], 2) +
              Math.pow(x[1] - yourLocation[1], 2),
            0.5
            );
        };
        if (pidor(a) < pidor(b)) {
          return -1;
        } else if (pidor(a) > pidor(b)) {
          return 1;
        }
        return 0;
      });
      

    // Создаем модель мультимаршрута.
    // for (var i = 9; i > -1; i--) {
        var multiRouteModel = new ymaps.multiRouter.MultiRouteModel([
            yourLocation, 
            banks[0]
        ], {
                // Путевые точки можно перетаскивать.
                // Маршрут при этом будет перестраиваться.
                wayPointDraggable: true,
                boundsAutoApply: true,
                routingMode: "masstransit"
            }),
            // Создаём выпадающий список для выбора типа маршрута.
            routeTypeSelector = new ymaps.control.ListBox({
                data: {
                    content: 'Как добраться'
                },
                items: [
                    new ymaps.control.ListBoxItem({data: {content: "Авто"}}),
                    new ymaps.control.ListBoxItem({data: {content: "Общественным транспортом"},state: {selected: true}}),
                    new ymaps.control.ListBoxItem({data: {content: "Пешком"}})
                ],
                options: {
                    itemSelectOnClick: false
                }
            }),
            // Получаем прямые ссылки на пункты списка.
            autoRouteItem = routeTypeSelector.get(0),
            masstransitRouteItem = routeTypeSelector.get(1),
            pedestrianRouteItem = routeTypeSelector.get(2);
            // Подписываемся на события нажатия на пункты выпадающего списка.
            pedestrianRouteItem.events.add('click', function (e) { changeRoutingMode('pedestrian', e.get('target')); });
            autoRouteItem.events.add('click', function (e) { changeRoutingMode('auto', e.get('target')); });
            masstransitRouteItem.events.add('click', function (e) { changeRoutingMode('masstransit', e.get('target')); });
    
            ymaps.modules.require([
            'MultiRouteCustomView'
        ], function (MultiRouteCustomView) {
            // Создаем экземпляр текстового отображения модели мультимаршрута.

            // см. файл custom_view.js
            new MultiRouteCustomView(multiRouteModel);
        });
    
        // Создаем карту с добавленной на нее кнопкой.
        var myMap = new ymaps.Map('map', {
            center: [55.76, 37.64],
            zoom: 11,
                controls: [routeTypeSelector]
            }, {
                buttonMaxWidth: 300,
                yandexMapDisablePoiInteractivity: true
            }),
            HintLayout = ymaps.templateLayoutFactory.createClass( "<div class='my-hint'>" +
                "<b>{{ properties.object }}</b><br />" +
                "{{ properties.address }}" +
                "</div>", {
                    // Определяем метод getShape, который
                    // будет возвращать размеры макета хинта.
                    // Это необходимо для того, чтобы хинт автоматически
                    // сдвигал позицию при выходе за пределы карты.
                    getShape: function () {
                        var el = this.getElement(),
                            result = null;
                        if (el) {
                            var firstChild = el.firstChild;
                            result = new ymaps.shape.Rectangle(
                                new ymaps.geometry.pixel.Rectangle([
                                    [0, 0],
                                    [firstChild.offsetWidth, firstChild.offsetHeight]
                                ])
                            );
                        }
                        return result;
                    }
                }
            ),
            // Создаем на основе существующей модели мультимаршрут.
            multiRoute = new ymaps.multiRouter.MultiRoute(multiRouteModel, {
                // Путевые точки можно перетаскивать.
                // Маршрут при этом будет перестраиваться.
                wayPointDraggable: true,
                boundsAutoApply: true,
                routeVisible: false,
                // Показывает нитку активного маршрута.
                routeActiveVisible: true,
                // setActiveRoute(myFindShortest(myMultiRoute.getRoutes()));
            });
        // Добавляем мультимаршрут на карту.
        myMap.geoObjects.add(multiRoute);
        
        locations.forEach(function(location) {
            var myPlacemark = new ymaps.Placemark([location.lat, location.lon], {
                address: location.name,
                object: location.adr        
                }, {
                iconLayout: 'default#image',
                iconImageHref: 'http://127.0.0.1:5000/static/logo.png',
                iconImageSize: [32, 32],
                iconImageOffset: [-16, -16],
                hideIconOnBalloonOpen: false,
                hintLayout: HintLayout
            });
        
            myMap.geoObjects.add(myPlacemark);
    
            myPlacemark.events.add('click', function (e) {
                var lat = location.lon;
                var lon = location.lat;
                updateRouteEndPoint(lat, lon);
            });
        });
        
        function updateRouteEndPoint(lat, lon) {
            multiRouteModel.setReferencePoints([yourLocation, [lat, lon]]);
            console.log([lat, lon])
            multiRouteModel.update().then(function () {
                // Маршрут перестроен, можно выполнить дополнительные действия
            });
        }
        function changeRoutingMode(routingMode, targetItem) {
            multiRouteModel.setParams({ routingMode: routingMode }, true);
            // Отменяем выбор элементов.
            pedestrianRouteItem.deselect();
            autoRouteItem.deselect();
            masstransitRouteItem.deselect();
            // Выбираем элемент и закрываем список.
            targetItem.select();
            routeTypeSelector.collapse();
        }
        
    }
    ymaps.ready(init);