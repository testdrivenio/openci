# project/server/main/views.py


import redis
from rq import Queue, Connection
from flask import render_template, Blueprint, request, redirect, \
    url_for, flash, jsonify, current_app
from flask_login import login_required, current_user

from project.server import db
from project.server.models import Project
from project.server.main.tasks import create_task


main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/', methods=['GET'])
@login_required
def home():
    projects = Project.query.all()
    return render_template('main/home.html', projects=projects)


@main_blueprint.route('/projects', methods=['POST'])
@login_required
def add_project():
    user_id = current_user.id
    name = request.form['name']
    url = request.form['url']
    db.session.add(Project(user_id=user_id, name=name, url=url))
    db.session.commit()
    flash('Project added!', 'success')
    return redirect(url_for('main.home'))


@main_blueprint.route('/projects/delete/<int:project_id>', methods=['GET'])
@login_required
def remove_project(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    db.session.delete(project)
    db.session.commit()
    flash('Project removed!', 'success')
    return redirect(url_for('main.home'))


@main_blueprint.route('/projects/grade/<int:project_id>', methods=['GET'])
@login_required
def grade_project(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    with Connection(redis.from_url(current_app.config['REDIS_URL'])):
        q = Queue()
        task = q.enqueue(
            create_task,
            project.url,
            current_app.config["OPENFAAS_URL"]
        )
    response_object = {
        'status': 'success',
        'data': {
            'task_id': task.get_id()
        }
    }
    return jsonify(response_object), 202


@main_blueprint.route('/tasks/<int:project_id>/<task_id>', methods=['GET'])
def get_status(project_id, task_id):
    with Connection(redis.from_url(current_app.config['REDIS_URL'])):
        q = Queue()
        task = q.fetch_job(task_id)
    if task:
        response_object = {
            'status': 'success',
            'data': {
                'task_id': task.get_id(),
                'task_status': task.get_status(),
                'task_result': task.result
            }
        }
        if task.get_status() == 'finished':
            project = Project.query.filter_by(id=project_id).first()
            project.status = False
            if bool(task.result['status']):
                project.status = True
            db.session.commit()
    else:
        response_object = {'status': 'error'}
    return jsonify(response_object)


@main_blueprint.route('/about/')
def about():
    return render_template('main/about.html')
