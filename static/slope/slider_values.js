document.addEventListener("DOMContentLoaded", ()=> {
    
    updateSliderValues();
    
})

function updateSliderValues() {
    // get all sliders
    var sliders = document.querySelectorAll('input[type="range"]');
    
    for (var i = 0; i < sliders.length; i += 1) {
        var slider = sliders[i];
        var textnode = document.createElement("p");
        textnode.style = "display:inline-block"
        textnode.innerText = slider.value;

        slider.parentElement.appendChild(textnode);

        // Update the current slider value (each time you drag the slider handle)
        slider.oninput = function() {
            var number_children = this.parentElement.childElementCount;
            this.parentElement.children[number_children-1].innerHTML = this.value;
        }
    };

}