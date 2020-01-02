var About = (function () {
    "use strict";
    var vm = {};

    function view() {
        return Templates.splitContent(
            NavBar.view(),
            m('p', '--About--'),
        );
    }

    return {
        view: view,
        private: function () {
            return vm;
        },
    };
})();
