const Answer = () => {
    const deleteAnswer = (event) => {
        event.preventDefault();
    }

    return (
        <div className="answer">
            <button type="click" onClick={deleteAnswer.bind(this)}>-</button>
            <div>
                <label htmlFor="answer">Answer text: </label>
                <input type="text" name="answer" id="answer"/>
            </div>
            <div>
                <label htmlFor="is_correct">Is correct answer: </label>
                <input type="checkbox" name="is_correct" id="is_correct"/>
            </div>
        </div>
    );
}

export default Answer;