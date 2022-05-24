// script to update plot to show failure planes

// function to update plot
function createPlot(max_display_fos) {

    // grabbing the JSON data
    const plot = JSON.parse(JSON.parse(document.getElementById('plot_json').textContent))
    const COLOUR_FOS_DICT = JSON.parse(document.getElementById('COLOUR_FOS_DICT').textContent)

    // some values for styling
    const w = window.innerWidth;

    plot.layout.width = w * 0.98
    plot.layout.height = w * 0.6
    plot.layout.margin = {
        'l': 10,
        'r': 10,
        'b': 10,
        't': 10,
        'pad': 0
    }

    // for mobile displays hide the annotations and shapes from the plotly chart and create html info
    if (w < 900) {

        // remove legend and material table
        plot.layout.annotations = []
        plot.layout.shapes = []
        document.getElementById("mobile_screen_menus").style.display = "block"

        if (document.getElementById('mobile_soil_table').childElementCount == 0) {

            soils = document.getElementsByClassName('formset-row-Materials')
            soils_count = soils.length

            for (var i = 0; i < soils_count; i += 1) {
                // creating the table of soil properties
                weight = document.getElementById('id_material-' + i + '-unit_weight').value
                friction = document.getElementById('id_material-' + i + '-friction_angle').value
                cohesion = document.getElementById('id_material-' + i + '-cohesion').value
                soil_name = document.getElementById('id_material-' + i + '-name').value
                colour = plot.data[i + 1].fillcolor
                var objTo = document.getElementById('mobile_soil_table');
                var tr = document.createElement("tr");
                tr.innerHTML = '<td>' + soil_name + '</td><td style="background-color:' + colour + ';"></td><td>' + weight + '</td><td>' + cohesion + '</td><td>' + friction + '</td>';
                objTo.appendChild(tr)
            }

            //creating the html FOS scale
            var objTo = document.getElementById('FOS_legend');
            for (fos_colour in COLOUR_FOS_DICT) {
                var td = document.createElement("td");
                td.style.backgroundColor = COLOUR_FOS_DICT[fos_colour];
                td.style.height = '15px';
                objTo.appendChild(td)
            }
        }
        Plotly.update('plotly_js', plot.data, plot.layout)
    }
    else {
        //if not a mobile screen hide the extra html elements
        document.getElementById("mobile_screen_menus").style.display = "none"
        // create a new plot
        Plotly.newPlot('plotly_js', plot.data, plot.layout)
    }

    updateFOS(max_display_fos);

}
function updateFOS(max_display_fos) {


    // get plot object
    const plot_all = document.getElementById('plotly_js');

    // get search information that was calculated on backend
    const search = JSON.parse(document.getElementById('search').textContent)
    const search_length = search.length;

    //get colour FOS dictionary
    const COLOUR_FOS_DICT = JSON.parse(document.getElementById('COLOUR_FOS_DICT').textContent);
    const MAX_COLOUR_FOS = Object.keys(COLOUR_FOS_DICT).pop()

    // get the highest FOS shown on the plot (if isNan than set to 0)
    let traces_length = plot_all.data.length;
    let previous_fos = 0;

    // get the previous factor of safety, need to loop through since the FOS are
    // added in reverse order to appear better.
    for (let i = 0; i < traces_length; i += 1) {
        previous_fos = plot_all.data[i].hovertemplate;
        if (isNaN(previous_fos) || !previous_fos) {
            continue
        }
        else {
            break
        }
    }

    if (isNaN(previous_fos)) {
        previous_fos = 0;
    };

    // define traces at higher level so can use outside for loop scope
    let traces = [];

    // if fos smaller just purge data and start again?

    // loop through all results and add in new traces if more to be added
    if (max_display_fos > previous_fos) {
        for (var i = 0; i < search_length; i += 1) {
            let color;
            let fos;

            // if below previous continue since already on plot
            if (previous_fos > search[i].FOS) {
                continue;
            }
            // else if below max_display fos then we need to add it in.
            else if (search[i].FOS < max_display_fos) {

                // get the FOS and round to 1 decimal places for coloring purposes
                // if greater than 5 use 5
                fos = Math.min(Math.round(search[i].FOS * 10) / 10, Number(MAX_COLOUR_FOS)).toString()

                // if string length < 2 than is int (ie 2) which needs to be converted to
                // have one decimal place (ie add "".0")
                if (fos.length < 2) {
                    fos += ".0";
                }

                color = COLOUR_FOS_DICT[fos];

                traces.push({
                    'mode': "lines",
                    'name': "",
                    'type': "scattergl",
                    x: search[i].x,
                    y: search[i].y,
                    hovertemplate: Math.round(search[i].FOS * 1000) / 1000,
                    marker: { 'color': `${color}` },
                });
            }
            // if not less than FOS stop (since results are sorted all subsequent results
            // will be greater than FOS)
            else {
                break
            }
        };

        //reversed the order of the traces so that the most critical FOS are drawn on the top
        Plotly.addTraces(plot_all, traces.reverse());
    }

}

document.addEventListener("DOMContentLoaded", () => {
    let max_display_fos = document.getElementById('id_options-max_display_FOS');
    createPlot(max_display_fos.value)

    let stored_latest_fos;

    max_display_fos.addEventListener("change", (e) => {
        // if fos greater update otherwise just create a new graph cause its quicker.
        // get plot object
        let new_fos = e.currentTarget.value;
        if (new_fos > stored_latest_fos) {
            updateFOS(e.currentTarget.value);
        }
        else {
            createPlot(e.currentTarget.value);
        }
        stored_latest_fos = e;

    })
});

window.addEventListener('resize', () => {
    let max_display_fos = document.getElementById('id_options-max_display_FOS');
    createPlot(max_display_fos.value)

})