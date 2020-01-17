var NavBar = (function () {
    "use strict";
    var vm = {};

    function it(title, link) {
        return {
            title: title,
            link: link,
        };
    }

    vm.items = [
        it('Info', 'info'),
        it('Holstep', 'holstep'),
    ];

    /////////////////////////////////////////

    function button(item) {
        var classes = 'navbar-button';
        if (m.route.get() === '/' + item.link) {
            classes += ' selected';
        }
        return m(m.route.Link, {
            href: '/' + item.link,
            class: classes,
            oncreate: m.route.link,
        }, item.title)
    }

    function view() {
        return vm.items.map(item => button(item));
    }

    return {
        view: view,
        private: function () {
            return vm;
        },
    };
})();
