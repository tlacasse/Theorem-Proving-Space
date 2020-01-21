var root = document.getElementById('page');

function splitView(baseView) {
    var oninit = function () { };
    var onchange = function () { };
    if (baseView.oninit) {
        oninit = baseView.oninit;
    }
    if (baseView.onchange) {
        onchange = baseView.onchange;
    }
    return {
        oninit: oninit,
        onchange: onchange,
        view: function () {
            return Templates.splitContent(
                NavBar.view(),
                baseView.view(),
            );
        },
    };
}

m.route(root, '/info', {
    '/info': splitView(Info),
    '/holstep': splitView(HolstepSearch),
});

var App = {};

App.failedPath = '';

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

m.mount(document.getElementById('message-box'), MessageBox);
