from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bucks.auth import login_required
from bucks.db import get_db

bp = Blueprint('item', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('item/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        print(request.form)
        picture = request.form['picture']
        error = None

        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Description is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, picture, author_id, contact)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, picture, g.user['id'], g.user['contact'])
            )
            db.commit()
            return redirect(url_for('item.index'))

    return render_template('item/create.html')