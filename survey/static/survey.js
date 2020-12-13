function createElementFromHTML(htmlString) {
    let div = document.createElement('div');
    div.id = "question_id"
    div.innerHTML = htmlString.trim();
  
    // Change this to div.childNodes to support multiple top-level nodes
    return div.firstChild; 
  }

question_count = 0

adder = () => {
    let my_html_str = `
        <div>Question ${question_count+1}:<input class="question q${question_count}" 
                                                name="question${question_count}" 
                                                placeholder="Type your question" 
                                                autofocus="">
        </div>
        // <div class="survey_state">
        //     <label for="ans_type">  Answer type: </label>
        //         <select name="ans_type" id="ans_type">
        //             <option value="new">One-choice</option>
        //             <option value="new">Multiple choice</option>
        //             <option value="new">Text</option>
        //             <option value="new">Number</option>
        //         </select>
        // </div>
    
    `

    question_count += 1
    createElementFromHTML(my_html_str)
    
    
    // let new_div  = document.createElement("div")
    // let new_input = document.createElement("input")
    // new_div.innerText = `Question ${question_count+1}: `
    // let ans_type = document.createElement("label")
    // ans_type.innerText = "  Answer type: "
    // ans_type.setAttribute("for", "ans_type")

    // new_input.setAttribute("class", `question q${question_count}`)
    // new_input.setAttribute("name", `question${question_count}`)
    // new_input.setAttribute("placeholder", 'Type your question')
    // new_input.setAttribute("autofocus", '')

    // new_div.appendChild(new_input)
    // new_div.appendChild(ans_type)
    // document.getElementById("question_id").appendChild(new_div)

    

    // for(let element of document.getElementsByClassName("question")){
    //     console.log(element.value)
    // }
}