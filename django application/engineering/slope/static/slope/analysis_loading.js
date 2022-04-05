first_load = true

document.addEventListener("DOMContentLoaded", () => {
    slip_center_y = document.getElementById('y').textContent
    document.getElementById("soil_profile").height = document.getElementById("soil_profile").parentElement.clientWidth;
    generate_chart()

    })

    function generate_chart() {
        plane_fos = Math.round(parseFloat(document.getElementById('fos').textContent)* 1000) / 1000

        soil_count = document.getElementsByClassName("formset-row-Materials").length;

        slope_height = document.getElementById('id_slope-height').value
        slope_angle = document.getElementById('id_slope-angle').value
        slope_length = document.getElementById('id_slope-length').value

        slope_coords = JSON.parse(document.getElementById('slope_coords').textContent)
        soil_dict = []

        annotation_holder = []
        center_x = parseFloat(document.getElementById('x').textContent)
        center_y = parseFloat(document.getElementById('y').textContent)
        radius = parseFloat(document.getElementById('radius').textContent)


        min_x = center_x-radius
        max_x = center_x+radius
        min_y = center_y-radius
        max_y = center_y+radius

        //Stevan 05/04/22 this annotation for the ellipse isn't needed, just leaving it in for now incase I change my mind
        holder =             
            {box0: {
                type: 'ellipse',
                xMin: min_x,
                xMax: max_x,
                yMin: min_y,
                yMax: max_y,
                backgroundColor: 'rgba(255,255,255,0.5)',
                borderColor: 'rgba(0,0,0,0.5)',
                borderWidth: 1,
              },
              }
            
            annotation_holder = []




        color = getRandomColor()       
        soil_base = slope_coords[3][1]

        soil_dict_holder = {
            label: 'Ground level',
            data: [{
                'x': slope_coords[0][0],
                'y': slope_coords[0][1]
              },
              {
                'x': slope_coords[1][0],
                'y': slope_coords[1][1]
              },
              {
                'x': slope_coords[2][0],
                'y': slope_coords[2][1]
              },   
              {
                'x': slope_coords[3][0],
                'y': slope_coords[3][1]
              },],
            fill: false,
            pointRadius:0,  
            backgroundColor: color,
            borderColor: 'rgb(0, 0, 0)',
        }

        model_bottom = {
            label: 'Model bottom',
            data: [{
                'x': 0,
                'y': 0
              },
              {
                'x': slope_coords[3][0],
                'y': 0
              },
            ],
            fill: '-1',
            pointRadius:0,  
            backgroundColor: color,
            borderColor: 'rgb(0,0,0, 0.5)',
        }

        soil_dict.push(soil_dict_holder)


        //Stevan 05/04/22 iterarting through the django form which is brought to the front end to build the chart

        for (let i = 0; i < soil_count; i++) {
            soil_number = i+1
            color = getRandomColor()
    
            depth = document.getElementById('id_material-'+i+'-depth_to_bottom').value

            slope_start = slope_coords[1][0]
            slope_end = slope_coords[2][0]
            slope_length = slope_end-slope_start

            slope_top = slope_coords[0][1]
            slope_base = slope_coords[3][1]
            slope_depth = slope_top - slope_base
                        
            if(depth>slope_depth) {
                strata = {
                    label: 'holder',
                    data: [{
                        'x': slope_coords[0][0],
                        'y': slope_top-depth
                    },  
                    {
                        'x': slope_coords[3][0],
                        'y': slope_top-depth
                    },],
                    fill: '-1',
                    pointRadius:0,  
                    backgroundColor: color,
                    borderColor: 'rgb(0, 0, 0)',
                }
            }
            else {


                if (slope_length>0){
                    slope_factor = slope_depth/slope_length
                    slope_intersect = slope_coords[1][0] + slope_factor*depth
                }
                else{
                    slope_intersect = slope_start
                }

                strata = {
                    label: 'holder',
                    data: [{
                        'x': slope_coords[0][0],
                        'y': slope_top-depth
                    },
                    {
                        'x': slope_intersect,
                        'y': slope_top-depth
                    },
                    {
                        'x': slope_coords[2][0],
                        'y': slope_coords[2][1]
                      },   
                      {
                        'x': slope_coords[3][0],
                        'y': slope_coords[3][1]
                      },],
                    fill: '-1',
                    pointRadius:0,  
                    backgroundColor: color,
                    borderColor: 'rgb(0, 0, 0)',
                }                
            }
            soil_dict.push(strata)
    
    
            }

            soil_dict.push(model_bottom)


            //Stevan 05/04/22 marking the centre of the slip surface and labelling it with the FOS

            Chart.register(ChartDataLabels);
            Chart.defaults.set('plugins.datalabels', {
                display: false
              });

            soil_dict.push({
                label: plane_fos,
                data: [{
                  x: center_x,
                  y: center_y,
                }],
                borderWidth: 2,
                borderColor: 'rgb(0, 0, 0, 1)',
                backgroundColor: 'rgb(0, 0, 0)',
                pointRadius: 4,
                pointRotation: 0,              
                pointHitRadius: 10,
                pointHoverRadius: 6,
                rotation: 90,
                pointStyle: 'circle',
                datalabels: {
                  color:'black',
                  display: true,
                  align: 45,
                  offset:5,
                  anchor: 'start',
                  font:{
                      weight: 'bold',
                    }
                }
              })


              //Stevan 05/04/22 using this function below to generate the slip surface. This might be buggy I didnt check it properly yet
              circle_coords = []
              circle_coords.push(({'x': center_x, 'y':center_y}))

              var items = 100;
              for(var i = 0; i < items; i++) {

                  var x = center_x + radius * Math.cos(2 * Math.PI * i / items);
                  var y = center_y + radius * Math.sin(2 * Math.PI * i / items); 
                  if (x>=center_x && y>slope_base){}
                  else if (x<center_x && y>slope_top){}
                  else{
                    circle_coords.push({'x': x, 'y':y})
                  }
              }
              circle_coords.push(({'x': center_x, 'y':center_y}))

              soil_dict.push({
                label: plane_fos,
                data: circle_coords,
                borderWidth: 2,
                borderColor: 'rgb(0, 0, 0, 0.5)',
                backgroundColor: 'rgb(0, 0, 0)',
                pointRadius: 0,

              })



            
        if (first_load == false) 
        {    
        myChart1.options.plugins.annotation.annotations = annotation_holder    
        myChart1.data.datasets = soil_dict
        myChart1.options.scales.y.min = -height-3
        myChart1.update()
        }
        else {
        first_load = false
        var ctx = document.getElementById('soil_profile').getContext('2d');
        myChart1 = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: soil_dict
        },
        options: {
        scales: {
            x: {
            type: 'linear',
            position: 'bottom',
            },
            y: {
            type: 'linear',
            position: 'left',
            max: center_y+5,
            }
        },
        plugins: {
            legend: {
                display: false
                },        autocolors: false,
            annotation: {
            annotations: 

                annotation_holder

                
            },
            datalabels: {
                formatter: function(value, context) {
                if (context.dataset.data.length > 1) {
                  if (context.dataIndex === 1)
                {
                  return context.dataset.label;
                }
                return "";
                }
                else {
                  return context.dataset.label
                }
              },
            }
        }
        }
        }); 
    }


    }


    function getRandomColor() {
        var trans = '0.5'; // 50% transparency
        var color = 'rgba(';
        for (var i = 0; i < 3; i++) {
          color += Math.floor(Math.random() * 255) + ',';
        }
        color += trans + ')'; // add the transparency
        return color;
      }