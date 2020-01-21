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
        array.push([k, value[k]]);
    }
    return array;
}

var API = {};

API.get = function (url, success) {
    url = 'http://localhost:5000/api/' + url;
    App.wait();
    m.request({
        method: 'GET',
        dataType: 'jsonp',
        url: url,
    }).then(function (data) {
        App.reenable();
        success(data);
    }).catch(function (e) {
        App.reenable();
        App.showError(url);
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

