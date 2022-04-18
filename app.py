from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
db = SQLAlchemy(app)


class Link(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    original_link = db.Column(db.String(), nullable=False)
    hashed_link = db.Column(db.String(), nullable=False)
    is_deleted = db.Column(db.Boolean)
    date_of_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Link %r>" % self.id


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
