from flask import request, render_template, url_for, make_response, redirect
from flask import session as s
from app.models import User
from app.db import session
from app.app import oauth
from uuid import uuid4


def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    username = request.form.get('username')
    password = request.form.get('password')

    user = session.query(User).filter_by(username=username).first()

    if user:
        return 'USER ALREADY EXIST'

    user = User(username=username, password=password)

    session.add(user)
    session.commit()

    response = make_response(redirect('/'))
    response.set_cookie('user_id', str(user.id), httponly=True)

    return response


def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = session.query(User).filter_by(username=username).first()
        if not user:
            return 'USER DON\'T EXISTS'

        if user.password != password:
            if user.sub != 0:
                return 'LOG IN THIS PROFILE USING GOOGLE AUTH'
            return 'WRONG PASSWORD'

        response = make_response(redirect(url_for('index')))
        response.set_cookie('user_id', str(user.id), httponly=True)

        return response

    return render_template('auth/login.html')


def google_oauth():
    redirect_uri = url_for('auth.google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


def google_auth():
    token = oauth.google.authorize_access_token()
    user_info = token['userinfo']

    user = session.query(User).filter_by(sub=user_info['sub']).first()

    if not user:
        s['user_info'] = user_info

        #  Creating a user now cuz I want simply add random username after oauth
        username = 'user_' + str(uuid4())[:8]
        user = User(
            sub=user_info['sub'],
            username=username,
            email=user_info['email'],
            name=user_info['name'],
            picture=user_info['picture']
        )
        session.add(user)
        session.commit()

        response = make_response(redirect(url_for('auth.username')))
        response.set_cookie('user_id', str(user.id), httponly=True)

        return response

    response = make_response(redirect('/'))
    response.set_cookie('user_id', str(user.id), httponly=True)

    return response


def add_username():
    if 'user_info' not in s.keys():
        return redirect('/')

    if request.method == 'POST':
        username = request.form.get('username')
        user_info = s.get('user_info')

        user = session.query(User).filter_by(sub=user_info['sub']).first()

        user.username = username
        session.commit()

        s.pop('user_info')

        return redirect('/')

    return render_template('auth/username.html')


def logout():
    response = make_response(redirect('/'))
    response.set_cookie('user_id', '', expires=0)
    return response
