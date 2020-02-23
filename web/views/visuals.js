var Visuals = (function () {
    "use strict";
    var vm = {};

    vm.data = null;

    vm.visual = 'none';

    vm.plotLayout = {
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0,
        }
    };

    function loadData() {
        if (vm.visual !== 'none') {
            API.get('visuals/data/' + vm.visual, function (data) {
                vm.data = data;
                if (vm.visual.charAt(vm.visual.length - 2) === '3') {
                    createGraph(true);
                } else {
                    createGraph(false);
                }
            });
        } else {
            App.get('visuals-container').innerHTML = '';
        }
    }

    function getDim(n) {
        return vm.data.map(x => x[n]);
    }

    function createGraph(threeDim) {
        var points = {
            x: getDim(0),
            y: getDim(1),
            mode: 'markers',
            marker: {
                symbol: 'circle',
                size: 5,
                line: {
                    color: 'rgba(217, 217, 217, 0.5)',
                    width: 0.5
                },
                opacity: 1,
            },
            type: 'scatter',
        };

        if (threeDim) {
            points.z = getDim(2);
            points.type = 'scatter3d';
        } else {
            points.type = 'scatter';
        }

        Plotly.newPlot('visuals-container', [points], vm.plotLayout);
    }

    function oninit() {
        vm.visual = 'none';
    }

    /////////////////////////////////////////

    function buildDropdownOption(value, display) {
        var attrs = {
            value: value,
        }
        if (vm.visual === value) {
            attrs.selected = 'selected';
        }
        return m('option', attrs, display);
    }

    function buildDropdown() {
        return m('select', {
            class: 'visuals-dropdown',
            onchange: function (e) {
                vm.visual = e.target.value;
                loadData();
            }
        }, [
                buildDropdownOption('none', 'SELECT'),
                buildDropdownOption('holstepview_tsne_2d', 'Holstep - TSNE 2D'),
                buildDropdownOption('holstepview_tsne_3d', 'Holstep - TSNE 3D'),
            ]);
    }

    function view() {
        return [
            buildDropdown(),
            m('div', { class: 'content-area no-padding', id: 'visuals-container' }, ''),
        ];
    }

    return {
        oninit: oninit,
        view: view,
        private: function () {
            return vm;
        },
    };
})();
