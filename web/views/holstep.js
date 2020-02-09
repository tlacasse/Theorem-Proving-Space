var Holstep = (function () {
    "use strict";
    var vm = {};

    vm.conjecture = null;

    vm.parenMap = {};

    function toCodeToken(token, type, props) {
        if (token === '<br>') {
            return m('br');
        }
        var classes = 'code-' + type;
        props.class = classes;
        return m('span', props, token.replaceAll(' ', nbsp()));
    }

    function formatCode(tokens) {
        var final = [];
        function clearParen() {
            var parens = document.getElementsByClassName('code-PAR');
            for (var j = 0; j < parens.length; j++) {
                parens[j].classList.remove('code-PAR-highlight');
            }
        }
        function highlightParen(e) {
            var paren = e.target.id;
            App.get(paren).classList.add('code-PAR-highlight');
            App.get(vm.parenMap[paren]).classList.add('code-PAR-highlight');
        }
        var parenStack = [];
        for (var i = 0; i < tokens.length; i++) {
            var props = {};
            var on = tokens[i][0];
            var type = tokens[i][1];
            if (type === 'PAR') {
                props.onmouseenter = highlightParen;
                props.onmouseleave = clearParen;
                var id = App.uniqueId();
                props.id = id;
                if (on === '(') {
                    parenStack.push(id);
                }
                if (on === ')') {
                    var top = parenStack.pop();
                    vm.parenMap[top] = id;
                    vm.parenMap[id] = top;
                }
            }
            final.push(toCodeToken(on, type, props));
        }
        return final;
    }

    function oninit() {
        vm.parenMap = {};
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
            m('div', { class: 'holstep-code-area' }, formatCode(vm.conjecture.text)),
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
