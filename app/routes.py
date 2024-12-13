from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from urllib.parse import urlparse as url_parse
from app.forms import LoginForm, RegistrationForm, QuestionForm
from app.models import User, Question, Score
from sqlalchemy import func




"""login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
"""
"""
@login_manager.user_loader
def load_user(user_id):
    user= User.query.get(user_id)
    print(F"USER LOADED:{user}")
    return user
"""

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        g.user = user

@app.route('/')
def index():
    return render_template('home.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #filtering the user with email
        user = User.query.filter_by(email=form.email.data).first()
        
        #checking if the user entered password and password in the database are same or not
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))

        # logging the user in and storing the user_id in the session
        login_user(user) 
        session['user_id'] = user.id  
        session['score'] = 0  

        # Redirect to the next page or to the quiz page
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '': 
            next_page = url_for('quiz') 
        return redirect(next_page)

    if 'user_id' in session:
        return redirect(url_for('quiz'))  # redirecting to quiz app if the user_id is already logged in and they haven't logged out

    return render_template('login.html', form=form, title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['score'] = 0
        return redirect(url_for('login'))
    if g.user:
        return redirect(url_for('quiz'))
    return render_template('register.html', title='Register', form=form)


@app.route('/quiz')
def quiz():
     return render_template('quiz.html')

@app.route('/profile')
def profile():
    user = current_user 
    scores = user.scores
    print(scores)  
    return render_template('profile.html', user=user, scores=scores)


@app.route('/quiz/<category>', methods=["GET", "POST"])
def quiz_category(category):
    questions = Question.query.filter(func.lower(Question.category) == func.lower(category)).all()#retrieving questions by filtering through categories
    if not questions:
        return "No questions available in this category.", 404

    if 'question_index' not in session:
        session['question_index'] = 0
    if 'scores' not in session:
        session['scores'] = 0

    current_index = session['question_index']
    current_question = questions[current_index]#extracting questions from it's index

    if request.method == "POST":
        #handling question_answer submission
        user_answer = request.form.get(f'question{current_question.id}')
        if user_answer and user_answer.lower() == current_question.answer.lower():
            session['scores'] += 1
        # moving to another question
        session['question_index'] += 1
        if session['question_index'] >= len(questions):
            final_score = Score(score=session['scores'], user_id=current_user.id)
            db.session.add(final_score)
            db.session.commit()
            scores = session.pop('scores', 0)
            session.pop('question_index', None)
            return render_template('result.html', scores=scores, total=len(questions), user = current_user)

        current_question = questions[session['question_index']]

    return render_template('questions.html', current_question=current_question, category = category)

#submitting quiz and giving the result after the quiz
@app.route('/submit_quiz', methods=["POST"])
def submit_quiz():
    user = current_user
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    scores = 0
    for question in Question.query.all():
        user_answer = request.form.get(f'question{question.id}')
        if user_answer == question.answer.lower():
           scores += 1
    return render_template('result.html', user = user, scores=scores)

# route for logging out of the quiz
@app.route('/logout')
def logout():
  if not g.user:
    return redirect(url_for('login'))
  session.pop('user_id',None)
  session.pop('scores',None)
  session.clear()
  return redirect(url_for('index'))

def is_admin():
    return current_user.role == 'admin'

@app.route("/change_category", methods=["POST"])
def change_category():
    if not is_admin():
        flash("You do not have permission to change categories.", "danger")
        return redirect(url_for('index'))  # Redirect to the homepage or a safe page

    # Code to change categories
    # Only the admin can access this logic
    category_id = request.form['category_id']
    new_name = request.form['new_name']
    # Your logic to update the category in the database...
    flash("Category updated successfully!", "success")
    return redirect(url_for('categories'))

from app import routes