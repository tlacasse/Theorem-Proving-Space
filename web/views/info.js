var Info = (function () {
    "use strict";
    var vm = {};

    function content() {
        return [
            m('div', { class: 'section-title' }, 'Info'),
            m('div', { class: 'hrule' }),
            m('br'),
            m('i', 'Generative Modeling of a Continuous Premise-Conjecture Space'),
            m('br'),
            m('br'),
            m('div', { class: 'section-title' }, 'Holstep'),
            m('div', { class: 'hrule' }),
            m('ul', [
                m('li', m('a[href=http://cl-informatik.uibk.ac.at/cek/holstep/]', 'Link')),
                m('li', ['Conjecture search.',
                    m('ul', [
                        m('li', 'Search bar at the top, spaces separate search parameters into different required substrings (ANDs).'),
                        m('li', 'Switch sorting by Id or by Name.'),
                        m('li', 'Navigate through pages of results.'),
                        m('li', 'Click each record to view more details about the conjecture.'),
                    ]),
                ]),
                m('li', ['View individual conjectures.',
                    m('ul', [
                        m('li', 'Pretty-printed and syntax coloring.'),
                        m('li', 'Hover over parenthesis to highlight matching pairs.'),
                    ]),
                ]),
            ]),
            m('br'),
            m('br'),
            m('div', { class: 'section-title' }, 'Mizar Mathematical Library'),
            m('div', { class: 'hrule' }),
            m('ul', [
                m('li', m('a[href=http://www.mizar.org/library/]', 'Link')),
                m('li', ['Theorem search.',
                    m('ul', [
                        m('li', 'Search bar at the top, spaces separate search parameters into different required substrings (ANDs).'),
                        m('li', 'Theorems are not named as in Holstep, instead search conjecture text.'),
                        m('li', 'Navigate through pages of results.'),
                        m('li', 'Click each record to view more details about the theorem.'),
                    ]),
                ]),
                m('li', ['View individual theorems.',
                    m('ul', [
                        m('li', 'Syntax coloring.'),
                        m('li', 'Beginning highlighted text is the conjecture, after that, the proof.'),
                    ]),
                ]),
            ]),
        ];
    }

    function view() {
        return m('div', { class: 'content-area overflow' }, content());
    }

    return {
        view: view,
        private: function () {
            return vm;
        },
    };
})();
