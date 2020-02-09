var MizarView = (function () {
    "use strict";
    var vm = {};

    vm.theorem = null;
    vm.proof = null;

    vm.parenMap = {};

    function toCodeToken(a) {
        var token = a[0];
        var type = a[1];
        var isProofStep = a[2];
        if (token === '<br>') {
            return m('br');
        }
        var classes = 'code-' + type;
        if (!isProofStep) {
            classes += ' code-theorem-step';
        }
        return m('span', { class: classes }, token.replaceAll(' ', nbsp()));
    }

    function formatCode(tokens) {
        return tokens.map(toCodeToken);
    }

    function oninit() {
        vm.parenMap = {};
        vm.theorem = null;
        vm.proof = null;
        API.get('mizar/theorem/' + m.route.param('id'), function (data) {
            vm.theorem = TO.theorem(data[0]);
            vm.proof = data[1];
        });
    }

    /////////////////////////////////////////

    function view() {
        if (vm.theorem === null) {
            return '';
        }
        var desc = vm.theorem.article + ' ' + vm.theorem.type + ' ' + vm.theorem.id;
        return m('div', { class: 'content-area' }, [
            m('div', { class: 'section-title' }, desc),
            m('div', { class: 'hrule' }),
            m('br'),
            m('div', { class: 'view-code-area' }, formatCode(vm.proof)),
        ]);
    }

    return {
        oninit: oninit,
        view: view,
        private: function () {
            return vm;
        },
    };
})();
