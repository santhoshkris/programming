const getApi = () => {
	fetch("http://localhost:8080/api/hello?name='san+'")
        .then(response => response.json())
        .then(data => {console.log(data);});
}

const TestInput = () => {
    getApi();
    return <div>
        <input type="text" id="name" name="name" required
               minLength="4" maxLength="8" size="10" />
    </div>
}

export default TestInput;
