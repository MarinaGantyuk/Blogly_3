"""Blogly application."""

from flask import Flask,render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, User, Post, Tag, PostTag


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
#db.init_app(app)   
with app.app_context():
    db.create_all()

@app.route('/')
def home_page():
    return redirect('/users')


@app.route('/users')
def users_page():
    users = db.session.execute(db.select(User)).scalars()
    return render_template('home.html', users = users)

@app.route('/users/<int:id>')
def user_detail(id):
    user = db.get_or_404(User,id)
    posts = Post.query.filter_by(user_id = user.id).all()
    return render_template('user_detail.html', user = user, posts = posts)

@app.route('/users/new', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        user = User( 
            #id = num(request.form['id']),
            first_name = request.form['first_name'],
            last_name = request.form['last_name'],
            image_url = request.form['image_url']
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/users/' + str(user.id))

    return render_template('user_addform.html')

@app.route('/users/<int:id>/delete', methods=['POST','GET'])
def delete_user(id):
    user=db.get_or_404(User, id)
    if request.method=='POST':
        db.session.delete(user)
        db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>/edit', methods=['POST', 'GET'])
def edit_user(id):
    user=db.get_or_404(User, id)
    if request.method == 'POST':

        user.first_name = request.form['first_name'],
        user.last_name = request.form['last_name'],
        user.image_url = request.form['image_url']
        user.veryfied = True
        db.session.commit()
        return redirect('/users/' + str(user.id))

    return render_template('user_editform.html', user=user)

@app.route('/users/<int:id>/posts/new', methods=['POST', 'GET'])
def post_user(id):
    user=db.get_or_404(User, id) 
    tags = db.session.execute(db.select(Tag)).scalars()
    if request.method == 'POST':
        post = Post( 
            title = request.form['title'],
            content = request.form['content'],
            user_id = user.id
        )
        db.session.add(post)
        db.session.commit()
        return redirect('/users/' + str(user.id))

    return render_template('post_addform.html', user=user, tags=tags)

@app.route('/posts/<int:id>')
def post_detail(id):
    post = db.get_or_404(Post,id)
    user = db.get_or_404(User,post.user_id)
    tag_ids=PostTag.query.with_entities(PostTag.tag_id).filter_by(post_id=id).all()
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    #to do pass tags to template
    return render_template('post_detail.html', post = post, user = user)

@app.route('/posts/<int:id>/edit', methods=['POST', 'GET'])
def edit_post(id):
    post=db.get_or_404(Post, id)
    tag_ids=PostTag.query.with_entities(PostTag.tag_id).filter_by(post_id=id).all()
    tags = db.session.execute(db.select(Tag)).scalars()
    tagsforpost = [{'name': el.name, 'id': el.id, 'checked': el.id in tag_ids} for el in tags]
    if request.method == 'POST':

        post.title = request.form['title'],
        post.content = request.form['content'],
        post.veryfied = True
        tag_ids = [int(num) for num in request.form.getlist("tags")]
        #for tag in tagsforpost:
            #if tag.checked and tag.id not in tag_ids:

        #user = db.get_or_404(User,id)
        db.session.commit()
        return redirect('/posts/' + str(post.id))

    return render_template('post_editform.html', post = post, tags = tagsforpost) 

@app.route('/posts/<int:id>/delete', methods=['POST','GET'])
def delete_post(id):
    post=db.get_or_404(Post, id)
    if request.method=='POST':
        db.session.delete(post)
        db.session.commit()

    return redirect('/users/' + str(post.user_id))

@app.route('/tags')
def tags_page():
    tags = db.session.execute(db.select(Tag)).scalars()
    return render_template('tags.html', tags = tags)

@app.route('/tags/new', methods=['POST', 'GET'])
def post_tag():
    if request.method == 'POST':
        tag = Tag( 
            name = request.form['name']
        )
        db.session.add(tag)
        db.session.commit()
        return redirect('/tags')

    return render_template('tag_addform.html')

@app.route('/tags/<int:id>')
def tag_detail(id):
    tag=db.get_or_404(Tag, id)
    post_ids=PostTag.query.with_entities(PostTag.post_id).filter_by(tag_id=id).all()
    postsbytag = Post.query.filter(Post.id.in_(post_ids)).all()
    return render_template('tag_detail.html', tag=tag, posts=postsbytag)

@app.route('/tags/<int:id>/delete', methods=['POST','GET'])
def delete_tag(id):
    tag=db.get_or_404(Tag, id)
    if request.method=='POST':
        db.session.delete(tag)
        db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:id>/edit', methods=['POST', 'GET'])
def edit_tag(id):
    tag=db.get_or_404(Tag, id)
    if request.method == 'POST':

        tag.name = request.form['name'],
        tag.veryfied = True
        db.session.commit()
        return redirect('/tags/' + str(tag.id))

    return render_template('tag_editform.html', tag = tag)
















