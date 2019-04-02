from flask import Flask, redirect, render_template, session
from flask_bootstrap import Bootstrap
from DataBase import DB, NewsModel, UserModel
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')


app = Flask(__name__)
bootstrap = Bootstrap(app)
db = DB()
factor = 1


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name = form.username.data
    password = form.password.data
    user_model = UserModel(db.get_connection())
    exists = user_model.exists(user_name, password)
    if exists[0]:
        session['username'] = user_name
        session['user_id'] = exists[1]
        session['user_game'] = exists[2]
        session['user_factor'] = exists[3]
        print(user_model.get_all())
        return redirect("/game")
    else:
        user_model.insert(user_name, password)
        return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        return redirect('/login')
    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        nm = NewsModel(db.get_connection())
        nm.insert(title, content, session['user_id'])
        return redirect("/news")
    return render_template('add_news.html', title='Добавление новости',
                           form=form, username=session['username'])


@app.route('/share_news', methods=['GET', 'POST'])
def share_news():
    if 'username' not in session:
        return redirect('/login')
    title = session['username']
    content = 'Я набрал {} очков в ВК Кликере!'.format(session['user_game'])
    nm = NewsModel(db.get_connection())
    nm.insert(title, str(content), session['user_id'])
    return redirect("/news")


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/news")


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    session.pop('user_game', 0)
    session.pop('user_factor', 1)
    return redirect('/login')


@app.route('/table')
def table():
    if 'username' not in session:
        return redirect('/login')
    return render_template('table.html')


@app.route('/game')
def game():
    if 'username' not in session:
        return redirect('/login')
    user_model = UserModel(db.get_connection())
    #print(user_model.get_all())
    return render_template('game.html')


@app.route('/game_plus')
def game_plus():
    if 'username' not in session:
        return redirect('/login')
    user_model = UserModel(db.get_connection())
    user_model.add_game(session["user_id"])
    #print(user_model.get_all())
    session['user_game'] += session['user_factor']
    return redirect('/game')


@app.route('/game_factor')
def game_factor():
    if 'username' not in session:
        return redirect('/login')
    user_model = UserModel(db.get_connection())
    user_model.add_factor(session["user_id"])
    session['user_factor'] += 1
    session['user_game'] -= 100
    return redirect('/game')


@app.route('/game_factor_2')
def game_factor_2():
    if 'username' not in session:
        return redirect('/login')
    user_model = UserModel(db.get_connection())
    user_model.add_factor_2(session["user_id"])
    session['user_factor'] += 2
    session['user_game'] -= 200
    return redirect('/game')


@app.route('/game_factor_3')
def game_factor_3():
    if 'username' not in session:
        return redirect('/login')
    user_model = UserModel(db.get_connection())
    user_model.add_factor_3(session["user_id"])
    session['user_factor'] += 3
    session['user_game'] -= 300
    return redirect('/game')


@app.route('/game_factor_4')
def game_factor_4():
    if 'username' not in session:
        return redirect('/login')
    user_model = UserModel(db.get_connection())
    user_model.add_factor_4(session["user_id"])
    session['user_factor'] += 4
    session['user_game'] -= 400
    return redirect('/game')


@app.route('/news', methods=['GET'])
def news():
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection()).get_all()
    return render_template('news.html', news=nm)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret_key'
    app.run(port=8080, host='127.0.0.1')
