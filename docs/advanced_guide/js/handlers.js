/* located in js/handlers.js */
on_each_feature = function(f, l) {
    l.bindPopup(function() {
        return '<h5>' + dayjs.unix(f.properties.timestamp).format() + '</h5>';
    });
}

source = function(responseHandler, errorHandler) {
    var url = 'https://api.wheretheiss.at/v1/satellites/25544';

    fetch(url)
    .then((response) => {
        return response.json().then((data) => {
            var { id, timestamp, longitude, latitude } = data;

            return {
                'type': 'FeatureCollection',
                'features': [{
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [longitude, latitude]
                    },
                    'properties': {
                        'id': id,
                        'timestamp': timestamp
                    }
                }]
            };
        })
    })
    .then(responseHandler)
    .catch(errorHandler);
}

module.exports = {
    source,
    on_each_feature
}
