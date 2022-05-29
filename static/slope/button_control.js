document.addEventListener("DOMContentLoaded", () => {
    console.log("loaded")
    document.getElementById('loading-spinner').style = "display:none";

    document.getElementById('pdf_button').addEventListener("click", trigger_spinner);
    document.getElementById('analysis_button').addEventListener("click", trigger_spinner);
    document.getElementById('reset_button').addEventListener("click", trigger_spinner);



    inputs = document.getElementsByTagName('input');
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].id != 'id_options-max_display_FOS') {
            inputs[i].addEventListener('change', () => {
                document.getElementById('analysis_button').disabled = false

                // for pdf_button it has been changed to a link so need 
                document.getElementById('pdf_button').classList.add('disabled');
                document.getElementById('pdf_button').href = '';
            });
        }

    }
});

function trigger_spinner() {

    document.getElementById('loading-spinner').style = "display:inline-block";
    setTimeout(() => {
        document.getElementById('loading-spinner').style = "display:none";
    },
        10000
    )

}