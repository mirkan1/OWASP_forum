from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from .forms import SearchForm

bp = Blueprint('forum', __name__)

# @bp.route('/search', methods=["GET", 'POST'])
# @login_required
# def search():
#     form = SearchForm()
#     if not form.validate_on_submit():
#         return redirect(url_for('index'))
#     return redirect((url_for('search_results', query=form.search.data)))






@bp.route('/search_results/<query>', methods=["GET"])
def search_results(query):
    import json as js
    import re
    json = {
        "users": [],
        "category": [],
        "thread": {
            "title": [],
            "body": [],
        },
        "post": [],
    }
    try:
        db = get_db()
        users = db.execute(f'SELECT * FROM user WHERE username LIKE "%{str(query)}%"').fetchall()
        category = db.execute(f'SELECT * FROM category WHERE title LIKE "%{str(query)}%"').fetchall()
        thread = db.execute(f'SELECT * FROM thread WHERE title LIKE "%{str(query)}%"').fetchall()
        thread = db.execute(f'SELECT * FROM thread WHERE body LIKE "%{str(query)}%"').fetchall()
        post = db.execute(f'SELECT * FROM post WHERE body LIKE "%{str(query)}%"').fetchall()
        # '"Attacker "/><script>alert(1)</script>"'
        for i in range(len(users)): json["users"].append(users[i]['username'])
        for i in json["users"]: i = "".join(i.split('"'))
        for i in json["users"]: i = "".join(i.split("'"))
        for i in range(len(category)): json["category"].append(category[i]['title'])
        for i in json["category"]: i = "".join(i.split('"'))
        for i in json["category"]: i = "".join(i.split("'"))
        for i in range(len(thread)): json["thread"]['title'].append(thread[i]['title'])
        for i in json["thread"]['title']: i = "".join(i.split('"'))
        for i in json["thread"]['title']: i = "".join(i.split("'"))
        for i in range(len(thread)): json["thread"]['body'].append(thread[i]['body'])
        for i in json["thread"]['body']: i = "".join(i.split('"'))
        for i in json["thread"]['body']: i =  "".join(i.split("'"))
        for i in range(len(post)): json["post"].append(post[i]['body'])
        for i in range(len(json["post"])):
            remzi = re.search("<.+>", str(json["post"][i]))
            if remzi != None:
                match = "".join(remzi.string.split(remzi.string[remzi.span()[0]]))
                match = "".join(match.split(match[remzi.span()[1] - 3]))
                json["post"][i] = match
        json = js.dumps(json)
        db.commit()
    except:
        return render_template('forum/search_results.html', query=query, results=json)
         
    return render_template('forum/search_results.html', query=query, results=json)

@bp.route('/')
def index():
    db = get_db()
    categories = db.execute('SELECT rowid, * FROM category;')
    return render_template('forum/index.html', categories = categories)

@bp.route('/category/<int:category_id>')
def category(category_id):
    db = get_db()
    threads = db.execute('SELECT rowid, * FROM thread WHERE category_id=?;', (str(category_id)))
    return render_template('forum/threads.html', threads = threads, category_id=category_id)

@bp.route('/category/<int:category_id>/thread/<int:thread_id>', methods=('GET', 'POST'))
def thread(thread_id, category_id):
    if request.method == 'POST':
        body = request.form['body']
        error = None #catch spams

        if error is not None:
            flash(error)
        else:

            db = get_db()
            db.execute(
                'INSERT INTO post (body, author_id, thread_id)'
                ' VALUES ( ?, ?,?)',
                (body, g.user['id'], str(thread_id))
            )
            posts = db.execute('SELECT rowid, * FROM post').fetchall()
            users = db.execute('SELECT rowid, * FROM user').fetchall()
            thread = db.execute('SELECT rowid, * FROM thread WHERE id=?;', (str(thread_id))).fetchall()
            body = thread[0]['body']
            db.commit()
            return render_template('forum/posts.html', body=body, users=users, posts=posts, thread_id=thread_id, category_id=category_id)

    db = get_db()
    posts = db.execute('SELECT rowid, * FROM post').fetchall()
    users = db.execute('SELECT rowid, * FROM user').fetchall()
    thread = db.execute('SELECT rowid, * FROM thread WHERE id=?;', (str(thread_id))).fetchall()
    body = thread[0]['body']
    db.commit()
    return render_template('forum/posts.html', users=users, posts=posts, thread_id=thread_id, category_id=category_id, body=body)

@bp.route('/posts')
def posts():
    db = get_db()
    posts = db.execute(
        'SELECT p.id,  body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('forum/posts.html', posts=posts)

@bp.route('/create/<int:category_id>/thread/<int:thread_id>', methods=('GET', 'POST'))
@login_required
def create(thread_id, category_id):
    if request.method == 'POST':
        body = request.form['body']
        error = None #catch spams

        if error is not None:
            flash(error)
        else:

            db = get_db()
            db.execute(
                'INSERT INTO post (body, author_id, thread_id)'
                ' VALUES ( ?, ?,?)',
                (body, g.user['id'], str(thread_id))
            )
            posts = db.execute('SELECT rowid, * FROM post').fetchall()
            db.commit()
            return render_template('forum/posts.html', posts=posts, thread_id=thread_id, category_id=category_id)
    return render_template('forum/create.html',thread_id=thread_id)

@bp.route('/create/<int:category_id>/', methods=('GET', 'POST'))
@login_required
def create_thread(category_id):
    if request.method == 'POST':
        body = request.form['body']
        title = request.form['title']
        error = None #catch spams

        if error is not None:
            flash(error)
        else:

            db = get_db()
            db.execute(
                        'INSERT INTO thread ( title, body, category_id )'
                        ' VALUES (?, ?, ?)',
                        (title, body, category_id)
                    )
            db = get_db()
            threads = db.execute('SELECT rowid, * FROM thread WHERE category_id=?;', (str(category_id)))
            db.commit()
            return render_template('forum/threads.html', threads = threads, category_id=category_id)
    return render_template('forum/create.html', category_id=category_id)


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        
        body = request.form['body']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET , body = ?'
                ' WHERE id = ?',
                ( body, id)
            )
            db.commit()
            return redirect(url_for('forum.posts'))

    return render_template('forum/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('forum.posts'))

@bp.route('/<int:id>/details', methods=('GET',))
def details(id):
    post = get_db().execute(
        'SELECT p.id, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    return render_template('forum/details.html', post=post)

@bp.route('/cross_site_scripting', methods=('GET',))
def cross_site_scripting():
    return render_template('example/cross_site_scripting.html')
