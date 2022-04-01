from flask import Flask, session, request, render_template, url_for, redirect
from funk import get_user_by_username, registr_new_user, password_hashing, username_check

app = Flask(__name__)
app.secret_key = b'fhjfjgjgf'

@app.route('/')
def home():
    if session.get('user'):
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user'):
        return redirect(url_for('profile'))
    form_data = {}
    errors = {}

    if request.method == 'GET':
        return render_template('login.html', form_data=form_data, errors=errors)

    if request.method == 'POST':
        form_data = request.form
        username = form_data.get('username')
        password = password_hashing(form_data.get('password'))

        if not username:
            errors['username'] = 'Username is required.'

        if not password:
            errors['password'] = 'Password is required.'

        if len(errors) == 0:
            user = get_user_by_username(username)

            if user is None:
                errors['form_error'] = 'Invalid credentials.'

            if user is not None:
                if password != user['password']:
                    errors['form_error'] = 'Invalid credentials.'

        if len(errors):
            return render_template('login.html', errors=errors, form_data=form_data), 400

        session['user'] = {'id': user['id'], 'username': user['username']}

        return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    current_user = session.get('user')
    if not current_user:
        return redirect(url_for('login'))
    user = get_user_by_username(current_user['username'])
    return render_template('profile.html', current_user=user)


@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session.get('user'):
        return redirect(url_for('profile'))
    form_data = {}
    errors = {}

    if request.method == 'GET':
        return render_template('registration.html', form_data=form_data, errors=errors)

    if request.method == 'POST':
        form_data = request.form
        username = form_data.get('username')
        real_password = form_data.get('password')
        password = password_hashing(form_data.get('password'))
        conf_password = password_hashing(form_data.get('confpsw'))

        if not username:
            errors['username'] = 'Username is required.'

        if not username_check(username):
            errors['username'] = 'Wrong username.'

        if not password:
            errors['password'] = 'Password is required.'

        if not conf_password:
            errors['conf_password'] = 'Password confirmation is required.'

        if len(errors) == 0:
            user = get_user_by_username(username)

            if user is not None:
                errors['username'] = 'This username is taken.'

            if len(real_password) < 6:
                errors['password'] = 'Password must have at least 6 simbols.'

            if user is None:
                if password != conf_password:
                    errors['conf_password'] = 'Passwords are not same.'

        if len(errors):
            return render_template('registration.html', errors=errors, form_data=form_data), 400
        registr_new_user(username, password)
        return render_template('registered.html', current_user=username)


if __name__ == "__main__":
    app.run()