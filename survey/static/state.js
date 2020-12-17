state_change = (button_id, status_id, save_button_id, hidden_id) =>{
    
    // value of the triple button
    let survey_state = document.getElementById(button_id).value;   
    // survey status
    let survey_status = document.getElementById(status_id)
    
    document.getElementById(hidden_id).value = survey_state;

    survey_status.innerText = "Status: " + survey_state; 

    let save_button = document.getElementById(save_button_id); 
    save_button.style.display = "block"   

}

// check_uncheck = (button_id, status_id)  =>{
    
//     let button_value =  document.getElementById(button_id).value;

//     let current_status = document.getElementById(status_id)
//     current_status.innerText.slice(9);

//     console.log(current_status.innerText)

//     if (current_status === button_value){
//         document.getElementById(button_id).checked = true
//     }
// }