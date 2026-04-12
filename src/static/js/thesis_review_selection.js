(function () {
    var sectionInput = document.getElementById("id_section");
    var selectedTextInput = document.getElementById("id_selected_text");

    if (!sectionInput || !selectedTextInput) {
        return;
    }

    var updateFromSelection = function (event) {
        var selection = window.getSelection();
        var text = selection ? selection.toString().trim() : "";
        if (!text) {
            return;
        }

        selectedTextInput.value = text;
        var section = event.currentTarget.getAttribute("data-section");
        if (section) {
            sectionInput.value = section;
        }
    };

    document.querySelectorAll(".selectable").forEach(function (node) {
        node.addEventListener("mouseup", updateFromSelection);
        node.addEventListener("touchend", updateFromSelection);
    });
})();
