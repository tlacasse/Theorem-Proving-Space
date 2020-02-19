var Chart = {};

// https://observablehq.com/@d3/force-directed-graph

Chart.color = function () {
    var scale = d3.scaleOrdinal(d3.schemeCategory10);
    return d => scale(d.group);
}

Chart.drag = function (simulation) {
    function dragstarted(d) {
        if (!d3.event.active) {
            simulation.alphaTarget(0.3).restart();
        }
        d.fx = d.x;
        d.fy = d.y;
    }
    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }
    function dragended(d) {
        if (!d3.event.active) {
            simulation.alphaTarget(0);
        }
        d.fx = null;
        d.fy = null;
    }
    return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
}

Chart.makeChart = function (data, width, height) {
    var color = Chart.color;
    var drag = Chart.drag;
    var links = data.links.map(d => Object.create(d));
    var nodes = data.nodes.map(d => Object.create(d));

    var simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    var svg = d3.create("svg")
        .attr("viewBox", [0, 0, width, height]);

    var link = svg.append("g")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", d => Math.sqrt(d.value));

    var node = svg.append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5)
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", 5)
        .attr("fill", color)
        .call(drag(simulation))
        .on('click', function () {
            var id = d3.select(this)._groups[0][0].textContent;
            HolstepSearch.goToConjecture(id);
        });

    node.append("title")
        .text(d => d.id);

    // https://bl.ocks.org/mbostock/1129492

    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node.attr("cx", function (d) { return d.x = Math.max(0, Math.min(width, d.x)); })
            .attr("cy", function (d) { return d.y = Math.max(0, Math.min(height, d.y)); });
    });

    return svg.node();
}

var Cluster = (function () {
    "use strict";
    var vm = {};

    vm.data = {};

    function load_data() {
        API.get('cluster/data', function (data) {
            vm.data = data;
            var dim = getDim();
            App.get('cluster-container').append(Chart.makeChart(vm.data, dim[0], dim[1]));
        });
    }

    function getDim() {
        var area = App.get('content-right');
        var ratio = area.clientWidth / area.clientHeight;
        var height = 640;
        var width = height * ratio;
        return [width, height];
    }

    function oninit() {
        load_data();
    }

    /////////////////////////////////////////

    function view() {
        return m('div', { class: 'content-area no-padding', id: 'cluster-container' }, '');
    }

    return {
        oninit: oninit,
        view: view,
        private: function () {
            return vm;
        },
    };
})();
