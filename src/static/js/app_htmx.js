(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            var cookies = document.cookie.split(";");
            for (var i = 0; i < cookies.length; i += 1) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    document.body.addEventListener("htmx:configRequest", function (event) {
        var csrfToken = getCookie("csrftoken");
        if (csrfToken) {
            event.detail.headers["X-CSRFToken"] = csrfToken;
        }
    });
})();
