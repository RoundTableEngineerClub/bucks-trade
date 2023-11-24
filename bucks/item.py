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
        error = None

        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Description is required.'
     
        # for storing file into db
        picture = request.files['picture']
        filename = secure_filename(picture.filename)
        print(os.getcwd())
        print(os.path.join(current_app.config['UPLOAD'], filename))
        picture.save(os.path.join(current_app.config['UPLOAD'], filename))
        
        img = os.path.join(current_app.config['UPLOAD'], filename)
        return render_template('item/index.html', img=img)
    
        if __name__ == '__main__':
            app.run(debug=True, port=8001)

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

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
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

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('item.index'))