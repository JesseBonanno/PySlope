document.addEventListener("DOMContentLoaded", () => {
    console.log("loaded")
    document.getElementById('loading-spinner').style = "display:none";
    
    document.getElementById('pdf_button').addEventListener("click", trigger_spinner); 



    inputs = document.getElementsByTagName('input');
    for (var i = 0; i < inputs.length; i++){

        inputs[i].oninput = function() {
            document.getElementById('analysis_button').disabled = false
            document.getElementById('pdf_button').disabled = true
        
            document.getElementById('analysis_button').addEventListener("click", trigger_spinner);      
        
        }
    }
    
})

function trigger_spinner(){

    document.getElementById('loading-spinner').style = "display:inline-block";
    setTimeout(()=>{
        document.getElementById('loading-spinner').style = "display:none";
    },
    10000
    )

}