var root = document.getElementById('page');

m.route(root, '/', {
    '/': About,
});

// error message
m.mount(document.getElementById('message-box'), ErrorMessage);
