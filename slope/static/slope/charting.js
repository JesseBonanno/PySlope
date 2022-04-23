// function to update plot
function updatePlot(max_display_fos) {

    // grabbing the JSON data
    const plot = JSON.parse(JSON.parse(document.getElementById('plot_json').textContent))
    const search = JSON.parse(document.getElementById('search').textContent)
    const COLOUR_FOS_DICT = JSON.parse(document.getElementById('COLOUR_FOS_DICT').textContent)
    
    //initialising things 
    const plot_all = document.getElementById('plotly_js')
    const search_length = search.length
    
    // for mobile displays hide the annotations and shapes from the plotly chart and create html info
    if (window.screen.width < 1000) {
        document.getElementById("mobile_screen_menus").style.display = "block"
        plot.layout.annotations = []
        plot.layout.shapes = []

        soils = document.getElementsByClassName('formset-row-Materials')
        soils_count = soils.length
        for (var i = 0; i < soils_count; i += 1) {
            // creating the table of soil properties
            weight = document.getElementById('id_material-'+i+'-unit_weight').value
            friction = document.getElementById('id_material-'+i+'-friction_angle').value
            cohesion = document.getElementById('id_material-'+i+'-cohesion').value
            soil_name = document.getElementById('id_material-'+i+'-name').value
            colour = plot.data[i+1].fillcolor
            var objTo = document.getElementById('mobile_soil_table');
            var tr = document.createElement("tr");
            tr.innerHTML = '<td>'+soil_name+'</td><td style="background-color:'+colour+';"></td><td>'+weight+'</td><td>'+cohesion+'</td><td>'+friction+'</td>';
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
    else{
        //if not a mobile screen hide the extra html elements
        document.getElementById("mobile_screen_menus").style.display = "none"
    }

    // create a new plot
    Plotly.newPlot('plotly_js', plot.data, plot.layout)

    // some values for styling
    var w = document.getElementById('plotly_js').getBoundingClientRect().width
    var h = document.getElementById('plotly_js').getBoundingClientRect().height
    plot.layout.width = w*0.98
    plot.layout.height = w*0.6
    plot.layout.margin= {
        'l':10,
        'r':10,
        'b':10,
        't':10,
        'pad':0
    }

    // define traces at higher level so can use outside for loop scope
    let traces = [];

    // loop through all results
    for (var i = 0; i < search_length; i += 1) {
        let color;
        let fos;

        // if less than FOS than plot
        if (search[i].FOS < max_display_fos) {

            // get the FOS and round to 1 decimal places for coloring purposes
            // if greater than 3 use 3
            fos = Math.min(Math.round(search[i].FOS*10)/10,3).toString()

            // if string length < 2 than is int (ie 2) which needs to be converted to
            // have one decimal place (ie add "".0")
            if (fos.length < 2) {
                fos+=".0";
            }
            
            color = COLOUR_FOS_DICT[fos];

            traces.push({
                'mode':"lines",
                'name':"",
                'type':"scattergl",
                x:search[i].x,
                y:search[i].y,
                hovertemplate: Math.round(search[i].FOS*1000)/1000,
                marker : {'color': `${color}`},
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
document.addEventListener("DOMContentLoaded", () => {
    let max_display_fos = document.getElementById('id_options-max_display_FOS');
    updatePlot(max_display_fos.value)

    max_display_fos.addEventListener("change", (e) => {
            updatePlot(e.currentTarget.value);
    })   
});