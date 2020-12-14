
answer_deleters = []
question_count = 0

answer_checker = (question_idx) => {

    let answer_type = document.getElementById(`ans_type${question_idx}`).value
    let button = document.getElementById(`answer_button${question_idx}`)

    let answers = document.getElementsByClassName(`answerfor${question_idx}`)

    if (answer_type === "one" || answer_type ==="mult"){
        button.style.display = "block"
        for (let answer of answers){
            answer.style.display = "block"
        }
    }
    else {
        button.style.display = "none"
        for (let answer of answers){
            answer.style.display = "none"
        }
    }
}

answer_delete = (question_idx) => {

    document.getElementById
}

question_adder = () => {
    let htmlString = `
        <div>
            <div>Question ${question_count+1}: 
                <input class="question q${question_count}" 
                        name="question${question_count}" 
                        placeholder="Type your question">
            
            </div>
            <div class="survey_state">
                <label for="ans_type">  Answer type: </label>
                    <select name="ans_type" id="ans_type${question_count}" onchange="answer_checker(${question_count})">
                        <option value="one">One-choice</option>
                        <option value="mult">Multiple choice</option>
                        <option value="text">Text</option>
                        <option value="num">Number</option>
                    </select>
            </div>
    
            <button id="answer_button${question_count}" type="button" onclick="answer_adder(${question_count})">Add answer</button>
        </div>
    
    `
    
    let div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    global_div = div.firstChild

    document.getElementById("question_id").appendChild(global_div)

    question_count += 1
}

answer_adder = (question_idx) => {

    let htmlString = `
        <div class="answerfor${question_idx}">Answer: 
            <input class="answer q${question_idx}" 
                    name="answer${question_idx}" 
                    placeholder="Type your answer">
            <button id="del_answer_button${question_idx}" type="button" tabindex="-1" onclick="answer_deleters[${answer_deleters.length}]()"> X </button>
        </div>
    `
    let div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    let global_div = div.firstChild

    let question_list = document.getElementById("question_id").children[question_idx]
    question_list.appendChild(global_div)

    answer_deleters.push(() => {
        question_list.removeChild(global_div)
    })
}