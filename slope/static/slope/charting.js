document.addEventListener("DOMContentLoaded", () => {

    // grabbing the JSON data
    const plot = JSON.parse(JSON.parse(document.getElementById('plot_json').textContent))
    const search = JSON.parse(document.getElementById('search').textContent)
    const COLOUR_FOS_DICT = JSON.parse(document.getElementById('COLOUR_FOS_DICT').textContent)
    let max_display_fos = document.getElementById('id_options-max_display_FOS').value

    // some values for styling
    var config = {responsive: true}
    var w = document.getElementById('plotly_js').getBoundingClientRect().width
    var h = document.getElementById('plotly_js').getBoundingClientRect().height
    plot.layout.width = w
    plot.layout.height = w
    plot.layout.margin= {
        'l':10,
        'r':10,
        'b':10,
        't':10,
        'pad':0
    },

    // create plotly chart for critical FOS
    Plotly.react('plotly_js', plot.data, plot.layout, config);


    // check if first load or not and generate the failure surface if not. I used a step of 10 as there were a lot of traces which need to be loaded and it was taking a while
    // maybe it would be better to load the first chart and then do this one afterwards, like 'lazy loading' or use a range slider to move through the results and load them one by one? 
    search_length = search.length

    document.getElementById('plotly_js_all').style.display = 'block'
    Plotly.newPlot('plotly_js_all', plot.data, plot.layout, config)
    plot_data = []
    plot_all = document.getElementById('plotly_js_all')

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
            Plotly.addTraces(plot_all, traces);
            break
        }
    };
});