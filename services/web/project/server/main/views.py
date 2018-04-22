# project/server/main/views.py


from flask import render_template, Blueprint, request, redirect, \
    url_for, flash
from flask_login import login_required, current_user

from project.server import db
from project.server.models import Project


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


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")
