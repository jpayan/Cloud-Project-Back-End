import os
import sys
from chalice import Chalice, ChaliceViewError

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, 'chalicelib/'))

from project.mapper.test_mapper import *
from project.mapper.student_mapper import *
from project.mapper.teacher_mapper import *
from project.mapper.group_mapper import *
from project.mapper.applied_test_mapper import *
from project.NLP.answer_analyzer import *

app = Chalice(app_name='cc414-nb-service')
app.debug = True


@app.route('/tests', methods=['POST'], content_types=['application/x-www-form-urlencoded', 'application/json'],
           cors=True)
def ep_create_test():
    try:
        payload = app.current_request.json_body
        response = create_test(payload)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/tests/teacher/{teacher_id}', methods=['GET'],
           content_types=['application/x-www-form-urlencoded', 'application/json'], cors=True)
def ep_get_tests_by_teacher(teacher_id):
    try:
        response = get_tests_by_teacher(teacher_id)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/tests', methods=['GET'], content_types=['application/x-www-form-urlencoded', 'application/json'],
           cors=True)
def ep_get_test():
    try:
        test_id = app.current_request.query_params.get('test_id')
        teacher_id = app.current_request.query_params.get('teacher_id')
        response = get_test(test_id, teacher_id)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/tests/code/{code}', methods=['GET'],
           content_types=['application/x-www-form-urlencoded', 'application/json'], cors=True)
def ep_get_test_by_code(code):
    try:
        response = get_test_by_code(code)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/tests', methods=['PUT'], content_types=['application/x-www-form-urlencoded', 'application/json'],
           cors=True)
def ep_update_test():
    try:
        test_id = app.current_request.query_params.get('test_id')
        teacher_id = app.current_request.query_params.get('teacher_id')
        payload = app.current_request.json_body
        response = update_test(test_id, teacher_id, payload)
        return response['Attributes']
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/tests', methods=['DELETE'],
           content_types=['application/x-www-form-urlencoded', 'application/json'], cors=True)
def ep_delete_test():
    try:
        test_id = app.current_request.query_params.get('test_id')
        teacher_id = app.current_request.query_params.get('teacher_id')
        response = delete_test(test_id, teacher_id)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/students', methods=['POST'], content_types=['application/x-www-form-urlencoded', 'application/json'],
           cors=True)
def ep_create_student():
    try:
        payload = app.current_request.json_body
        response = create_student(payload)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/students/group', methods=['GET'],
           content_types=['application/x-www-form-urlencoded', 'application/json'], cors=True)
def ep_get_students_by_group():
    try:
        group_name = app.current_request.query_params.get('group_name')
        teacher_id = app.current_request.query_params.get('teacher_id')
        response = get_students_by_group(group_name, teacher_id)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/students', methods=['PUT'],
           content_types=['application/x-www-form-urlencoded', 'application/json'], cors=True)
def ep_update_student():
    try:
        payload = app.current_request.json_body
        response = update_student(payload)
        return response['Attributes']
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/students', methods=['DELETE'],
           content_types=['application/x-www-form-urlencoded', 'application/json'], cors=True)
def ep_delete_student():
    try:
        payload = app.current_request.json_body
        response = delete_student(payload)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/teachers', methods=['POST'], content_types=['application/x-www-form-urlencoded', 'application/json'],
           cors=True)
def ep_create_teacher():
    try:
        payload = app.current_request.json_body
        response = create_teacher(payload)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/teachers/{teacher_id}', methods=['GET'],
           content_types=['application/x-www-form-urlencoded', 'application/json'], cors=True)
def ep_get_teacher(teacher_id):
    try:
        response = get_teacher(teacher_id)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/groups', methods=['POST'], content_types=['application/x-www-form-urlencoded', 'application/json'],
           cors=True)
def ep_create_group():
    try:
        payload = app.current_request.json_body
        response = create_group(payload)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/groups/{teacher_id}', methods=['GET'],
           content_types=['application/x-www-form-urlencoded', 'application/json'], cors=True)
def ep_get_groups_by_teacher_id(teacher_id):
    try:
        response = get_groups_by_teacher_id(teacher_id)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/groups', methods=['PUT'], content_types=['application/x-www-form-urlencoded', 'application/json'],
           cors=True)
def ep_update_group():
    try:
        payload = app.current_request.json_body
        response = update_group(payload)
        return response['Attributes']
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/groups', methods=['DELETE'], content_types=['application/x-www-form-urlencoded', 'application/json'],
           cors=True)
def ep_delete_group():
    try:
        payload = app.current_request.json_body
        response = delete_group(payload)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/applied_tests', methods=['POST'], content_types=['application/x-www-form-urlencoded', 'application/json'],
           cors=True)
def ep_create_applied_tests():
    try:
        payload = app.current_request.json_body
        response = create_applied_tests(payload)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/applied_tests/group', methods=['POST'], content_types=['application/x-www-form-urlencoded',
                                                                    'application/json'],
           cors=True)
def ep_create_applied_tests_by_group():
    try:
        payload = app.current_request.json_body
        response = create_applied_tests_by_group(payload)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/applied_tests/test/{test_id}', methods=['GET'],
           content_types=['application/x-www-form-urlencoded', 'application/json'], cors=True)
def ep_get_applied_tests_by_test(test_id):
    try:
        response = get_applied_tests_by_test(test_id)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/applied_tests', methods=['PUT'],
           content_types=['application/x-www-form-urlencoded', 'application/json'], cors=True)
def ep_update_applied_test():
    try:
        payload = app.current_request.json_body
        response = update_applied_test(payload)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/applied_tests', methods=['DELETE'],
           content_types=['application/x-www-form-urlencoded', 'application/json'], cors=True)
def ep_delete_applied_test():
    try:
        payload = app.current_request.json_body
        response = delete_applied_test(payload)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


# ******************************************************** NLP ******************************************************* #

@app.route('/nlp/feedback', methods=['POST'], content_types=['application/x-www-form-urlencoded', 'application/json'],
           cors=True)
def ep_get_answer_feedback():
    try:
        payload = app.current_request.json_body
        response = get_answer_feedback(payload['concept'], payload['answer'])
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/nlp/grade', methods=['POST'], content_types=['application/x-www-form-urlencoded', 'application/json'],
           cors=True)
def ep_grade_answer():
    try:
        payload = app.current_request.json_body
        response = grade_answer(payload['concept'], payload['answer'])
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)
