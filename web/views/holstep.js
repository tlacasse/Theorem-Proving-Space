var Holstep = (function () {
    "use strict";
    var vm = {};

    vm.conjecture = null;

    function oninit() {

    }

    /////////////////////////////////////////

    function view() {
        return [
            m('div', { class: 'section-title' }, m.route.param('id')),
            m('div', { class: 'hrule' }),
        ];
    }

    return {
        oninit: oninit,
        view: view,
        private: function () {
            return vm;
        },
    };
})();
