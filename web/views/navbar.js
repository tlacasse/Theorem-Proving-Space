var NavBar = (function () {
    "use strict";
    var vm = {};

    function view() {
        return m('p', 'About');
    }

    return {
        view: view,
        private: function () {
            return vm;
        },
    };
})();
