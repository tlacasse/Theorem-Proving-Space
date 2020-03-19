var Visuals = (function () {
    "use strict";
    var vm = {};

    vm.data = null;

    vm.EMPTY_VISUAL = JSON.parse('{"file": "none"}');
    vm.visual = vm.EMPTY_VISUAL;

    vm.plotLayout = {
        hovermode: 'closest',
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0,
        },
    };

    function loadData() {
        if (vm.visual.file !== 'none') {
            API.get('visuals/data/' + vm.visual.file, function (data) {
                vm.data = data;
                createGraph();
            });
        } else {
            App.get('visuals-container').innerHTML = '';
        }
    }

    function getDim(n) {
        return vm.data.map(x => x[n]);
    }

    function createGraph() {
        var points = {
            text: getDim(0),
            x: getDim(1),
            y: getDim(2),
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
        };

        if (vm.visual.actualDim === 3) {
            points.z = getDim(3);
            points.type = 'scatter3d';
            points.hoverinfo = 'x+y+z+text';
        } else {
            if (vm.visual.dim > vm.visual.actualDim) {
                points.z = getDim(2).map(_ => 0);
                points.type = 'scatter3d';
                points.hoverinfo = 'x+y+text';
            } else {
                points.type = 'scatter';
                points.hoverinfo = 'x+y+text';
            }
        }

        Plotly.newPlot('visuals-container', [points], vm.plotLayout);

        App.get('visuals-container').on('plotly_click', function (data) {
            HolstepSearch.goToConjecture(data.points[0].text);
        });
    }

    function oninit() {
        vm.visual = vm.EMPTY_VISUAL;
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
                vm.visual = JSON.parse(e.target.value);
                loadData();
            }
        }, [
                buildDropdownOption('none', 'SELECT'),
                buildDropdownOption('{"file": "holstepview_tsne_2d", "dim": 2, "actualDim": 2}', 'Holstep - tSNE 2D'),
                buildDropdownOption('{"file": "holstepview_tsne_2d", "dim": 3, "actualDim": 2}', 'Holstep - tSNE 2D in 3D'),
                buildDropdownOption('{"file": "holstepview_tsne_3d", "dim": 3, "actualDim": 3}', 'Holstep - tSNE 3D'),
                buildDropdownOption('{"file": "subset_tsne_2d", "dim": 2, "actualDim": 2}', 'Subset - tSNE 2D'),
                buildDropdownOption('{"file": "subset_tsne_2d", "dim": 3, "actualDim": 2}', 'Subset - tSNE 2D in 3D'),
                buildDropdownOption('{"file": "subset_tsne_3d", "dim": 3, "actualDim": 3}', 'Subset - tSNE 3D'),
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
