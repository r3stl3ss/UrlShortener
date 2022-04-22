from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


@app.route("/link_generator", methods=['POST', 'GET'])
def generate():
    if request.method == 'POST':
        original_link = request.form['original_link']
        hashed_link = 'HASH' + original_link + 'ENDHASH'
        link = Link(original_link=original_link, hashed_link=hashed_link, is_deleted=False)
        try:
            db.session.add(link)
            db.session.commit()
            return redirect('/')
        except:
            return "Error while shortening link"
    else:
        return render_template('generator.html')



if __name__ == '__main__':
    app.run(debug=True)
