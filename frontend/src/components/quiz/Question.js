import AnswersList from "./AnswersList";

const Question = () => {
    const deleteQuestion = (event) =>{
        event.preventDefault();
    }

    return (
        <div className="question">
            <button type="click" onClick={deleteQuestion.bind(this)}>-</button>
            <div>
                <label htmlFor="question">Question text: </label>
                <input type="text" name="question" id="question"/>
            </div>
            <div>
                <label htmlFor="points">Description: </label>
                <input type="number" name="points" id="points" value="1" min="1" max="5"/>
            </div>
            <AnswersList/>
        </div>
    );
}

export default Question;