from ast import JoinedStr
from crypt import methods
import os
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
    start_page = (page - 1) * QUESTIONS_PER_PAGE
    end_page = start_page + QUESTIONS_PER_PAGE

    current_dataset = [data.format() for data in dataset]
    return current_dataset[start_page:end_page]


def paginate_current_category(request, questions):
    page = request.args.get('page', 1, type=int)
    start_page = (page - 1) * QUESTIONS_PER_PAGE
    end_page = start_page + QUESTIONS_PER_PAGE
    categories = [question.category for question in questions]
    # category_names = {}
    category_names = []
    for category in categories:
        current_category = Category.query.get(category)
        # category_names[str(current_category.id)] = current_category.type
        category_names.append(current_category.type)
    return category_names[start_page:end_page]


def paginate_category(request, categories):
    page = request.args.get('page', 1, type=int)
    start_page = (page - 1) * QUESTIONS_PER_PAGE
    end_page = start_page + QUESTIONS_PER_PAGE
    formatted_categories = [category.format() for category in categories]
    return formatted_categories[start_page:end_page]


def paginate_category_only(categories):
    formatted_categories = [category.format() for category in categories]
    processed_categories = {}
    for category in formatted_categories:
        processed_categories[str(category['id'])] = category['type']
    return processed_categories


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.\
            add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.\
            add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response

    @app.route('/categories')
    def get_categories():
        selections = Category.query.order_by(Category.id).all()
        formatted_selections = paginate_category_only(selections)
        if len(formatted_selections) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'categories': formatted_selections
            })

    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.category).all()
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = paginate_category_only(categories)
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

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            selected_question = Question.query.\
                                filter(Question.id == question_id)\
                                .one_or_none()
            if selected_question is None:
                abort(404)
            deleted = selected_question.id
            selected_question.delete()
            return jsonify({
                'success': True,
                'deleted_question_id': deleted
            })
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_question():
        data = request.get_json()
        search_term = data.get('searchTerm', None)
        try:
            if search_term is not None:
                matched_result = \
                    Question.query.\
                    filter(Question.question.ilike('%'+search_term+'%'))\
                    .all()
                if len(matched_result) == 0:
                    abort(404)
                elif len(matched_result) > 0:
                    matched_result_formatted = \
                        paginate_questions(request, matched_result)
                    matched_result_category = \
                        paginate_current_category(request, matched_result)
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

    @app.route('/categories/<int:category_id>/questions')
    def get_category_based_questions(category_id):
        cat_seltd_questions = \
            Question.query.\
            filter(Question.category == category_id).\
            all()
        if len(cat_seltd_questions) == 0:
            abort(404)
        else:
            formatted_cat_seltd_questions = \
                paginate_questions(request, cat_seltd_questions)
            current_category = \
                paginate_current_category(request, cat_seltd_questions)
            return jsonify({
                'questions': formatted_cat_seltd_questions,
                'total_questions': len(cat_seltd_questions),
                'current_category': current_category,
                'success': True
            })

    @app.route('/quizzes', methods=['POST'])
    def play_quizzes():
        data = request.get_json()
        previous_questions = data.get('previous_questions', [])
        quiz_category = data.get('quiz_category', None)
        unseen_questions = []
        category_based_questions = None
        formatted_all_category_based_questions = None
        try:
            if quiz_category is not None and quiz_category['id'] != 0:
                category_based_questions = Question.query.\
                    filter(Question.category == quiz_category['id']).\
                    all()
                formatted_all_category_based_questions = \
                    [question.format() for question in
                        category_based_questions]
                for question in formatted_all_category_based_questions:
                    if question['id'] not in previous_questions:
                        unseen_questions.append(question)
            else:
                all_questions = Question.query.all()
                formatted_all_questions = \
                    [question.format() for question in all_questions]
                for question in formatted_all_questions:
                    if question['id'] not in previous_questions:
                        unseen_questions.append(question)
            '''
                If there are still no more unattempted questions in the list,
                then, return the below to signify end of game.
            '''
            if len(unseen_questions) < 1:
                return jsonify({
                    'success': True,
                    'question': None,
                    'previous_question': previous_questions
                })
            '''
                Randomly select a question from the unseen_questions,
                only if there are still unattempted questions in
                the list.
            '''
            new_random_question = random.choice(unseen_questions)
            return jsonify({
                'success': True,
                'question': new_random_question,
                'previous_question': previous_questions
            })
        except:
            abort(400)

    @app.errorhandler(404)
    def not_found(error):

        return (jsonify({
                'success': False,
                'error': 404,
                'message': 'the requested resource not found.'
                }),
                404
                )

    @app.errorhandler(422)
    def unprocessable(error):

        return (jsonify({
                'success': False,
                'error': 422,
                'message': 'operation can not be processed'
                }),
                422
                )

    @app.errorhandler(400)
    def bad_syntax(error):

        return (jsonify({
                'success': False,
                'error': 400,
                'message': 'bad request / bad syntax'
                }),
                400
                )

    @app.errorhandler(500)
    def internal_server_error(error):

        return (jsonify({
                'success': False,
                'error': 500,
                'message': 'Internal server error.'
                }),
                500
                )

    return app
