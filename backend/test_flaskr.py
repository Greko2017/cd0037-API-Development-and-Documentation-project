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
        self.user = 'postgres'
        self.password = 'postgres'
        self.host = '127.0.0.1'
        self.port = 5432
        self.database_name = 'trivia_test'
        self.database_path = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
            self.user, self.password, self.host, self.port, self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "Quel est ton nom ?", "answer": "Mon nom est Gregory Goufan", "category": 3, "difficulty": 5}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    @DONE
    Write at least one test for each test for successful operation and for expected errors.
    """
    # GET '/categories'
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])
    # Fail
    def test_405_if_categories_(self):
        res = self.client().delete("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method Not Allowed")

    # GET '/questions?page=${integer}'
    def test_get_paginated_questions(self):
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))

        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)
    # Fail
    def test_422_get_paginated_questions(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # GET '/categories/${id}/questions'
    def test_get_question_by_category_id(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
    # Fail
    def test_404_if_question_does_not_exist(self):
        res = self.client().get("/categories/30/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    # POST '/questions'
    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # POST '/questions'
    def test_search_question_byu_search_term(self):
        res = self.client().post("/questions", json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
    # Fail
    def test_422_search_question_by_search_term(self):
        res = self.client().get("/questions?page=200", json={"searchTerm": None})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


    # DELETE '/questions/${id}'
    def test_delete_question(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['id'])
    # Fail delete
    def test_404_delete_question(self):
        res = self.client().delete('/questions/300')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # POST '/quizzes'
    def test_get_random_question(self):
        res = self.client().post("/quizzes", json={'previous_questions': [],
            'quiz_category': {'type': "Science", 'id': "1"}
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
    # Fail
    def test_500_random_question(self):
        res = self.client().post("/quizzes", json={'previous_questions': [],
            'quiz_category': "Art"
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Server Side Error")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()