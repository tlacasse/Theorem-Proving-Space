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

function clamp(x, min, max) {
    if (x < min) {
        return min;
    }
    if (x > max) {
        return max;
    }
    return x;
}

var API = {};

API._get = function (url, success, block) {
    url = 'http://localhost:5000/api/' + url;
    if (block) {
        App.wait();
    }
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

API.get = function (url, success) {
    API._get(url, success, true);
}

API.aget = function (url, success) {
    API._get(url, success, false);
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

var App = {};

App.failedPath = '';
App.uniqueCounter = 0;

App.showError = function (failedPath) {
    document.getElementById('message-box').style.display = 'block';
    App.failedPath = failedPath;
}

App.hideError = function () {
    document.getElementById('message-box').style.display = 'none';
}

App.wait = function () {
    document.getElementById('wall').style.display = 'block';
}

App.reenable = function () {
    document.getElementById('wall').style.display = 'none';
}

App.uniqueId = function () {
    App.uniqueCounter++;
    return 'id' + String(App.uniqueCounter);
}

App.get = function (id) {
    return document.getElementById(id);
}

var MessageBox = {
    view: function () {
        return [
            m('div', { class: 'message-box-title' },
                m('button', {
                    class: 'message-box-button',
                    onclick: App.hideError
                }, 'X')
            ),
            m('div', { class: 'message-box-detail' },
                m('iframe', { src: App.failedPath })
            ),
        ];
    },
};
