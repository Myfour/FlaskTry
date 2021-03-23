from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from flask_login import login_required
from bluelog.models import Post, Category, Comment
from bluelog.forms import PostForm, CategoryForm, CommentForm
from bluelog.extensions import db
from bluelog.utils import redirect_back

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/settings')
# @login_required
def settings():
    return render_template('admin/settings.html')


# 使用钩子来实现对该蓝本下所有view添加login_required
@admin_bp.before_request
@login_required
def login_protect():
    pass


@admin_bp.route('/post/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect_back()


@admin_bp.route('/newcategory', methods=['GET', 'POST'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Add category successed.', 'success')
        return redirect(url_for('.manage_category'))
    return render_template('admin/new_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category updated.', 'success')
        return redirect(url_for('.manage_category'))
    form.name.data = category.name  # 注意这个的位置，位置不对会影响表单的验证导致修改不了
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('delete successed', 'success')
    return redirect(url_for('.manage_category'))


@admin_bp.route('/post/manage')
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html',
                           pagination=pagination,
                           posts=posts)


@admin_bp.route('/category/manage')
def manage_category():
    page = request.args.get('page', 1, type=int)
    pagination = Category.query.order_by(Category.name.asc()).paginate(
        page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
    categories = pagination.items
    return render_template('admin/manage_category.html',
                           pagination=pagination,
                           categories=categories)


@admin_bp.route('/managecomment')
def manage_comment():
    filter_rule = request.args.get('filter', 'all')
    page = request.args.get('page', 1, type=int)
    if filter_rule == 'unread':
        filter_comments = Comment.query.filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filter_comments = Comment.query.filter_by(from_admin=True)
    else:
        filter_comments = Comment.query
    pagination = filter_comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
    comments = pagination.items
    return render_template('admin/manage_comment.html',
                           pagination=pagination,
                           comments=comments)


@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'success')
    return redirect_back()


@admin_bp.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    form = CommentForm()
    comment = Comment.query.get_or_404(comment_id)
    if form.validate_on_submit():
        comment.author = form.author.data
        comment.email = form.email.data
        comment.site = form.site.data
        comment.body = form.body.data
        db.session.commit()
        flash('Edit successed.', 'success')
        return redirect(url_for('.manage_comment'))
    form.author.data = comment.author
    form.email.data = comment.email
    form.site.data = comment.site
    form.body.data = comment.body
    return render_template('admin/edit_comment.html', form=form)


@admin_bp.route('/comment/<int:post_id>/set', methods=['POST'])
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('Comment Disabled.', 'info')
    else:
        post.can_comment = True
        flash('Comment Eabled.', 'info')
    db.session.commit()
    return redirect(url_for('blog.show_post', post_id=post.id))


@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('Comment has approved.', 'success')
    return redirect_back()