var root = document.getElementById('page');

m.route(root, '/info', {
    '/info': Info,
});

var App = {}

App.exception = [['', '']];

App.showError = function (exceptionObject) {
    document.getElementById('message-box').style.display = 'block';
    App.exception = objectToArray(exceptionObject);
}

App.hideError = function () {
    document.getElementById('message-box').style.display = 'none';
}

var MessageBox = (function () {
    "use strict";

    function propertyPairToRow(pair) {
        return (
            m('div', { class: 'message-box-pair' }, [
                m('div', { class: 'message-box-key' }, pair[0]),
                m('div', { class: 'message-box-value' }, pair[1]),
            ])
        );
    }

    function view() {
        return [
            m('div', { class: 'message-box-title' },
                m('button', {
                    class: 'message-box-button',
                    onclick: App.hideError
                }, 'X')
            ),
            m('div', { class: 'message-box-detail' },
                App.exception.map(x => propertyPairToRow(x))
            ),
        ];
    }

    return {
        view: view,
    };
})();

m.mount(document.getElementById('message-box'), MessageBox);
