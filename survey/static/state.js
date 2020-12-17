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




window.addEventListener("load", () => {


    let surveys = document.getElementsByClassName("survey")

    for (let survey of surveys){

        if (survey.getAttribute("data") === "new" ){
            
            survey.getElementsByClassName("button_new")[0].setAttribute("checked", "")

        }   
        else if (survey.getAttribute("data") === "online" ){

            survey.getElementsByClassName("button_online")[0].setAttribute("checked", "")
        } 
        else if (survey.getAttribute("data") === "closed" ){

            survey.getElementsByClassName("button_closed")[0].setAttribute("checked", "")
        } 

    }

})