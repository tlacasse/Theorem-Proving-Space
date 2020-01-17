var HolstepHelper = {};

HolstepHelper.pad = function (number, n) {
    return ('0'.repeat(n) + String(number)).slice(-n);
}

var Holstep = (function () {
    "use strict";
    var vm = {};

    vm.hasData = false;
    vm.conjecture = {};
    vm.id = null;
    vm.type = null;

    vm._buttonList = null;

    function set_conjecture(type, id) {
        vm.type = type;
        vm.id = id;
        API.get('holstep/conjecture/' + vm.type + '/' + vm.id,
            function (data) {
                vm.conjecture = TO.conjecture(data);
                vm.hasData = true;
            });
    }

    function oninit() {
        vm.hasData = false;
    }

    /////////////////////////////////////////

    function button(name, classes, type, id) {
        return m('a', {
            class: 'navbar-button ' + classes,
            onclick: function () {
                set_conjecture(type, id);
            },
        }, name)
    }

    function buttonList() {
        var list = [];
        for (var i = 1; i <= 9999; i++) {
            list.push(button(HolstepHelper.pad(i, 5) + ' train', 'color-training', 'train', i));
        }
        for (var i = 1; i <= 1411; i++) {
            list.push(button(HolstepHelper.pad(i, 4) + ' test', 'color-testing', 'test', i));
        }
        return list;
    }

    function right() {
        if (vm.id === null) {
            return '';
        }
        return m('pre', JSON.stringify(vm.conjecture, null, 2));
    }

    function view() {
        return Templates.splitContent(
            NavBar.view(),
            [
                m('div', { id: 'holstep-content-left' }, buttonList()),
                m('div', { id: 'holstep-content-right' }, right()),
            ],
        );
    }

    return {
        oninit: oninit,
        view: view,
        set_conjecture: set_conjecture,
        private: function () {
            return vm;
        },
    };
})();
