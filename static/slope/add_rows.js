// based on https://engineertodeveloper.com/dynamic-formsets-with-django/
// javascript script to ad rows to formsets
document.addEventListener("DOMContentLoaded", () => {


    // support rows
    const addMaterialFormBtn = document.querySelector('#add-Materials-form');
    const addUdlFormBtn = document.querySelector('#add-Udls-form');
    const addLineLoadFormBtn = document.querySelector('#add-LineLoads-form');

    const materialForm = document.getElementsByClassName("formset-row-Materials");
    const udlForm = document.getElementsByClassName("formset-row-Udls");
    const lineLoadForm = document.getElementsByClassName("formset-row-LineLoads");

    const mainMaterialForm = document.querySelector("#formset-Materials");
    const mainUdlForm = document.querySelector("#formset-Udls");
    const mainLineLoadForm = document.querySelector("#formset-LineLoads");

    const totalMaterialForms = document.querySelector('#id_material-TOTAL_FORMS');
    const totalLineLoadForms = document.querySelector('#id_lineload-TOTAL_FORMS');
    const totalUdlForms = document.querySelector("#id_udl-TOTAL_FORMS");


    let materialFormCount = materialForm.length - 1;
    let udlFormCount = udlForm.length - 1;
    let lineLoadFormCount = lineLoadForm.length - 1;

    addMaterialFormBtn.addEventListener('click', function(event) {
        event.preventDefault();
        
        // clone a New Form
        const newMaterialForm = materialForm[0].cloneNode(true);

        //get end position
        const materialEnd = document.querySelector('#end-row-Materials');

        materialFormCount++;
        const materialFormRegex = RegExp(`material-(\\d){1}-`, 'g');

        newMaterialForm.innerHTML = newMaterialForm.innerHTML.replace(materialFormRegex, `material-${materialFormCount}-`)

        // Insert before something lol
        mainMaterialForm.insertBefore(newMaterialForm, materialEnd);
        totalMaterialForms.setAttribute('value', `${materialFormCount+1}`);

        return false

    });

    addLineLoadFormBtn.addEventListener('click', function(event) {
        event.preventDefault();
        
        // clone a New Form
        const newLineLoadForm = lineLoadForm[0].cloneNode(true);

        //get end position
        const lineLoadEnd = document.querySelector('#end-row-LineLoads');

        lineLoadFormCount++;
        const lineLoadFormRegex = RegExp(`lineload-(\\d){1}-`, 'g');

        newLineLoadForm.innerHTML = newLineLoadForm.innerHTML.replace(lineLoadFormRegex, `lineload-${lineLoadFormCount}-`)

        // Insert before something lol
        mainLineLoadForm.insertBefore(newLineLoadForm, lineLoadEnd);
        totalLineLoadForms.setAttribute('value', `${lineLoadFormCount+1}`);

    });


    addUdlFormBtn.addEventListener('click', function(event) {
        event.preventDefault();
        
        // clone a New Form
        const newUdlForm = udlForm[0].cloneNode(true);

        //get end position
        const udlEnd = document.querySelector('#end-row-Udls');

        udlFormCount++;
        const udlFormRegex = RegExp(`udl-(\\d){1}-`, 'g');

        newUdlForm.innerHTML = newUdlForm.innerHTML.replace(udlFormRegex, `udl-${udlFormCount}-`)

        // Insert before something lol
        mainUdlForm.insertBefore(newUdlForm, udlEnd);
        totalUdlForms.setAttribute('value', `${udlFormCount+1}`);


    });

    function updateForms(event) {
        //material
        let count = 0;
        const materialFormRegex = RegExp(`material-(\\d){1}-`, 'g');
        for (let form of materialForm) {
            for (let cell of form.children) {
                for (let input of cell.children){
                    input.name = input.name.replace(materialFormRegex, `material-${count}-`);
                    input.id = input.id.replace(materialFormRegex, `material-${count}-`);
                }
            }
            count++;
        }
        
        //line loads
        count = 0;
        const lineLoadFormRegex = RegExp(`lineload-(\\d){1}-`, 'g');
        for (let form of lineLoadForm) {
            for (let cell of form.children) {
                for (let input of cell.children){
                    input.name = input.name.replace(lineLoadFormRegex, `lineload-${count}-`);
                    input.id = input.id.replace(lineLoadFormRegex, `lineload-${count}-`);
                }
            }
            count++;
        }

        // distributed loads
        count = 0;
        const udlFormRegex = RegExp(`udl-(\\d){1}-`, 'g');
        for (let form of udlForm) {
            for (let cell of form.children) {
                for (let input of cell.children){
                    input.name = input.name.replace(udlFormRegex, `udl-${count}-`);
                    input.id = input.id.replace(udlFormRegex, `udl-${count}-`);
                }
            }
            count++;
        }
    };

    mainMaterialForm.addEventListener("click", function(event) {
        if (event.target.classList.contains("delete-Materials-form")) {
            event.preventDefault();
            if (materialFormCount > 0) {
                event.target.parentElement.parentElement.remove();
                materialFormCount--;
                totalMaterialForms.setAttribute('value', `${materialFormCount+1}`);
            }
            updateForms(event);
        }
    })

    mainLineLoadForm.addEventListener("click", function(event) {
        if (event.target.classList.contains("delete-LineLoads-form")) {
            event.preventDefault();
            if (lineLoadFormCount > 0) {
                event.target.parentElement.parentElement.remove();
                lineLoadFormCount--;
                totalLineLoadForms.setAttribute('value', `${lineLoadFormCount+1}`);
            }
            updateForms(event);
        }
    })

    mainUdlForm.addEventListener("click", function(event) {
        if (event.target.classList.contains("delete-Udls-form")) {
            event.preventDefault();
            if (udlFormCount > 0) {
                event.target.parentElement.parentElement.remove();
                udlFormCount--;
                totalUdlForms.setAttribute('value', `${udlFormCount+1}`);
            }
            updateForms(event);
        }
    })
});