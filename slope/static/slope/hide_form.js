// script to hide form inputs that are irrelevant
document.addEventListener("DOMContentLoaded", () => {

    /// for slope angle and length
    function updateSlopeForm() {
        const define_slope_by_dropdown = document.querySelector("#id_options-slope_choice");

        const slope_form = document.querySelectorAll(".Slope-div");
        const angle_row = slope_form[1];
        const length_row = slope_form[2];

        if (define_slope_by_dropdown.value === "length") {
            angle_row.style = "display:none";
            length_row.style = "display:block";
        } else {
            angle_row.style = "display:block";
            length_row.style = "display:none";
        };
    }
    updateSlopeForm()

    const define_slope_by_dropdown = document.querySelector("#id_options-slope_choice");
    define_slope_by_dropdown.addEventListener('change', updateSlopeForm)

    // for water table
    function updateWaterForm() {
        const consider_water = document.getElementById('id_watertable-consider_water');
        const water_depth = document.querySelectorAll(".WaterTable-div")[1];
        if (consider_water.checked) {
            water_depth.style = "display:block";
        }
        else {
            water_depth.style = "display:none";
        }
    }
    updateWaterForm()

    const consider_water = document.getElementById('id_watertable-consider_water');
    consider_water.addEventListener('change', updateWaterForm);

    // for limits form
    function updateLimitsForm() {
        // get relevant forms and inputs
        const consider_limits = document.getElementById('id_limits-consider_limits');
        const consider_internal_limits = document.getElementById('id_limits-consider_internal_limits');
        const limits_form = document.querySelectorAll(".Limits-div");

        // define to help with scope issues
        let internal_display;
        let limits_display;

        if (consider_limits.checked && consider_internal_limits.checked) {
            // loop through items below checkbox and either show or hide
            for (let i = 1; i < 6; i++) {
                limits_form[i].style = `display:inline`
            }
        }
        else if (consider_limits.checked) {
            for (let i = 1; i < 4; i++) {
                limits_form[i].style = `display:inline`
            }
            for (let i = 4; i < 6; i++) {
                limits_form[i].style = `display:none`
            }

        }
        else if (!consider_limits.checked) {
            for (let i = 1; i < 6; i++) {
                limits_form[i].style = `display:none`
            }
        }
    }

    updateLimitsForm();

    const consider_limits = document.getElementById('id_limits-consider_limits');
    const consider_internal_limits = document.getElementById('id_limits-consider_internal_limits');
    consider_limits.addEventListener('change', updateLimitsForm)
    consider_internal_limits.addEventListener('change', updateLimitsForm)

});
