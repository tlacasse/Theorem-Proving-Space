function nbsps(n) {
    var result = '';
    for (var i = 0; i < n; i++) {
        result += '\u00A0'
    }
    return result;
}

function nbsp() {
    return nbsps(1);
}

function objectToArray(value) {
    var array = [];
    for (var k in value) {
        if (value.hasOwnProperty(k)) {
            array.push([k, value[k]]);
        }
    }
    return array;
}
