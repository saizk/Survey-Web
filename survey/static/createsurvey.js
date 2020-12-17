question_count = 0
question_deleters = []
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




question_adder = () => {
    let htmlString = `
        <div id="question${question_count}">
            <div class="question_div">Question: 
                <input name="num_q${question_count}" class="numq" type="number" min="1">
                <input class="question q${question_count}" 
                        name="question" 
                        placeholder="Type your question">
                <button id="del_question_button${question_count}" type="button" tabindex="-1" onclick="question_deleters[${question_deleters.length}]()"> X </button>
            </div>
            
            <div class="answersfor_q${question_count}">
                <div class="question_type_div">
                    <label for="question_type">  Answer type: </label>
                        <select name="question_type${question_count}" id="question_type${question_count}" onchange="qtype_checker(${question_count})">
                            <option value="one">One-choice</option>
                            <option value="mult">Multiple choice</option>
                            <option value="text">Text</option>
                            <option value="num">Number</option>
                        </select>
                    <button id="add_answer_button${question_count}" type="button" tabindex="-1" onclick="answer_adder(${question_count})">Add answer</button>
                </div>
            </div>
        </div>
    `
    let div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    let global_div = div.firstChild

    let question_list = document.getElementById("question_id")
    question_list.appendChild(global_div)

    // updates the range of the quesiton position when a question is added
    let q_nums = document.getElementsByClassName("numq")
    for (let i = 0; i < q_nums.length; i++) {
        q_nums[i].setAttribute("max", question_list.children.length)
        q_nums[i].value = i + 1
    }
    
    question_deleters.push(() => {
        question_list.removeChild(global_div)
        // updates the range of the question position when a question is deleted 
        for (let i = 0; i < q_nums.length; i++) {
            q_nums[i].setAttribute("max", question_list.children.length)
            q_nums[i].value = Math.min(q_nums[i].value, question_list.children.length)
        }
    })

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

    let answer_list = document.getElementById(`question${question_idx}`).children[1]
    answer_list.appendChild(global_div)

    answer_deleters.push(() => {
        answer_list.removeChild(global_div)
    })
}