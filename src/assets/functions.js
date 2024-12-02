window.myNamespace = Object.assign({}, window.myNamespace, {
    window_width: {
        get_window_width: function() {
            return window.innerWidth
        }
    }
});