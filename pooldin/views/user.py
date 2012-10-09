from flask import render_template, request, redirect, session, flash, url_for, abort
from flask.ext.login import login_user, logout_user, current_user

from ..app.negotiate import supports, accepts
from .base import BaseView
from ..forms import FormUserLogin

from ..database import db
from ..database.models import User


class ViewUserLogin(BaseView):
    name = 'user_login'

    @classmethod
    def add_routes(cls, app, view):
        app.add_get_rule('/login', view_func=view)
        app.add_post_rule('/login', view_func=view)

    def get(self):
        next = request.args.get('next')
        if next:
            session['next'] = next
        return render_template('user/login.html', form=FormUserLogin())

    @supports('application/json', 'application/x-www-form-urlencoded')
    def post(self):
        if request.form:
            data = request.form.to_dict()
        else:
            data = request.json

        form = FormUserLogin(**data)

        valid = form.validate()

        if not valid:
            return render_template('user/login.html', form=form)

        # Try and retrieve user by username first
        user = User.query.filter_by(username=form.login.data).first()
        if user is None:
            pass
            #email = Email.query.filter_by(address=form.login.data).first()
            #user = email.user.first() if email else None

        if not user or not user.is_password(form.password.data) or not user.enabled:
            flash('Unknown username/password combination.')
            return redirect(url_for('user_login'))

        login_user(user)
        next = session.get('next', request.args.get('next'))
        if 'next' in session:
            del session['next']
        return redirect(next or '/')


class ViewUserLogout(BaseView):
    name = 'user_logout'

    @classmethod
    def add_routes(cls, app, view):
        app.add_get_rule('/logout', view_func=view)
        app.add_post_rule('/logout', view_func=view)

    def get(self):
        logout_user()
        return redirect('/')


class ViewUserProfileAbout(BaseView):
    name = 'user_profile_about'

    @classmethod
    def add_routes(cls, app, view):
        app.add_post_rule('/user/<user_id>/about', view_func=view)

    @supports('application/json', 'application/x-www-form-urlencoded')
    @accepts('application/json')
    def post(self, user_id):
        user = User.query.filter_by(username=user_id).first()
        if request.form:
            data = request.form.to_dict()
        else:
            data = request.json

        if not user or user.id != current_user.id:
            abort(404)
        if 'about' not in data.keys():
            abort(400)

        user.about = data['about']
        db.session.commit()

        return user.to_json(fields=('username', 'about'))


class ViewUserProfile(BaseView):
    name = 'user_profile'

    @classmethod
    def add_routes(cls, app, view):
        app.add_get_rule('/user/<user_id>', view_func=view)

    @accepts('text/html', 'application/json')
    def get(self, user_id):
        is_user = False
        user = User.query.filter_by(username=user_id).first()
        if not user:
            abort(404)
        if current_user.username == user_id:
            is_user = True

        if request.best_mimetype == 'application/json':
            return user.to_json()

        return render_template('user/profile.html',
                               profile_user=user,
                               is_user=is_user)
