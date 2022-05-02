// to automatically select main tab to help with way page is displayed
document.addEventListener("DOMContentLoaded", () => {
    let form = document.getElementById('Slope-tab');
    window.setTimeout(() => {
        form.click();
    }, 200);
});