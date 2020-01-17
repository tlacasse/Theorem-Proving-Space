var root = document.getElementById('page');

m.route(root, '/info', {
    '/info': Info,
});

// error message
m.mount(document.getElementById('message-box'), ErrorMessage);
