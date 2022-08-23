# API Documentation

The following endpoints have been implemented to be consumed by the frontend and the backend server is not yet hosted, thus to hit any of the implemented API, the backend server URL is http://127.0.0.1:5000 while the respective paths are mentioned along with each of the below APIs.

Each of the endpoints returns some data and this is also detailed for each API and if any of the API encountered an error, the error has also been configured to send back helpful data to inform its users of what might be likely going wrong.

For each of the endpoints, I have explained them using the expected **url**, **parameter**, and **returned data**.

### API examples
    
#### To get list of categories
>   * url :- `GET http://127.0.0.1:5000/categories`
>   * parameter / data :- not required
>   * returned data :- On successful operation, it returns the list of categories in form of key:value pair as shown below. But if no category is found, it returns `404` error.
    > ```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
  ], 
  "success": true
}
    ```
    > As shown above, categories key contains a list of category objects, with each category having id and type keys and values. The success key is used to indicate that an operation's status, it returns True if operation is successful and false if not.
      
      
#### To get list of questions
>   * url :- `GET http://127.0.0.1:5000/questions?page=1`
>   * parameter / data :- page=1. This will send only the first 10 questions as this endpoint paginates and sends list of questions per `page` and if `page` parameter is not specified, it defaults to `page=1`. To fetch the next paginated list of question, increase the value of page. E.g `GET http://127.0.0.1:5000/questions?page=2`and if no question is found, it returns `404` error.
>   * returned data :- On successful operation, it returns the below data.
    > ```
    {
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }
  ], 
  "current_category": [
    "Entertainment", 
    "Entertainment", 
    "History", 
    "Entertainment", 
    "History", 
    "Sports", 
    "Sports", 
    "History", 
    "Geography", 
    "Geography"
  ], 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "total_questions": 19
}
    ```
    > As shown above; 
    *    `"categories"` key contains all available category objects. Each category's object contains its respective `"id"` and `"type"` keys and values as well.
    *    `"current_category"` key contains a list of the category for _only the currently shown questions_ in the same order as that of the shown questions. It should be noted that the list of the questions is paginated to 10 questions per page.
    *    `"questions"` key contains a list of questions while each of the contained questions has the following keys and each key has its respective values.
        * `"answer"` - the value is the answer to the particular question.
        * `"category"` - the value is the type of the category, to which this question belongs.
        * `"difficulty"` - this is a difficulty level of the given question.
        * `"question"` - this is the actual question.
    *    `"total_questions"` - this contains the value for the total number of all available questions
        
        
#### To delete a question
>    * url :- `DELETE http://127.0.0.1:5000/questions/<id>`
>    * parameter / data :- `id` where the id is the identification value for the question to delete. If question with the given id is not found, it returns `404` error.
>    * returned data :- On successful operation, it returns the below. And it returns `422` error if the operation wasn't successful.
     > `"success": True`
     
     
#### To create a new question
>    * url :- `POST http://127.0.0.1:5000/questions`
>    * parameter / data :- the following data and their value **must** be sent in json-encoded form along with the request.
       * `question`
       * `answer`
       * `category`
       * `difficulty`
         * For example, `POST http://127.0.0.1:5000/questions data={"question":"What is the name of the largest planet", "answer":"Jupiter", "category":"3", "difficulty":"3"}`
           We know from the list of catergory that category type `Geography` has identification number 3
>    * returned data :- On successful operation, it returns the below while it returns `422` error if the operation fails.
     > `"success": True`
     
     
#### To search up a question
>    * url :- `POST http://127.0.0.1:5000/questions`
>    * parameter /data :- the data `searchTerm` must be sent along with the request. `SearchTerm` will contain the partial string that is contained in the question, which is to be searched up.
       * For example, `POST http://127.0.0.1:5000/questions data={"searchTerm":"planet"}`
>    * returned data :- On successful operation, it returns the below while it returns `422` error if the operation fails.
     > `"success": True`
     
     
#### To get list of questions in a specified category
>    * url :- `GET http://127.0.0.1:5000/categories/<id>/questions`
>    * parameter / data :- `id` is the identification number of the particular category whose questions are going to be returned.
       * For example, `GET http://127.0.0.1:5000/categories/3/questions` This will return only questions that belong to **Geography** category since that is the category type with identification number 3.
>    * returned data :- On successful operation, it returns the below. If no question is found with the given category id, it returns error `404`.
     > ```
{
  "current_category": [
    "Geography", 
    "Geography", 
    "Geography"
  ], 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "total_questions": 3
}
     ```
     > As shown above; 
     *    `"current_category"` key contains a list of the category for _only the currently shown questions that match up our search term_ in the same order as that of the shown questions. It should be noted that the list of the questions is paginated to 10 questions per page, if the matched up question are more than 10.
     *    `"questions"` key contains a list of questions that match up our search term while each of the contained questions has the following keys and each key has its respective values.
          * `"answer"` - the value is the answer to the particular question.
          * `"category"` - the value is the type of the category, to which this question belongs.
          * `"difficulty"` - this is a difficulty level of the given question.
          * `"question"` - this is the actual question.
     *    `"total_questions"` - this contains the value for the total number of all available questions
     

#### To play the quiz
>    * url :- `POST http://127.0.0.1:5000/quizzes`
>    * parameter / data :- the following data are expected to be sent along with the request. One is not mandatory while the second data is.
       * `"quiz_category"` - based on the given category, random questions are going to be selected. It's not mandatory as stated above. If no category is specified, questions are going to be randomly selected from any of the available categories.
       * `"previous_questions"` - this is a list of already attempted questions. This is mandatorily required.
>    * returned data :- On successful operation, it returns a randomly selected question while it returns `400` error if the operation fails.
       ```
{
      "success": True,
      "question": {
                  "answer": "Edward Scissorhands", 
                  "category": 5, 
                  "difficulty": 3, 
                  "id": 6, 
                  "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }
}
       ```
       > As shown above;
       * `"success"` key gets a True as its value because the operation is successffuly executed.
       * `"question"` key contains the actual randomly selected question with the properties of the selected question, which includes the question's `answer`, `category`, `difficulty`, `id`, and the actual `question`.
       
       
       
### API errors
The following error status codes have been formatted to return a well-formatted data so that debug can be easily be made in using any of the endpoints.
* `400` error
* `404` error
* `422` error
* `500` error


