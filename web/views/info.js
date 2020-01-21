var Info = (function () {
    "use strict";
    var vm = {};

    function content() {
        return [
            m('div', { class: 'section-title' }, 'Info'),
            m('div', { class: 'hrule' }),
            m('br'),
            m('ul', [
                m('li', m('a[href=http://cl-informatik.uibk.ac.at/cek/holstep/]', 'Dataset Link')),
            ]),
            m('br'),
            m('iframe', { src: 'http://cl-informatik.uibk.ac.at/cek/holstep/' })
        ];
    }

    function view() {
        return m('div', { class: 'content-area' }, content());
    }

    return {
        view: view,
        private: function () {
            return vm;
        },
    };
})();
