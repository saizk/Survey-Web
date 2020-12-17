state_change = (button_idx) =>{
    
    // let survey_state = document.getElementById(`${button_idx}`).value;
    // let survey_status = document.getElementById(`${button_idx}`)

    let survey_state = document.getElementById(button_id).value;
    let survey_status = document.getElementById(status_id)
    survey_status.innerText = "Status: " + survey_state;
    
}