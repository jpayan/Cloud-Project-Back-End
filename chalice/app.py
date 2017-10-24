import os
import sys
from chalice import Chalice, IAMAuthorizer, ChaliceViewError

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, 'chalicelib/'))

from project.mapper.test_mapper import *
from project.mapper.student_mapper import *
from project.mapper.teacher_mapper import *
from project.mapper.group_mapper import *

authorizer = IAMAuthorizer()
app = Chalice(app_name='cc414-nb-service')
app.debug = True


@app.route('/tests', methods=['GET'], authorizer=authorizer, content_types=['application/x-www-form-urlencoded'])
def ep_get_tests():
    try:
        items = get_tests()
        return items
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/tests', methods=['POST'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_create_test():
    try:
        data = app.current_request.json_body
        item = create_test(data['title'], data['subject'], data['questions'])
        return item
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/tests/{test_id}', methods=['GET'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded'])
def ep_get_test(test_id):
    try:
        item = get_test(test_id)
        return item
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/tests/{test_id}', methods=['PUT'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_update_test(test_id):
    try:
        data = app.current_request.json_body
        response = update_test(test_id, data['expression'], data['attributes'])
        return response['Attributes']
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/tests/{test_id}', methods=['DELETE'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded'])
def ep_delete_test(test_id):
    try:
        response = delete_test(test_id)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/students', methods=['GET'], authorizer=authorizer, content_types=['application/x-www-form-urlencoded'])
def ep_get_students():
    try:
        items = get_students()
        return items
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/students', methods=['POST'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_create_student():
    try:
        data = app.current_request.json_body
        item = create_student(data['email'], data['full_name'])
        return item
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/students/{student_id}', methods=['GET'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded'])
def ep_get_student(student_id):
    try:
        item = get_student(student_id)
        return item
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/students/{student_id}', methods=['PUT'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_update_student(student_id):
    try:
        data = app.current_request.json_body
        response = update_student(student_id, data['expression'], data['attributes'])
        return response['Attributes']
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/students/{student_id}', methods=['DELETE'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded'])
def ep_delete_student(student_id):
    try:
        response = delete_student(student_id)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/teachers', methods=['GET'], authorizer=authorizer, content_types=['application/x-www-form-urlencoded'])
def ep_get_teachers():
    try:
        items = get_teachers()
        return items
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/teachers', methods=['POST'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_create_teacher():
    try:
        data = app.current_request.json_body
        item = create_teacher(
            data['email'], data['full_name'], data['prefix'], data['password'], data['groups'], data['tests'])
        return item
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/teachers/{teacher_id}', methods=['GET'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded'])
def ep_get_teacher(teacher_id):
    try:
        item = get_teacher(teacher_id)
        return item
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/teachers/{teacher_id}', methods=['PUT'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_update_teacher(teacher_id):
    try:
        data = app.current_request.json_body
        response = update_teacher(teacher_id, data['expression'], data['attributes'])
        return response['Attributes']
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/teachers/{teacher_id}', methods=['DELETE'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded'])
def ep_delete_teacher(teacher_id):
    try:
        response = delete_teacher(teacher_id)
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)

@app.route('/groups/{teacher_id}', methods=['GET'], authorizer=authorizer, content_types=['application/x-www-form-urlencoded'])
def ep_get_groups(teacher_id):
    try:
        items = get_groups(teacher_id)
        return items
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/groups', methods=['POST'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_create_group():
    try:
        data = app.current_request.json_body
        item = create_group(
            data['name'], data['teacher_id'], data['students'])
        return item
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/groups', methods=['GET'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_get_group():
    try:
        data = app.current_request.json_body
        item = get_group(
            data['name'], data['teacher_id']
        )
        return item
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/groups', methods=['PUT'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_update_group():
    try:
        data = app.current_request.json_body
        response = update_group(name, teacher_id, data['expression'], data['attributes'])
        return response['Attributes']
    except Exception as e:
        raise ChaliceViewError(e.message)


@app.route('/groups', methods=['DELETE'], authorizer=authorizer,
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def ep_delete_group():
    try:
        data = app.current_request.json_body
        response = delete_group(
            data['name'], data['teacher_id']
        )
        return response
    except Exception as e:
        raise ChaliceViewError(e.message)