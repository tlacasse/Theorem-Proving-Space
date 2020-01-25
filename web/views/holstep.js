var HolstepCode = (function () {
    "use strict";
    var vm = {};

    vm.getTypeChar = function (char) {
        if (char.match(/[a-z0-9_]/i)) {
            return 'VAR';
        }
        if (char.match(/[\s]/i)) {
            return 'SPC';
        }
        if (char.match(/[\(\)]/i)) {
            return 'PAR';
        }
        return 'SYM'
    }

    vm.getType = function (token) {
        var type = vm.getTypeChar(token.charAt(0));
        if (type === 'VAR' && token.length > 2) {
            return 'FUN';
        }
        return type;
    }

    vm.parse = function (code) {
        var tokenized = [];
        var prev = '';
        var token = '';
        for (var i = 0; i < code.length; i++) {
            var char = code.charAt(i);
            var type = vm.getTypeChar(char);
            if (type !== prev) {
                tokenized.push(token);
                token = '';
            }
            token += char;
            prev = type;
        }
        return tokenized;
    }

    vm.toDisplay = function (code, putId, hide) {
        var attrs = { class: 'holstep-code' };
        if (putId) {
            attrs.id = putId;
        }
        if (hide) {
            attrs.style = 'display: none;';
        }
        var tokens = vm.parse(code);
        tokens = tokens.map(function (t) {
            var classes = 'code-' + vm.getType(t);
            return m('span', { class: classes }, t.replace(' ', '_'));
        });
        return m('div', attrs, tokens);
    }

    function toTwoPart(left, right) {
        return m('div', { class: 'holstep-code-base' },
            m('table', m('tr', [
                left,
                m('td', { class: 'right' }, right),
            ]))
        );
    }

    vm.toTextAndTokenSwapCode = function (codeTXT, codeTOK) {
        var idTXT = App.uniqueId();
        var idTOK = App.uniqueId();
        var viewTXT = vm.toDisplay(codeTXT, idTXT);
        var viewTOK = vm.toDisplay(codeTOK, idTOK, true);
        var button = m('td', {
            class: 'left holstep-code-swap',
            onclick: function (e) {
                var div = e.target;
                var isTXT = div.innerText === 'TXT';
                App.get(idTXT).style.display = isTXT ? 'none' : 'block';
                App.get(idTOK).style.display = isTXT ? 'block' : 'none';
                div.innerText = isTXT ? 'TOK' : 'TXT';
            }
        }, 'TXT');
        return toTwoPart(button, [viewTXT, viewTOK]);
    }

    return vm;
})();

var Holstep = (function () {
    "use strict";
    var vm = {};

    vm.conjecture = null;

    function oninit() {
        vm.conjecture = null;
        API.get('holstep/conjecture/' + m.route.param('id'), function (data) {
            vm.conjecture = TO.conjecture(data);
        });
    }

    /////////////////////////////////////////

    function view() {
        if (vm.conjecture === null) {
            return '';
        }
        var idDesc = (vm.conjecture.isTraining ? 'train' : 'test') + ' ' + vm.conjecture.id;
        return m('div', { class: 'content-area' }, [
            m('table', m('tr', [
                m('td', { class: 'section-title align-left' }, vm.conjecture.name),
                m('td', { class: 'section-title align-right' }, idDesc),
            ])),
            m('div', { class: 'hrule' }),
            m('br'),
            HolstepCode.toTextAndTokenSwapCode(vm.conjecture.text, vm.conjecture.tokens),
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
