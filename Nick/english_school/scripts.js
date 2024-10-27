// JavaScript code for general functionality

document.addEventListener("DOMContentLoaded", function() {
    // Example: Alert when a button is clicked
    const buttons = document.querySelectorAll("button");
    buttons.forEach(button => {
        button.addEventListener("click", function() {
            alert("Button clicked!");
        });
    });
});
