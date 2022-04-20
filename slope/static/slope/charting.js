document.addEventListener("DOMContentLoaded", () => {

    // grabbing the JSON data
    const plot = JSON.parse(JSON.parse(document.getElementById('plot_json').textContent))
    const search = JSON.parse(document.getElementById('search').textContent)
    const COLOUR_FOS_DICT = JSON.parse(document.getElementById('COLOUR_FOS_DICT').textContent)
    let max_display_fos = document.getElementById('id_options-max_display_FOS').value

    //initialising things 
    plot_all = document.getElementById('plotly_js')
    search_length = search.length

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
            Plotly.newPlot('plotly_js', plot.data, plot.layout)
    }
    else{
        //if not a mobile screen hide the extra html elements
        Plotly.newPlot('plotly_js', plot.data, plot.layout)
        document.getElementById("mobile_screen_menus").style.display = "none"
    }

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

    for (var i = 0; i < search_length; i += 1) {
        let color;
        let fos;
        if (search[i].FOS < max_display_fos) {

            fos = Math.min(Math.round(search[i].FOS*10)/10,3.0).toString()
            if (fos.length < 2) {
                fos+=".0";
            }
            color = COLOUR_FOS_DICT[fos];

            traces.push({
                'mode':"lines",
                // can probably add a name to help with 'removing' (or making invisible if possible)
                // name proabably related to id in search list.
                'name':"",
                'type':"scattergl",
                x:search[i].x,
                y:search[i].y,
                meta:[Math.round(search[i].FOS*10)/10],
                // hovertemplate not really working at the moment (as only shows for the last
                // node and not all nodes)
                hovertemplate:[`%{meta[0]}`],
                marker : {'color': `${color}`},
            });
        }
        else {
            break
        }
    };
    
    //reversed the order of the traces so that the most critical FOS are drawn on the top
    Plotly.addTraces(plot_all, traces.reverse());


});