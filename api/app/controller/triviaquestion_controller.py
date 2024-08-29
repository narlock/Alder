from flask import Blueprint, request, jsonify
from app.model.triviaquestion_model import TriviaQuestion
from app.schema.triviaquestion_schema import TriviaQuestionSchema
from app import db
from sqlalchemy.sql.expression import func

# Define triviaquestion Blueprint
triviaquestion_bp = Blueprint('triviaquestion_bp', __name__)

# Initialize trivia question schema
triviaquestion_schema = TriviaQuestionSchema()

@triviaquestion_bp.route('/trivia', methods=['GET'])
def get_random_trivia_question():
    """
    Gets a random trivia question from the database.
    """
    # Query the database for a random trivia question
    triviaquestion = TriviaQuestion.query.order_by(func.rand()).first()

    if triviaquestion is None:
        # Return a 404 error if no trivia question is found
        return jsonify({'message': 'No trivia questions found'}), 404
    
    # If found, serialize the triviaquestion object to JSON using the schema
    return jsonify(triviaquestion_schema.dump(triviaquestion))

@triviaquestion_bp.route('/trivia/<int:id>', methods=['GET'])
def get_trivia_question(id):
    """
    Gets the trivia question matching the id in the path.
    """

    # Query the trivia question model to find the trivia question by the given ID
    triviaquestion = TriviaQuestion.query.get(id)
    if triviaquestion is None:
        # Return a 404 error if the trivia question is not found
        return jsonify({'message': 'Trivia question not found'}), 404
    
    # If found, serialize the triviaquestion object to JSON using the schema
    return jsonify(triviaquestion_schema.dump(triviaquestion))

@triviaquestion_bp.route('/trivia', methods=['POST'])
def create_trivia_question():
    """
    Given a request body of a full trivia question, insert
    the trivia question into the database.
    """
    # Load the request JSON data into a TriviaQuestionSchema object
    data = request.get_json()
    errors = triviaquestion_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # Create a new TriviaQuestion object from the validated data
    new_trivia_question = TriviaQuestion(
        title=data['title'],
        option_a=data['option_a'],
        option_b=data['option_b'],
        option_c=data['option_c'],
        option_d=data['option_d'],
        correct=data['correct'],
        author=data['author'],
        category=data['category']
    )

    # Add the new trivia question to the session and commit to the database
    db.session.add(new_trivia_question)
    db.session.commit()

    # Return the created trivia question as a response
    return jsonify(triviaquestion_schema.dump(new_trivia_question)), 201


@triviaquestion_bp.route('/trivia/<int:id>', methods=['PUT'])
def overwrite_trivia_question(id):
    """
    Given a request body of a full trivia question, overwrite
    the existing trivia question with the id in the path with
    the request body trivia question into the database.
    """
    # Query the trivia question model to find the trivia question by the given ID
    triviaquestion = TriviaQuestion.query.get(id)
    if triviaquestion is None:
        return jsonify({'message': 'Trivia question not found'}), 404
    
    # Load the request JSON data into a TriviaQuestionSchema object
    data = request.get_json()
    errors = triviaquestion_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # Update the trivia question with the new data
    triviaquestion.title = data['title']
    triviaquestion.option_a = data['option_a']
    triviaquestion.option_b = data['option_b']
    triviaquestion.option_c = data['option_c']
    triviaquestion.option_d = data['option_d']
    triviaquestion.correct = data['correct']
    triviaquestion.author = data['author']
    triviaquestion.category = data['category']

    # Commit the changes to the database
    db.session.commit()

    # Return the updated trivia question as a response
    return jsonify(triviaquestion_schema.dump(triviaquestion)), 200


@triviaquestion_bp.route('/trivia/<int:id>', methods=['DELETE'])
def delete_trivia_question(id):
    """
    Delete the trivia question matching the id in the path.
    """
    # Query the trivia question model to find the trivia question by the given ID
    triviaquestion = TriviaQuestion.query.get(id)
    if triviaquestion is None:
        return jsonify({'message': 'Trivia question not found'}), 404
    
    # Delete the trivia question from the session and commit to the database
    db.session.delete(triviaquestion)
    db.session.commit()

    # Return 204 No Content
    return '', 204
