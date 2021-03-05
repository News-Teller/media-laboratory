window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        setMeta: function(title, desc) {
            if (title) {
                document.title = title;
                document.querySelector('meta[property="og:title"]').setAttribute('content', title)
            }
            if (desc) {
                document.querySelector('meta[name="description"]').setAttribute('content', desc);
                document.querySelector('meta[property="og:description"]').setAttribute('content', desc)
            }
        }
    }
});
