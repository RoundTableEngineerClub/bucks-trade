# python module
import os

# third party module
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, send_from_directory
)
from werkzeug.exceptions import abort

# personal/private module
from bucks.auth import login_required
from bucks.db import get_db
from werkzeug.utils import secure_filename

bp = Blueprint('item', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username, picture, u.contact'
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
        error = None

        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Description is required.'
     
        # for storing file into db
        picture = request.files['picture']
        filename = secure_filename(picture.filename)
        picture.save(os.path.join(current_app.config['UPLOAD'], filename))

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, picture, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, picture.filename, g.user['id'])
            )
            db.commit()
            return redirect(url_for('item.index'))
    return render_template('item/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, picture'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Description is required.'

        picture = request.files['picture']
        if picture:
            picture.save(os.path.join(current_app.config['UPLOAD'], picture.filename))

            if error is not None:
                flash(error)
            else:
                db = get_db()
                db.execute(
                    'UPDATE post SET title = ?, body = ?, picture = ?'
                    ' WHERE id = ?',
                    (title, body, picture.filename, id)
                )
                db.commit()
                return redirect(url_for('item.index'))
            
        else:
            if error is not None:
                flash(error)
            else:
                db = get_db()
                db.execute(
                    'UPDATE post SET title = ?, body = ?'
                    ' WHERE id = ?',
                    (title, body, id)
                )
                db.commit()
                return redirect(url_for('item.index'))
            

    return render_template('item/update.html', post=post)

@bp.route('/<int:id>/postDetail', methods=('GET',))
@login_required
def postDetail(id):
    error = None
    
    if error is not None:
        flash(error)
    else:
        db = get_db()
        result = db.execute(
            'SELECT p.id, title, body, created, author_id, username, picture, u.contact'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE p.id = ?',
            (id,)
        ).fetchone()
            

    return render_template('item/postDetail.html', result=result)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('item.index'))

@bp.route('/<int:id>/picture')
def picture(id):
    post = get_post(id, check_author=False)
    return send_from_directory(current_app.config['UPLOAD'], post['picture'])