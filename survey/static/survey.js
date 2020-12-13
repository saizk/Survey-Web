question_count = 0

adder = () => {
    let new_q  = document.createElement("div")
    let new_q_input = document.createElement("input")
    new_q_input.setAttribute("class", `question q${question_count}`)
    new_q_input.setAttribute("name", `question${question_count}`)
    new_q_input.setAttribute("placeholder", 'Type your question')
    new_q_input.setAttribute("autofocus", '')

    new_q.innerText = `Question ${question_count+1}: `
    new_q.appendChild(new_q_input)
    document.getElementById("question_id").appendChild(new_q)

    question_count += 1

    // for(let element of document.getElementsByClassName("question")){
    //     console.log(element.value)
    // }
}