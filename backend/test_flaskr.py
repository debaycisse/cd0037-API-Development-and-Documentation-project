import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOSTNAME = os.getenv('DB_HOSTNAME', '127.0.0.1:5432')
        self.DB_USERNAME = os.getenv('DB_USERNAME', 'student')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'student')
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')
        self.DB_PATH = 'postgresql://{}:{}@{}/{}'.\
            format(self.DB_USERNAME, self.DB_PASSWORD, 
                self.DB_HOSTNAME, self.DB_NAME)
        setup_db(self.app, self.DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = \
            {"question": "What is the name of the smallest planet", 
            "answer": "Mercury", 
            "category": 3, 
            "difficulty": 3}

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_404_retrieving_wrongly_spelt_category(self):
        res = self.client().get('/categories/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "the requested resource not found.")

    def test_404_retrieving_unavailable_category(self):
        res = self.client().get('/categories?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the requested resource not found.")



    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_retrieving_beyond_available_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the requested resource not found.")

    
    def test_delete_question(self):
        res = self.client().delete('/questions/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_question_id'])

    def test_422_deletion_an_unavailable_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "operation can not be processed")


    def test_adding_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_adding_new_question_with_wrong_syntax_or_missing_data(self):
        res = self.client().post('/questions', json={"question":["what is the name of the smallest planet"], "answer": "Mercury"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "operation can not be processed")

    
    def test_searching_for_a_question(self):
        res = self.client().post('/questions', json={"searchTerm":"title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_searching_with_empty_result_or_422(self):
        res = self.client().post('/questions', json={"searchTerm":"RaupeRaupe"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "operation can not be processed")


    def test_retrieve_list_of_questions_based_on_given_category(self):
        res = self.client().get('categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_requesting_for_questions_in_an_inexisting_category(self):
        res = self.client().get('categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the requested resource not found.")

    def test_playing_quiz(self):
        res = self.client().post('/quizzes', json={"previous_questions":[]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_400_sending_bad_request_playing_quiz(self):
        res = self.client().post('/quizzes',json={"previous_questions":"what is your name"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request / bad syntax")










# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()