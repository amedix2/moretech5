function init () {
    // Создаем модель мультимаршрута.
    var multiRouteModel = new ymaps.multiRouter.MultiRouteModel([
            [55.734876, 37.59308],
            "Москва, ул. Мясницкая"
        ], {
            // Путевые точки можно перетаскивать.
            // Маршрут при этом будет перестраиваться.
            wayPointDraggable: true,
            boundsAutoApply: true,
            routingMode: "pedestrian"
        }),

        // Создаём выпадающий список для выбора типа маршрута.
        routeTypeSelector = new ymaps.control.ListBox({
            data: {
                content: 'Как добраться'
            },
            items: [
                new ymaps.control.ListBoxItem({data: {content: "Авто"}}),
                new ymaps.control.ListBoxItem({data: {content: "Общественным транспортом"}}),
                new ymaps.control.ListBoxItem({data: {content: "Пешком"},state: {selected: true}})
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
        var myPlacemark = new ymaps.Placemark([location.lat, location.lon], {balloonContent: location.adr+' ||| '+location.name}, {
            iconLayout: 'default#image',
            // Своё изображение иконки метки.
            iconImageHref: 'http://127.0.0.1:5000/static/logo.png',
            // Размеры метки.
            iconImageSize: [32, 32],
            // Смещение левого верхнего угла иконки относительно
            // её "ножки" (точки привязки).
            iconImageOffset: [-16, -16],
            hideIconOnBalloonOpen: false
        });
        myMap.geoObjects.add(myPlacemark);
    });

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
