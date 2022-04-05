document.addEventListener("DOMContentLoaded", () => {
    let button = document.querySelector('#analsis_button');
    button.disabled = false;
    button.addEventListener('click', () => {
        button.disabled = true;
    })