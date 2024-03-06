from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
Bootstrap5(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///activity.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class ToDo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    todo: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


class MyForm(FlaskForm):
    todo = StringField(label='Type your ToDo')
    submit = SubmitField(label='Add')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = MyForm()
    todo = []
    todo = db.session.execute(db.select(ToDo).order_by(ToDo.id)).scalars().all()
    if form.validate_on_submit():
        new_todo = ToDo(
            todo=form.todo.data
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('index.html', form=form, todo=todo)


@app.route('/delete')
def delete():
    db.session.query(ToDo).delete()
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, port=5003)
