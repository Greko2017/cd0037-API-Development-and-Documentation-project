## Getting Setup

### Installing Dependencies, 
### Running Your Frontend in Dev Mode 


1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

3. **Starting the frontend local server**
```bash
cd frontend
```

```bash
npm install
```

```bash
npm start
```


The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.



4. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

5. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
3. **Starting the frontend local server** - make sure your are in `root_path\backend` folder

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run
```



## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }
}
```


`GET '/questions'`

- Fetches a dictionary of data in which the keys are a dictionary of categories, an array questions and the total number of questions (total_questions)
- Request Arguments: page
- Returns: An object pf four keys, `questions`: that contains an object of `id: category_string` key: value pairs, `current_category`: might probably be null, `questions`: a paginated array of questions, `total_questions`: the total nomber of questions in the db

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    ...
  ], 
  "total_questions": 19
}
```


`DELETE /questions/<int:question_id>`

- delete question based on question ID
- Request Arguments: question_id
- Returns: An object with a single key, `id` with the value of the deleted question.

```json
{
    "id": 4
}
```

`POST /questions`

- Create a new question
- body: 
```json
{
    "question": 'What is the coun...',
    "answer": 'Bafia..',
    "difficulty": 3,
    "category": 5',
}
```
- Returns: None


`POST '/questions'`

- fetches questions based on a search term
- body: 

```json
{
    "searchTerm": 'What is the coun...',
}
```
- Returns: An object of three keys,  `questions`: a paginated array of questions, `total_questions`: the total nomber of questions in the db, `current_category`: might probably be null, 

```json
{
    "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
        }, 
        ...
    ], 
    "total_questions": 12,
    "current_category": null
}
```


`GET '/categories/<int:category_id>/questions'`

- fetches questions based on category id
- Request Arguments: category_id
- Returns: An object of three keys,  `questions`: a paginated array of questions, `total_questions`: the total nomber of questions in the db, `current_category`: might probably be null, 

```json
{
    "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
        }, 
        ...
    ], 
    "total_questions": 12,
    "current_category": null
}
```


`POST '/quizzes'`

- fetche  endpoint to get questions to play the quizz
- Request Arguments: previous_questions, quiz_category
- Returns: An object with a keys,  `question`: witch is a randomly selected key, 

```json
{
    "question": {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
}
```


`GET '/categories/<int:category_id>/questions'`

- fetches questions based on category id
- Request Arguments: category_id
- Returns: An object of three keys,  `questions`: a paginated array of questions, `total_questions`: the total nomber of questions in the db, `current_category`: might probably be null, 

```json
{
    "questions": {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
}
```