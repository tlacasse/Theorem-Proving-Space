var HolstepCode = (function () {
    "use strict";
    var vm = {};

    vm.parenMap = {};

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
            if (type !== prev || char === '(' || char === ')') {
                tokenized.push([token, vm.getType(token)]);
                token = '';
            }
            token += char;
            prev = type;
        }
        return tokenized;
    }

    function toCodeToken(token, type, props) {
        var classes = 'code-' + type;
        props.class = classes;
        return m('span', props, token.replace(' ', '_'));
    }

    function sizeOfNextParenBlock(tokens, i) {
        i++;
        var count = 0;
        while (tokens[i][0] !== ')') {
            if (tokens[i][0] === '(') {
                return 1000;
            }
            if (vm.getType(tokens[i][0]) !== 'SPC') {
                count++;
            }
            i++;
        }
        return count;
    }

    vm.prettyprintTXT = function (code) {
        var result = []
        var tokens = vm.parse(code);
        var indent = 0;
        function addNewLine() {
            result.push(m('br'));
            for (var j = 0; j < indent; j++) {
                result.push(['__', 'SPC']);
            }
        }
        for (var i = 0; i < tokens.length; i++) {
            var on = tokens[i][0];
            var type = tokens[i][1];
            function addToResult() {
                result.push([on, type]);
            }
            if (type === 'PAR') {
                if (on === '(') {
                    if (sizeOfNextParenBlock(tokens, i) <= 3) {
                        function addCurrentToken() {
                            result.push([tokens[i][0], tokens[i][1]]);
                        }
                        while (tokens[i][0] !== ')') {
                            addCurrentToken();
                            i++;
                        }
                        addCurrentToken();
                    } else {
                        addToResult();
                        indent++;
                        addNewLine();
                    }
                } else if (on === ')') {
                    indent--;
                    addNewLine();
                    addToResult();
                } else {
                    addToResult();
                }
            } else {
                addToResult();
            }
        }
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
        for (var i = 0; i < result.length; i++) {
            if (Array.isArray(result[i])) {
                var props = {};
                var on = result[i][0];
                var type = result[i][1];
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
            } else {
                final.push(result[i]);
            }
        }
        return final;
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
        tokens = tokens.map(function (toktype) {
            var token = toktype[0];
            var type = toktype[1];
            var classes = 'code-' + type;
            return m('span', { class: classes }, token.replace(' ', '_'));
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

    vm.toPrettyVersion = function (code) {
        return m('div', { class: 'holstep-code-area' }, vm.prettyprintTXT(code));
    }

    return vm;
})();

var Holstep = (function () {
    "use strict";
    var vm = {};

    vm.conjecture = null;

    function oninit() {
        HolstepCode.parenMap = {};
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
            //HolstepCode.toTextAndTokenSwapCode(vm.conjecture.text, vm.conjecture.tokens),
            HolstepCode.toPrettyVersion(vm.conjecture.text),
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
