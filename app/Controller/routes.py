from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config
from flask_login import current_user,login_required
from app import db
from app.Model.models import Post,Tag,postTags
from app.Controller.forms import PostForm,SortForm
bp_routes = Blueprint("routes", __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER  #'..\\View\\templates'

@bp_routes.route("/", methods=["GET", "POST"])
@bp_routes.route("/index", methods=["GET", "POST"])
@login_required
def index():
    sform = SortForm()
    posts = None 
    ptotal = None
    if sform.validate_on_submit():
        if sform.userSort.data == True:
            posts = current_user.get_user_posts()
            ptotal = posts.count()
        elif sform.sort.data == 1:
            posts = Post.query.order_by(Post.timestamp.desc()).all()
            ptotal = Post.query.count()
        elif sform.sort.data == 2:
            posts = Post.query.order_by(Post.title.desc()).all()
            ptotal = Post.query.count()
        elif sform.sort.data == 3:
            posts = Post.query.order_by(Post.likes.desc()).all()
            ptotal = Post.query.count()
        else:
            posts = Post.query.order_by(Post.happiness_level.desc()).all()
            ptotal = Post.query.count()
    else:
        posts = Post.query.order_by(Post.timestamp.desc()).all()
        ptotal = Post.query.count()
    return render_template("index.html", title="Smile Portal", posts=posts, ptotal=ptotal, form=sform,is_authenticated = current_user.is_authenticated,current_user = current_user)

@bp_routes.route("/postsmile", methods=["GET", "POST"])
@login_required
def create():
    cform = PostForm()
    if cform.validate_on_submit():
        newPost = Post(
            title=cform.title.data, body=cform.body.data, happiness_level=cform.happiness_level.data,user_id = current_user.id
        )
        t1 = cform.tag.data
        for tag in t1:
            newPost.tags.append(tag)

        db.session.add(newPost)
        db.session.commit()
        flash('Succsesfuly Submitted Smile')
        return(redirect(url_for('routes.index')))
    return render_template("create.html", title="Post Form", form=cform)


@bp_routes.route("/like/<post_id>", methods=["POST","GET"])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Post doesnt exist')
        return redirect(url_for('routes.index'))  
    else:
        post.likes+=1
        db.session.commit()
    return redirect(url_for('routes.index'))

@bp_routes.route("/deletepost/<post_id>", methods = ['DELETE', 'POST','GET'])
@login_required
def deletepost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    for tag in post.tags:
        post.tags.remove(tag)
    db.session.commit()
    db.session.delete(post)
    db.session.commit()
    flash('Deleted Post')
    return redirect(url_for('routes.index'))