var root = document.getElementById('page');

m.route(root, '/', {
    '/': Info,
});

// error message
m.mount(document.getElementById('message-box'), ErrorMessage);
