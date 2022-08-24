from ast import JoinedStr
from crypt import methods
import os
from tkinter.tix import Tree
from tokenize import endpats
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, dataset):
    page = request.args.get('page', 1, type=int)
    start_page = (page -1) * QUESTIONS_PER_PAGE
    end_page = start_page + QUESTIONS_PER_PAGE

    current_dataset = [data.format() for data in dataset]
    return current_dataset[start_page:end_page]

def paginate_current_category(request, questions):
    page = request.args.get('page', 1, type=int)
    start_page = (page -1) * QUESTIONS_PER_PAGE
    end_page = start_page + QUESTIONS_PER_PAGE

    categories = [question.category for question in questions]

    category_names = []
        
    for category in categories:
        category_names.append(Category.query.get(category).type)

    return category_names[start_page:end_page]

def paginate_category(request, categories):
    page = request.args.get('page', 1, type=int)
    start_page = (page - 1) * QUESTIONS_PER_PAGE
    end_page = start_page + QUESTIONS_PER_PAGE
    formatted_categories = [category.format() for category in categories]

    return formatted_categories[start_page:end_page]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods','GET,POST,DELETE')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        selections = Category.query.order_by(Category.id).all()
        formatted_selections = paginate_category(request, selections)
        if len(formatted_selections) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'categories': formatted_selections
            })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = [category.format() for category in categories]
        current_categories = paginate_current_category(request, questions)
        all_current_questions = paginate_questions(request, questions)
        if len(all_current_questions) == 0:
            abort(404)
        else:
            return jsonify({
                'questions': all_current_questions,
                'total_questions': len(questions),
                'categories': formatted_categories,
                'current_category': current_categories,
                'success': True
            })


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            selected_question = Question.query.filter(Question.id == question_id).one_or_none()
            
            if selected_question is None:
                abort(404)
            
            selected_question.delete()
            return jsonify({
                'success': True
            })
        except:
            abort(422)



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
        data = request.get_json()
        search_term = data.get('searchTerm', None)
        try:
            if search_term:
                matched_result = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
                if matched_result is None:
                    abort(404)
                else:
                    matched_result_formatted = paginate_questions(request, matched_result)
                    matched_result_category = paginate_current_category(request, matched_result)
                    return jsonify({
                        'success': True,
                        'questions': matched_result_formatted,
                        'total_questions': len(matched_result),
                        'current_category': matched_result_category
                    })
            else:
                question = data['question']
                answer = data['answer']
                category = data['category']
                difficulty = data['difficulty']
                new_question = Question(question, answer, category, difficulty)
                new_question.insert()

                return jsonify({
                    'success': True
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
    # This has been implemented in add_question function above

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions')
    def get_category_based_questions(category_id):
        cat_seltd_questions = Question.query.filter(Question.category == category_id).all()
        if cat_seltd_questions is None:
            abort(404)
        else:
            formatted_cat_seltd_questions = paginate_questions(request, cat_seltd_questions)
            current_category = paginate_current_category(request, cat_seltd_questions)

            return jsonify({
                'questions': formatted_cat_seltd_questions,
                'total_questions': len(cat_seltd_questions),
                'current_category': current_category,
                'success': True
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
    def play_quizzes():
        data = request.get_json()
        previous_questions = data.get('previous_questions', [])
        quiz_category = data.get('quiz_category', None)
        unseen_questions = []
        try:
            if quiz_category:
                category = Category.query.filter(Category.type == quiz_category)
                all_category_based_questions = Question.query.filter(Question.category == category.id).all()
                for question in all_category_based_questions:
                    if question['question'] not in previous_questions:
                        unseen_questions.append(question)
            else:
                all_questions = Question.query.all()
                for question in all_questions:
                    if question['question'] not in previous_questions:
                        unseen_questions.append(question)
            
            formatted_unseen_questions = paginate_questions(request, unseen_questions)

            # Randomly select a question in the formatted_unseen_questions
            new_random_question = random.choice(formatted_unseen_questions)

            return jsonify({
                'success': True,
                'question': new_random_question
            })
        except:
            abort(500)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return(
            jsonify({
                'success': False,
                'error': 404,
                'message': 'the requested resource not found.'
            }),
            404
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return(
            jsonify({
                'success': False,
                'error': 422,
                'message': 'operation can not be processed'
            }),
            422
        )

    @app.errorhandler(400)
    def bad_syntax(error):
        return(
            jsonify({
                'success': False,
                'error': 400,
                'message': 'bad request / bad syntax'
            }),
            400
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return(
            jsonify({
                'success': False,
                'error': 500,
                'message': 'Internal server error.'
            }),
            500
        )


    return app

