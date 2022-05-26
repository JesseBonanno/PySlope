function update_pdf_link() {
    let link = document.getElementById('pdf_button');
    let fos = document.getElementById('id_options-max_display_FOS').value;

    // if href = '' something has already changed in the inputs
    // the user isnt allowed to request pdf and as such the 
    // href shal remain '' unless form is the same.
    if (link.href = '') {
        pass;
    } else {
        link.href = `pdf/${fos}`;
    }

}

document.addEventListener('DOMContentLoaded', () => {
    // update value for thing
    update_pdf_link();
    let fos = document.getElementById('id_options-max_display_FOS');
    fos.addEventListener('change', update_pdf_link);

})
