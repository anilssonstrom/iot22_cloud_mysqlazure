from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysupersecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:example@localhost/flaskcodeloop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/init')
def init():
    """Create the database"""
    from sqlalchemy import create_engine, text

    with create_engine('mysql+pymysql://root:example@localhost').connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS flaskcodeloop"))
        conn.execute(text("commit"))

    db.create_all()
    u = UserInfo('codeloop', 1234)
    u1 = UserInfo('parwiz', 12345)
    db.session.add(u)
    db.session.add(u1)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if request.form['username'] != 'codeloop' or request.form['password'] != '12345':
            flash("Invalid Credentials, Please Try Again")


        else:
            return redirect(url_for('index'))

    return render_template('login.html', form=form)


# run flask app
if __name__ == "__main__":
    app.run(debug=True)
