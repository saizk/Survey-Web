function createElementFromHTML(htmlString) {
    let div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    // Change this to div.childNodes to support multiple top-level nodes
    return div.firstChild; 
  }

question_count = 0

adder = () => {
    let my_html_str = `
        <div>Question ${question_count+1}: 
            <input class="question q${question_count}" 
                    name="question${question_count}" 
                    placeholder="Type your question">

            <div class="survey_state">
                <label for="ans_type">  Answer type: </label>
                    <select name="ans_type" id="ans_type">
                        <option value="new">One-choice</option>
                        <option value="new">Multiple choice</option>
                        <option value="new">Text</option>
                        <option value="new">Number</option>
                    </select>
            </div>
        </div>
    
    `
    global_element = createElementFromHTML(my_html_str)
    document.getElementById("question_id").appendChild(global_element)

    question_count += 1
}