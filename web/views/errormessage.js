/**
 * Popup Exception Display.
 */
var ErrorMessage = (function () {
    "use strict";
    var vm = {};

    // exception object from server, passed through 'objectToArray'
    vm.exception = [['', '']];

    function show(exceptionObject) {
        get('message-box').style.display = 'block';
        vm.exception = objectToArray(exceptionObject.response);
    }

    function hide() {
        get('message-box').style.display = 'none';
    }

    ////////////////////// View

    function propertyPairToRow(pair) {
        return (
            m('div', { class: 'message-box-pair' }, [
                m('div', { class: 'message-box-key' }, pair[0]),
                m('div', { class: 'message-box-value' }, pair[1]),
            ])
        );
    }

    function view() {
        return [
            m('div', { class: 'message-box-title' },
                m('button', {
                    class: 'message-box-button',
                    onclick: hide
                }, 'X')
            ),
            m('div', { class: 'message-box-detail' },
                vm.exception.map(x => propertyPairToRow(x))
            ),
        ];
    }

    return {
        view: view,
        show: show,
        hide: hide,
    };
})();