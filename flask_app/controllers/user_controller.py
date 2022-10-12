from pprint import pprint
from flask_app import app, render_template, redirect, request, session, flash, bcrypt
from flask_app.models.user_model import User


# redirect user to login/reg
@app.get('/')
def redirect_user():
    return redirect ('users/login_reg')

@app.get('/users/login_reg')
def login_reg():
    return render_template('login_reg.html')

@app.post ('/users/register')
def register_user():
    #check if form is valid
    if not User.validate_registration(request.form):
        return redirect('/users/login_reg')

    #if form is valid, check to see if they are registered
    found_user = User.find_by_email(request.form)
    if found_user:
        flash ('Email already in database, Please login.', 'email')
        return redirect ('/users/login_reg')

    #hash password(encrypt with bycrypt)
    hashed = bcrypt.generate_password_hash(request.form['password'])
    # print(hashed)
    data= {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':hashed
    }
    #register(save) the user
    user_id= User.save(data)

    #log the user in and save user's id in session
    session['user_id']= user_id
    return redirect('/recipes')

@app.post('/users/login')
def login_users():
    #check if the form is valid
    if not User.validate_login(request.form):
        return redirect('/users/login_reg')

    #if the form is valid, check to see if they are registered
    found_user = User.find_by_email(request.form)
    if not found_user:
        flash('Email not found, please register.','log_email')
        return redirect('/users/login_reg')

    #if they did register, 
    # check if the password is correct
    if not bcrypt.check_password_hash(found_user.password, request.form['password']):
        flash('Invalid credentials. Please check your password.','log_password')
        return redirect('/users/login_reg')

    #if they password is correct, log them in
    session['user_id']=found_user.id
    return redirect('/recipes')



@app.get('/users/logout')
def logout():
        session.clear()
        return redirect('/users/login_reg')

