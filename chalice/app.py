import os
import sys
from chalice import Chalice, IAMAuthorizer, BadRequestError, ChaliceViewError

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, 'chalicelib/'))

from project.mapper.test_mapper import get_tests, get_test, create_test, update_test, delete_test
from project.mapper.teacher_mapper import get_teachers, get_teacher, create_teacher, update_teacher, delete_teacher
from project.mapper.student_mapper import get_students, get_student, create_student, update_student, delete_student
from project.mapper.applied_test_mapper import get_ap_tests, get_ap_test, create_ap_test, update_ap_test, delete_ap_test

authorizer = IAMAuthorizer()
app = Chalice(app_name='project-test')
app.debug = True

@app.route('/tests', methods=['GET'], authorizer=authorizer, content_types=['application/x-www-form-urlencoded'])
def ep_get_all_tests():
    try:
        pass
    except Exception as e:
        raise ChaliceViewError(e.message)

@app.route('/tests', methods=['POST'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_create_test():
    try:
        data = app.current_request.json_body
        item = create_test(data['name'], data['subject'])
        return item
    except Exception as e:
        raise ChaliceViewError(e.message)

@app.route('/tests/{id}', methods=['GET'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded'])
def ep_get_test(id):
    try:
        get_test(id)
    except Exception as e:
        raise ChaliceViewError(e.message)

@app.route('/tests/{id}', methods=['PUT'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_update_test(id):
    try:
        data = app.current_request.json_body
        update_test(id, data["test"])
    except Exception as e:
        raise ChaliceViewError(e.message)

@app.route('/tests/{id}', methods=['DELETE'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded'])
def ep_delete_test(id):
    try:
        delete_test(id)
    except Exception as e:
        raise ChaliceViewError(e.message)

@app.route('/teachers', methods=['GET'], authorizer=authorizer, content_types=['application/x-www-form-urlencoded'])
def ep_get_all_tests():
    try:
        pass
    except Exception as e:
        raise ChaliceViewError(e.message)

@app.route('/teachers', methods=['POST'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_create_test():
    try:
        data = app.current_request.json_body
        item = create_test(data['name'], data['subject'])
        return item
    except Exception as e:
        raise ChaliceViewError(e.message)

@app.route('/tests/{id}', methods=['GET'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded'])
def ep_get_test(id):
    try:
        get_test(id)
    except Exception as e:
        raise ChaliceViewError(e.message)

@app.route('/tests/{id}', methods=['PUT'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_update_test(id):
    try:
        data = app.current_request.json_body
        update_test(id, data["test"])
    except Exception as e:
        raise ChaliceViewError(e.message)

@app.route('/tests/{id}', methods=['DELETE'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded'])
def ep_delete_test(id):
    try:
        delete_test(id)
    except Exception as e:
        raise ChaliceViewError(e.message)
