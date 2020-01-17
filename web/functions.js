function nbsps(n) {
    var result = '';
    for (var i = 0; i < n; i++) {
        result += '\u00A0'
    }
    return result;
}

function nbsp() {
    return nbsps(1);
}

function objectToArray(value) {
    var array = [];
    for (var k in value) {
        if (value.hasOwnProperty(k)) {
            array.push([k, value[k]]);
        }
    }
    return array;
}

var API = {};

API.get = function (url, success) {
    App.wait();
    m.request({
        method: 'GET',
        dataType: 'jsonp',
        url: ('http://localhost:5000/api/' + url),
    }).then(function (data) {
        success(data);
        App.reenable();
    }).catch(function (e) {
        App.showError(e);
        App.reenable();
    });
}

var TO = {};

TO.conjecture = function (data) {
    return {
        id: data[0],
        isTraining: data[1] === 1,
        name: data[2],
        text: data[3],
        tokens: data[4],
    };
}

var Templates = {};

Templates.splitContent = function (left, right) {
    return [
        m('div', { id: 'content-left' }, left),
        m('div', { id: 'content-right' }, right),
    ];
}

