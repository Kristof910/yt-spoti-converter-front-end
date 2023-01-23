document.addEventListener("DOMContentLoaded", function() {
    var text = document.querySelector("p");
    text.addEventListener("click", function() {
        alert("You clicked on the text!");
    });
});
