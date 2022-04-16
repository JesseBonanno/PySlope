document.addEventListener("DOMContentLoaded", () => {

    plot_json = document.getElementById("plot_json").textContent
    plot = JSON.parse(JSON.parse(plot_json));
    plot_height = window.innerHeight
    plot_width = window.innerWidth

    plot.layout.height = plot_height*0.8
    plot.layout.width = plot_width*0.8

    Plotly.newPlot('slope_profile', plot.data, plot.layout);


})