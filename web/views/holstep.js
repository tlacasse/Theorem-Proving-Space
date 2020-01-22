var HolstepSearch = (function () {
    "use strict";
    var vm = {};

    vm.query = '';
    vm.countResults = null;
    vm.countPages = null;
    vm.page = null;
    vm.results = null;

    vm.hasData = false;
    vm.timeout = null;

    function search(query) {
        query = query.replace(/[^._\w\d\s]/g, '');
        var uri = 'holstep/search/q/' + query;
        if (query === '') {
            uri = 'holstep/search/all'
        }
        API.get(uri, function (data) {
            vm.results = data;
            API.get('holstep/search/info', function (data) {
                vm.countResults = data[0];
                vm.countPages = data[1];
                vm.page = 0;
                vm.hasData = true;
            });
        });
    }

    function delaySearch() {
        if (vm.timeout !== null) {
            console.log('clear');
            clearTimeout(vm.timeout);
        }
        console.log(vm.query);
        vm.timeout = setTimeout(function () {
            search(vm.query);
        }, 500);
    }

    function nextPage(n) {
        vm.page += n;
        vm.page = clamp(vm.page, 0, vm.countPages - 1);
        API.get('holstep/search/page/' + vm.page, function (data) {
            vm.results = data;
        });
    }

    function oninit() {
        delaySearch();
    }

    /////////////////////////////////////////

    function topBox() {
        return [
            m('input', {
                type: 'text',
                id: 'holstep-search',
                placeholder: 'search',
                onkeyup: function (e) {
                    vm.query = e.target.value;
                    delaySearch();
                },
            }),
        ];
    }

    function displayIfEnoughPagesStyle(n) {
        return vm.countPages > n ? '' : 'display: none;';
    }

    function midBox() {
        if (!vm.hasData) {
            return '';
        }

        var show10 = displayIfEnoughPagesStyle(10);
        var show100 = displayIfEnoughPagesStyle(100);
        return m('table', { class: 'holstep-info' },
            m('tr', [
                m('td', { class: 'holstep-info-left' }, vm.countResults + ' results.'),
                m('td', { class: 'holstep-info-right' }, [
                    m('a', {
                        onclick: function () { nextPage(-100000); },
                    }, '1'),
                    m('a', {
                        style: show100,
                        onclick: function () { nextPage(-100); },
                    }, '<<<'),
                    m('a', {
                        style: show10,
                        onclick: function () { nextPage(-10); },
                    }, '<<'),
                    m('a', {
                        onclick: function () { nextPage(-1); },
                    }, '<'),
                    m('span', vm.page + 1),
                    m('a', {
                        onclick: function () { nextPage(1); },
                    }, '>'),
                    m('a', {
                        style: show10,
                        onclick: function () { nextPage(10); },
                    }, '>>'),
                    m('a', {
                        style: show100,
                        onclick: function () { nextPage(100); },
                    }, '>>>'),
                    m('a', {
                        onclick: function () { nextPage(100000); },
                    }, vm.countPages),
                ])
            ])
        );
    }

    function conjectureToRecord(data) {
        return m('tr', [
            m('td', data[1] === 1 ? 'train' : 'test'),
            m('td', data[0]),
            m('td', data[2]),
        ]);
    }

    function botBox() {
        if (!vm.hasData) {
            return '';
        }
        var height = (vm.results.length + 1) * 5;
        var records = vm.results.map(conjectureToRecord);
        records.unshift(m('tr', [
            m('th', { width: '15%' }, 'Type'),
            m('th', { width: '15%' }, 'Id'),
            m('th', { width: '70%' }, 'Conjecture Name'),
        ]));
        return m('table', {
            height: String(height) + '%',
            id: 'holstep-search-results',
        }, records);
    }

    function view() {
        return [
            m('div', { class: 'holstep-topbox' }, topBox()),
            m('div', { class: 'holstep-topbox holstep-midbox' }, midBox()),
            m('div', { class: 'holstep-botbox' }, botBox()),
        ];
    }

    return {
        oninit: oninit,
        view: view,
        search: search,
        getQuery: function () {
            return vm.query;
        },
        private: function () {
            return vm;
        },
    };
})();