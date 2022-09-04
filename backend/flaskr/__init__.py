import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)    

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        formatted_categories = {}
        for index, category in enumerate(categories):
            formatted_categories[str(category.id)] = category.type
        
        return jsonify({
            'categories':formatted_categories,
            })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    @app.route('/questions', methods=['GET'])
    #@cross_origin
    def get_questions():
        # Implement pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        formatted_question = [question.format() for question in questions]
        # Categories
        categories = Category.query.all()
        formatted_categories = {}
        for index, category in enumerate(categories):
            formatted_categories[str(index+1)] = category.type
        
        if len(formatted_question[start:end]) == 0:
            abort(422)
            
        return jsonify({
            'questions':formatted_question[start:end],
            'total_questions':len(questions),
            'categories':formatted_categories,
            'current_category': None
            })
            
    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_quesiton(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)        
        else:
            question.delete()
            return jsonify({
                'id': question_id
            })


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        
        questions = Question.query.all()

        # Search logic        
        searchTerm = body.get('searchTerm', None)
        if searchTerm is not None:
            filter_questions = Question.query.filter(Question.question.ilike("%{}%".format(searchTerm))).all()
            formatted_question = [question.format() for question in filter_questions]
            
            return jsonify({
                "questions": formatted_question[start:end],
                "total_questions": len(questions),
                "current_category": None
                })

        else:
            try:
                question = Question(question=question,answer=answer,category=category,difficulty=difficulty)
                question.insert()
                
                questions = Question.query.all()
                formatted_question = [question.format() for question in questions]
                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions':formatted_question[start:end],
                    'total_questions': len(questions),
                    'current_category': question.category
                })
            except:
                abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    # I added the logic in add_question controller

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category_id(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()
        if category is None:
            abort(404)
        
        questions = Question.query.filter(Question.category == category.id).all()
        formatted_question = [question.format() for question in questions]

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        return jsonify({
            "questions": formatted_question[start:end],
            "total_questions": len(questions),
            "current_category": category.type
            })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)
 
        if (previous_questions is None) or (quiz_category is None):
            abort(404)
        try:   
            if quiz_category['id'] == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
                # print('b questions',questions)
            else:
                questions = Question.query.filter(Question.category == quiz_category['id']).filter(Question.id.notin_(previous_questions)).all()
            # choose random number amont index of array        
            nrb_questions = 2
            if len(questions) != 0:
                nrb_questions = len(questions)
            question = questions[random.randint(0, (nrb_questions-1) )]
                
            return jsonify({
                "question": question.format()
                })
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def  not_found(error):
        return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404
        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    return app

