// https://plot.ly/javascript/3d-scatter-plots/

var TSNE = (function () {
    "use strict";
    var vm = {};

    vm.data = {};

    function load_data() {
        API.get('tsne/data', function (data) {
            vm.data = data;

            var layout = {
                margin: {
                    l: 0,
                    r: 0,
                    b: 0,
                    t: 0,
                }
            };

            function getDim(n) {
                return vm.data.map(x => x[n]);
            }


            var data = {
                x: getDim(0),
                y: getDim(1),
                z: getDim(2),
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
                type: 'scatter3d',
            };

            Plotly.newPlot('tsne-container', [data], layout);
        });
    }

    function oninit() {
        load_data();
    }

    /////////////////////////////////////////

    function view() {
        return m('div', { class: 'content-area no-padding', id: 'tsne-container' }, '');
    }

    return {
        oninit: oninit,
        view: view,
        private: function () {
            return vm;
        },
    };
})();
