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
        it('Mizar Lib', 'mizar'),
        it('Visualization', 'visuals'),
    ];

    /////////////////////////////////////////

    function button(item) {
        var classes = 'navbar-button';
        var test = '/' + item.link;
        if (m.route.get().slice(0, test.length) === test) {
            classes += ' selected';
        }
        return m(m.route.Link, {
            href: '/' + item.link,
            class: classes,
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
