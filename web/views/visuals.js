var Visuals = (function () {
    "use strict";
    var vm = {};

    /////////////////////////////////////////

    function view() {
        return m('div', { class: 'content-area no-padding' }, '');
    }

    return {
        view: view,
        private: function () {
            return vm;
        },
    };
})();
