// based on https://engineertodeveloper.com/dynamic-formsets-with-django/
document.addEventListener("DOMContentLoaded", () => {


    // support rows
    const addMaterialFormBtn = document.querySelector('#add-Materials-form');
    const addUdlFormBtn = document.querySelector('#add-Udls-form');
    const addPointLoadFormBtn = document.querySelector('#add-PointLoads-form');

    const materialForm = document.getElementsByClassName("formset-row-Materials");
    const udlForm = document.getElementsByClassName("formset-row-Udls");
    const pointLoadForm = document.getElementsByClassName("formset-row-PointLoads");

    const mainMaterialForm = document.querySelector("#formset-Materials");
    const mainUdlForm = document.querySelector("#formset-Udls");
    const mainPointLoadForm = document.querySelector("#formset-PointLoads");

    const totalMaterialForms = document.querySelector('#id_material-TOTAL_FORMS');
    const totalPointLoadForms = document.querySelector('#id_pointload-TOTAL_FORMS');
    const totalUdlForms = document.querySelector("#id_udl-TOTAL_FORMS");


    let materialFormCount = materialForm.length - 1;
    let udlFormCount = udlForm.length - 1;
    let pointLoadFormCount = pointLoadForm.length - 1;

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

    addPointLoadFormBtn.addEventListener('click', function(event) {
        event.preventDefault();
        
        // clone a New Form
        const newPointLoadForm = pointLoadForm[0].cloneNode(true);

        //get end position
        const pointLoadEnd = document.querySelector('#end-row-PointLoads');

        pointLoadFormCount++;
        const pointLoadFormRegex = RegExp(`pointload-(\\d){1}-`, 'g');

        newPointLoadForm.innerHTML = newPointLoadForm.innerHTML.replace(pointLoadFormRegex, `pointload-${pointLoadFormCount}-`)

        // Insert before something lol
        mainPointLoadForm.insertBefore(newPointLoadForm, pointLoadEnd);
        totalPointLoadForms.setAttribute('value', `${pointLoadFormCount+1}`);

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
        
        //point loads
        count = 0;
        const pointLoadFormRegex = RegExp(`pointload-(\\d){1}-`, 'g');
        for (let form of pointLoadForm) {
            for (let cell of form.children) {
                for (let input of cell.children){
                    input.name = input.name.replace(pointLoadFormRegex, `pointload-${count}-`);
                    input.id = input.id.replace(pointLoadFormRegex, `pointload-${count}-`);
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

    mainPointLoadForm.addEventListener("click", function(event) {
        if (event.target.classList.contains("delete-PointLoads-form")) {
            event.preventDefault();
            if (pointLoadFormCount > 0) {
                event.target.parentElement.parentElement.remove();
                pointLoadFormCount--;
                totalPointLoadForms.setAttribute('value', `${pointLoadFormCount+1}`);
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