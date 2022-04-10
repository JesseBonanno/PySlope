// based on https://engineertodeveloper.com/dynamic-formsets-with-django/
document.addEventListener("DOMContentLoaded", () => {

    // get the dropdown
    const define_slope_by_dropdown = document.querySelector("#id_options-slope_choice");

    const slope_form = document.querySelectorAll(".Slope-div");

    const angle_row = slope_form[1];
    const length_row = slope_form[2];

    if (define_slope_by_dropdown.value === "length"){
        angle_row.style = "display:none";
    } else {
        length_row.style = "display:none";
    };


    define_slope_by_dropdown.addEventListener('change', function(event) {
        const result = event.target.value;
        console.log(result);

        if (result == "length"){
            angle_row.style = "display:none";
            length_row.style = "display:block";
        } else {
            angle_row.style = "display:block";
            length_row.style = "display:none";
        };

    });

});
