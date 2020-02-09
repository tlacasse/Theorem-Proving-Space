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
    '/holstep/view/:id': splitView(HolstepView),
    '/mizar': splitView(MizarSearch),
    '/mizar/view/:id': splitView(MizarView),
    '/cluster': splitView(Cluster),
});

m.mount(document.getElementById('message-box'), MessageBox);
