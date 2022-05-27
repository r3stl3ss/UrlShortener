import sqlite3

from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from hashids import Hashids
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'salt_for_coding'
hashids = Hashids(min_length=6, salt=app.config['SECRET_KEY'])
db = SQLAlchemy(app)


class Link(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    original_link = db.Column(db.String(), nullable=False)
    hashed_link = db.Column(db.String(), default=None)
    is_deleted = db.Column(db.Boolean)
    date_of_creation = db.Column(db.DateTime, default=datetime.utcnow)
    times_clicked = db.Column(db.BigInteger(), default=0)

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
    all_except_deleted = Link.query.filter(Link.is_deleted == False)
    if request.method == 'POST':
        original_link = request.form['original_link']
        results = [id[0] for id in Link.query.with_entities(Link.id).all()]
        hashed_link = hashids.encode(max(results) + 1)
        link = Link(original_link=original_link, hashed_link=hashed_link, is_deleted=False)
        try:
            db.session.add(link)
            db.session.commit()
            shown_url = "127.0.0.1:5000/" + hashed_link
            return render_template('shortened_link_page.html', short_url=shown_url, link="redir/" + hashed_link)
        except Exception as e:
            print(e.with_traceback())
            return "Error while shortening link"
    else:
        return render_template('generator.html')


@app.route("/get_all_links")
def get_hash():
    all_except_deleted = Link.query.filter(Link.is_deleted == False)
    return render_template("allLinks.html", links=all_except_deleted)


@app.route("/redir/<hashed_link>")
def redirect_to_short(hashed_link):
    link_id = hashids.decode(hashed_link)[0]
    if link_id:
        orig = Link.query.filter(Link.id == link_id).filter(Link.is_deleted == False).first()
        orig.times_clicked += 1
        db.session.commit()
        log = orig.original_link
        return redirect(log)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))


@app.route("/del/<hashed_link>")
def delete_link(hashed_link):
    link_id = hashids.decode(hashed_link)[0]
    link = Link.query.filter(Link.id == link_id).filter(Link.is_deleted == False).first()
    link.is_deleted = True
    db.session.commit()
    return redirect('/get_all_links')


if __name__ == '__main__':
    app.run(debug=True)
