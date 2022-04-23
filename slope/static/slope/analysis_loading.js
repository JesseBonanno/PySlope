// script to lock analysis button after pressing and 
// changing visualisation to show loading
document.addEventListener("DOMContentLoaded", () => {

    let button = document.getElementById('analysis_button');
    let mainform = document.getElementById('mainform');
    let analyse_text = document.getElementById('analyse_text');
    let loading_text = document.getElementById('loading_text');

    button.disabled = false;
    loading_text.style = "display: none";
    analyse_text.style = "display: inline";

    mainform.addEventListener('submit', () => {
        button.disabled = true;
        analyse_text.style = "display: none";
        loading_text.style = "display: inline";

        
    });
});