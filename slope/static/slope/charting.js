document.addEventListener("DOMContentLoaded", () => {

    // grabbing the JSON data
    plot = JSON.parse(JSON.parse(document.getElementById('plot_json').textContent))
    search = JSON.parse(document.getElementById('search').textContent)

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
    Plotly.newPlot('plotly_js', plot.data, plot.layout, config);


    // check if first load or not and generate the failure surface if not. I used a step of 10 as there were a lot of traces which need to be loaded and it was taking a while
    // maybe it would be better to load the first chart and then do this one afterwards, like 'lazy loading' or use a range slider to move through the results and load them one by one?
    search_length =search.length
    if (search_length>2){
    document.getElementById('plotly_js_all').style.display = 'block'
    Plotly.newPlot('plotly_js_all', plot.data, plot.layout, config)
    plot_data = []
    plot_all = document.getElementById('plotly_js_all')

        for (var i = 0; i < search_length; i += 10) {
            Plotly.addTraces(plot_all, {
                'mode':"lines",
                'name':"",
                'type':"scatter",
                x:search[i].x,
                y:search[i].y
            })
        }
    }
    else{
        document.getElementById('plotly_js_all').style.display = 'none'
    }
})