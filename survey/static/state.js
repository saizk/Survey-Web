state_change = (button_id, status_id, save_button_id, hidden_id, checked_button_id) =>{
    
    
    let survey_state = document.getElementById(button_id).value;   
    let survey_status = document.getElementById(status_id)
    
    document.getElementById(hidden_id).value = survey_state;

    survey_status.innerText = "Status: " + survey_state; 

    let save_button = document.getElementById(save_button_id); 
    save_button.style.display = "block"

    // esto es lo que se me ha ocurrido pero no funciona
    // document.getElementById(checked_button_id).checked = false;
    // document.getElementById(button_id).checked = true;

}

// esto se supone que podria ir en el submit button. no se
// check_uncheck = (button_id, checked_button_id) =>{

//     status_value = document.getElementsByName("survey_status").value

//     document.get
    

// }