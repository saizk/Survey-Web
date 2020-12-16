question_count = 0
// question_deleters = []
answer_deleters = []

qtype_checker = (question_idx) => {  // checks when the answer type changes

    let answer_type = document.getElementById(`question_type${question_idx}`).value  // value of the select
    let button = document.getElementById(`add_answer_button${question_idx}`) // "add answer" button
    let answers = document.getElementsByClassName(`answerfor${question_idx}`)  // div for answers

    if (answer_type === "one" || answer_type ==="mult"){
         // displays the "add answer" button
        button.style.display = "block"
        for (let answer of answers){
            // displays all the question's answers 
            answer.style.display = "block"
        }
    }
    else {
        // hides the "add answer" button
        button.style.display = "none"
        for (let answer of answers){
            // hides all the question's answers 
            answer.style.display = "none"
        }
    }
}

// question_remove = (question_idx) => {

//     document.getElementById(`del_question_button${question_idx}`).style.display = "none"
//     document.getElementById(`question${question_idx}`).style.display = "none"
// }


/* <button id="del_question_button${question_count}" type="button" tabindex="-1" onclick="question_remove(${question_count})"> X </button> */


question_adder = () => {
    let htmlString = `
        <div name="question${question_count}">
            <div class="question_div">Question ${question_count+1}: 
                <input class="question q${question_count}" 
                        name="question" 
                        placeholder="Type your question">
            </div>
            <div class="question_type_div">
                <label for="question_type">  Answer type: </label>
                    <select name="question_type${question_count}" id="question_type${question_count}" onchange="qtype_checker(${question_count})">
                        <option value="one">One-choice</option>
                        <option value="mult">Multiple choice</option>
                        <option value="text">Text</option>
                        <option value="num">Number</option>
                    </select>
            </div>
            <button id="add_answer_button${question_count}" type="button" onclick="answer_adder(${question_count})">Add answer</button>

        </div>
    
    `
    let div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    let global_div = div.firstChild

    document.getElementById("question_id").appendChild(global_div)

    // let question_list = document.getElementById("question_id").children[question_count]
    // question_list.appendChild(global_div)

    // question_deleters.push(() => {
    //     question_list.removeChild(global_div)
    // })

    answer_adder(question_count)
    question_count += 1
}

answer_adder = (question_idx) => {

    let htmlString = `
        <div class="answerfor${question_idx}">Answer: 
            <input class="answer q${question_idx}" 
                    name="answerfor${question_idx}" 
                    placeholder="Type your answer">
            <button id="del_answer_button${question_idx}" type="button" tabindex="-1" onclick="answer_deleters[${answer_deleters.length}]()"> X </button>
        </div>
    `
    let div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    let global_div = div.firstChild

    let answer_list = document.getElementById("question_id").children[question_idx]
    answer_list.appendChild(global_div)

    answer_deleters.push(() => {
        answer_list.removeChild(global_div)
    })
}



state_change = (button_id, status_id) =>{
    
    let survey_state = document.getElementById(button_id).value;   
    let survey_status = document.getElementById(status_id)
    survey_status.innerText = "Status: " + survey_state; 
    
    
}








