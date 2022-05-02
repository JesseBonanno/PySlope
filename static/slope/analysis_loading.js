// script to lock analysis button after pressing and 
// changing visualisation to show loading
document.addEventListener("DOMContentLoaded", () => {

    document.getElementById('loading-spinner').style = "display:none";

    document.getElementById('button-row').addEventListener('click', () => {
        document.getElementById('loading-spinner').style = "display:inline-block";
        setTimeout(()=>{
            document.getElementById('loading-spinner').style = "display:none";
        },
        10000
        )

    })

});