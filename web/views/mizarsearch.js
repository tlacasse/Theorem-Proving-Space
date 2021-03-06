﻿var MizarSearch = (function () {
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
        query = query.replace(/[^=\w\d\s]/g, '');
        var uri = 'mizar/search/q/' + query;
        if (query === '') {
            uri = 'mizar/search/all';
        }
        API.get(uri, function (data) {
            vm.results = data;
            API.get('mizar/search/info', function (data) {
                vm.countResults = data[0];
                vm.countPages = data[1];
                vm.page = 0;
                vm.hasData = true;
            });
        });
    }

    function delaySearch() {
        if (vm.timeout !== null) {
            clearTimeout(vm.timeout);
        }
        vm.timeout = setTimeout(function () {
            search(vm.query);
        }, 500);
    }

    function nextPage(n) {
        vm.page += n;
        vm.page = clamp(vm.page, 0, vm.countPages - 1);
        API.get('mizar/search/page/' + vm.page, function (data) {
            vm.results = data;
        });
    }

    function goToTheorem(id) {
        m.route.set('/mizar/view/' + String(id));
    }

    /////////////////////////////////////////

    function topBox() {
        return [
            m('input', {
                type: 'text',
                id: 'search-bar',
                placeholder: 'search',
                value: vm.query,
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
        var show1000 = displayIfEnoughPagesStyle(1000);
        return m('table', { class: 'search-info' },
            m('tr', [
                m('td', { class: 'search-info-left' }, vm.countResults + ' results.'),
                m('td', { class: 'search-info-right' }, [
                    m('a', {
                        onclick: function () { nextPage(-100000); },
                    }, '1'),
                    m('a', {
                        style: show1000,
                        onclick: function () { nextPage(-1000); },
                    }, '<<<<'),
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
                        style: show1000,
                        onclick: function () { nextPage(1000); },
                    }, '>>>>'),
                    m('a', {
                        onclick: function () { nextPage(100000); },
                    }, vm.countPages),
                ])
            ])
        );
    }

    function theoremToRecord(data) {
        return m('tr', {
            onclick: function () {
                goToTheorem(data[1]);
            }
        }, [
                m('td', data[0]),
                m('td', data[1]),
                m('td', data[2]),
                m('td', data[3]),
            ]);
    }

    function botBox() {
        if (!vm.hasData) {
            return '';
        }
        var height = (vm.results.length + 1) * 5;
        var records = vm.results.map(theoremToRecord);
        records.unshift(m('tr', [
            m('th', { width: '10%' }, 'Article'),
            m('th', { width: '10%' }, 'Id'),
            m('th', { width: '15%' }, 'Type'),
            m('th', { width: '65%' }, 'Theorem'),
        ]));
        return m('table', {
            height: String(height) + '%',
            id: 'search-results',
        }, records);
    }

    function view() {
        return [
            m('div', { class: 'search-topbox' }, topBox()),
            m('div', { class: 'search-topbox search-midbox' }, midBox()),
            m('div', { class: 'search-botbox' }, botBox()),
        ];
    }

    delaySearch();

    return {
        view: view,
        search: search,
        goToTheorem: goToTheorem,
        nextPage: nextPage,
        getQuery: function () {
            return vm.query;
        },
        private: function () {
            return vm;
        },
    };
})();
