
function init() {
    var myMap = new ymaps.Map('for-offline-map', {
            center: [48.707067, 44.516975],
            zoom: 8,
            controls: ['zoomControl']
        }),
    // Создаем коллекцию.
        myCollection = new ymaps.GeoObjectCollection()
        var myPoints = []
        for (var i = 0; i < offlineStoreAddresses.length; i++)
        {
            ymaps.geocode(offlineStoreAddresses[i]).then(function (res) {
                var obj = res.geoObjects.get(0)
                myPoints.push({ coords: obj.geometry._coordinates, text: [obj.getCountry(), obj.getAddressLine()].join(', ') })
                if (myPoints.length == offlineStoreAddresses.length) {
                    continueInit()
                }
            })
        }

    function continueInit(){
        for (var i = 0, l = myPoints.length; i < l; i++) {
            var point = myPoints[i];
            var myPlacemark = new ymaps.Placemark(
                point.coords, {
                    balloonContentBody: point.text
                }
            )
            myPlacemark.events.add('click', function(e) {
                thisPlacemark = e.get('target');
                var text = thisPlacemark.properties._data.balloonContentBody
                $("#offline-address").text(text)
                })
            myCollection.add(myPlacemark)
        }
    
        // Добавляем коллекцию меток на карту.
        myMap.geoObjects.add(myCollection);
    
        // Создаем экземпляр класса ymaps.control.SearchControl
        var mySearchControl = new ymaps.control.SearchControl({
            options: {
                // Заменяем стандартный провайдер данных (геокодер) нашим собственным.
                provider: new CustomSearchProvider(myPoints),
                // Не будем показывать еще одну метку при выборе результата поиска,
                // т.к. метки коллекции myCollection уже добавлены на карту.
                noPlacemark: true,
                resultsPerPage: 5
            }});
    
        // Добавляем контрол в верхний правый угол,
        myMap.controls
            .add(mySearchControl, { float: 'right' });
    }
}


// Провайдер данных для элемента управления ymaps.control.SearchControl.
// Осуществляет поиск геообъектов в по массиву points.
// Реализует интерфейс IGeocodeProvider.
function CustomSearchProvider(points) {
    this.points = points;
}

// Провайдер ищет по полю text стандартным методом String.ptototype.indexOf.
CustomSearchProvider.prototype.geocode = function (request, options) {
    var deferred = new ymaps.vow.defer(),
        geoObjects = new ymaps.GeoObjectCollection(),
    // Сколько результатов нужно пропустить.
        offset = options.skip || 0,
    // Количество возвращаемых результатов.
        limit = options.results || 20;
        
    var points = [];
    // Ищем в свойстве text каждого элемента массива.
    for (var i = 0, l = this.points.length; i < l; i++) {
        var point = this.points[i];
        if (point.text.toLowerCase().indexOf(request.toLowerCase()) != -1) {
            points.push(point);
        }
    }
    // При формировании ответа можно учитывать offset и limit.
    points = points.splice(offset, limit);
    // Добавляем точки в результирующую коллекцию.
    for (var i = 0, l = points.length; i < l; i++) {
        var point = points[i],
            coords = point.coords,
                    text = point.text;

        geoObjects.add(new ymaps.Placemark(coords, {
            name: text + ' name',
            description: text + ' description',
            balloonContentBody: '<p>' + text + '</p>',
            boundedBy: [coords, coords]
        }));
    }

    deferred.resolve({
        // Геообъекты поисковой выдачи.
        geoObjects: geoObjects,
        // Метаинформация ответа.
        metaData: {
            geocoder: {
                // Строка обработанного запроса.
                request: request,
                // Количество найденных результатов.
                found: geoObjects.getLength(),
                // Количество возвращенных результатов.
                results: limit,
                // Количество пропущенных результатов.
                skip: offset
            }
        }
    });

    // Возвращаем объект-обещание.
    return deferred.promise();
};


ymaps.ready(init);